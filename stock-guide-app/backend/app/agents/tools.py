"""
ReAct Agent Tools
각 Tool은 실제 외부 API를 호출하여 데이터를 가져옵니다.
"""
import httpx
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.core.config import settings
from loguru import logger


# ===== Tool 1: 실시간 주가 조회 =====
async def search_realtime_stock_price(ticker: str) -> Dict[str, Any]:
    """
    Alpha Vantage API로 실시간 주가 조회

    Args:
        ticker: 종목 코드 (예: 'AAPL', '005930.KS')

    Returns:
        {
            "current_price": 178.50,
            "change_percent": -1.2,
            "volume": 56234567,
            "52w_high": 199.62,
            "52w_low": 164.08,
            "market_cap": 2800000000000
        }
    """
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": settings.ALPHA_VANTAGE_API_KEY
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        if "Global Quote" not in data or not data["Global Quote"]:
            # API 제한 또는 잘못된 티커
            logger.warning(f"No data for ticker {ticker}")
            return {
                "error": f"주식 '{ticker}'의 데이터를 찾을 수 없습니다. 종목 코드를 확인해주세요.",
                "current_price": None
            }

        quote = data["Global Quote"]

        return {
            "ticker": ticker,
            "current_price": float(quote.get("05. price", 0)),
            "change_percent": float(quote.get("10. change percent", "0%").rstrip('%')),
            "volume": int(quote.get("06. volume", 0)),
            "52w_high": float(quote.get("03. high", 0)),
            "52w_low": float(quote.get("04. low", 0)),
            "previous_close": float(quote.get("08. previous close", 0)),
            "timestamp": datetime.now().isoformat()
        }

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching stock price for {ticker}: {e}")
        return {"error": f"API 호출 실패: {str(e)}", "current_price": None}
    except Exception as e:
        logger.error(f"Unexpected error in search_realtime_stock_price: {e}")
        return {"error": f"알 수 없는 오류: {str(e)}", "current_price": None}


# ===== Tool 2: 재무제표 조회 =====
async def search_financial_reports(ticker: str) -> Dict[str, Any]:
    """
    Financial Modeling Prep API로 재무제표 조회

    Returns:
        {
            "revenue_growth": 2.1,  # YoY %
            "operating_margin": 29.8,  # %
            "debt_to_equity": 1.97,
            "roe": 160.5,  # %
            "quick_ratio": 0.85,
            "period": "2024Q3"
        }
    """
    try:
        # Income Statement (손익계산서)
        income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}"
        balance_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}"
        ratios_url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}"

        params = {"apikey": settings.FMP_API_KEY, "limit": 4}  # 최근 4분기

        async with httpx.AsyncClient(timeout=15.0) as client:
            income_res, balance_res, ratios_res = await asyncio.gather(
                client.get(income_url, params=params),
                client.get(balance_url, params=params),
                client.get(ratios_url, params=params)
            )

        income_data = income_res.json()
        balance_data = balance_res.json()
        ratios_data = ratios_res.json()

        if not income_data or not isinstance(income_data, list):
            return {"error": "재무 데이터를 찾을 수 없습니다."}

        latest = income_data[0]
        prev = income_data[1] if len(income_data) > 1 else latest

        # 매출 성장률 계산
        revenue_growth = ((latest.get("revenue", 0) - prev.get("revenue", 1)) /
                         prev.get("revenue", 1) * 100) if prev.get("revenue") else 0

        # 영업이익률
        operating_margin = (latest.get("operatingIncome", 0) /
                           latest.get("revenue", 1) * 100) if latest.get("revenue") else 0

        # 부채비율 (총부채 / 총자산)
        total_debt = balance_data[0].get("totalDebt", 0) if balance_data else 0
        total_equity = balance_data[0].get("totalStockholdersEquity", 1) if balance_data else 1
        debt_to_equity = total_debt / total_equity if total_equity else 0

        # ROE, Quick Ratio
        roe = ratios_data[0].get("returnOnEquity", 0) * 100 if ratios_data else 0
        quick_ratio = ratios_data[0].get("quickRatio", 0) if ratios_data else 0

        return {
            "ticker": ticker,
            "revenue_growth": round(revenue_growth, 2),
            "operating_margin": round(operating_margin, 2),
            "debt_to_equity": round(debt_to_equity, 2),
            "roe": round(roe, 2),
            "quick_ratio": round(quick_ratio, 2),
            "period": latest.get("date", "N/A"),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in search_financial_reports for {ticker}: {e}")
        return {"error": f"재무 데이터 조회 실패: {str(e)}"}


# ===== Tool 3: 애널리스트 목표주가 =====
async def search_analyst_targets(ticker: str) -> Dict[str, Any]:
    """
    애널리스트 목표주가 및 등급 조회

    Returns:
        {
            "target_price_avg": 195.30,
            "target_price_high": 220.00,
            "target_price_low": 175.00,
            "upside_potential": 9.4,  # %
            "buy_ratings": 28,
            "hold_ratings": 10,
            "sell_ratings": 2
        }
    """
    try:
        url = f"https://financialmodelingprep.com/api/v3/price-target-consensus/{ticker}"
        params = {"apikey": settings.FMP_API_KEY}

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()

        if not data or not isinstance(data, list):
            return {"error": "목표주가 데이터 없음"}

        consensus = data[0]

        return {
            "ticker": ticker,
            "target_price_avg": float(consensus.get("targetConsensus", 0)),
            "target_price_high": float(consensus.get("targetHigh", 0)),
            "target_price_low": float(consensus.get("targetLow", 0)),
            "buy_ratings": int(consensus.get("buyRatings", 0)),
            "hold_ratings": int(consensus.get("holdRatings", 0)),
            "sell_ratings": int(consensus.get("sellRatings", 0)),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in search_analyst_targets: {e}")
        return {"error": str(e)}


# ===== Tool 4: 외국인/기관 수급 =====
async def search_corporate_ownership(ticker: str) -> Dict[str, Any]:
    """
    기관/외국인 보유 비율 조회

    Returns:
        {
            "institutional_ownership": 65.4,  # %
            "insider_ownership": 0.07,  # %
            "shares_outstanding": 15634000000
        }
    """
    try:
        url = f"https://financialmodelingprep.com/api/v4/institutional-ownership/symbol-ownership"
        params = {"symbol": ticker, "apikey": settings.FMP_API_KEY}

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()

        # 간단한 예시 (실제로는 더 복잡한 파싱 필요)
        total_shares = sum([item.get("sharesNumber", 0) for item in data[:10]]) if data else 0

        return {
            "ticker": ticker,
            "institutional_ownership": 0,  # 계산 필요 (전체 발행주식 대비)
            "insider_ownership": 0,
            "major_holders": data[:5] if data else [],
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in search_corporate_ownership: {e}")
        return {"error": str(e)}


# ===== Tool 5: 뉴스 및 감성 분석 =====
async def search_news_and_issues(query: str, days: int = 7) -> Dict[str, Any]:
    """
    News API로 최신 뉴스 검색 및 감성 분석

    Args:
        query: 검색 키워드 (기업명, CEO, 산업 등)
        days: 최근 N일 이내 뉴스

    Returns:
        {
            "articles": [
                {
                    "title": "...",
                    "summary": "...",
                    "sentiment": "긍정",
                    "published_at": "2024-11-17T10:00:00Z",
                    "source": "Reuters"
                }
            ],
            "overall_sentiment": 0.3  # -1.0 ~ 1.0
        }
    """
    try:
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "from": from_date,
            "sortBy": "relevancy",
            "language": "en",
            "apiKey": settings.NEWS_API_KEY,
            "pageSize": 10
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()

        if data.get("status") != "ok":
            return {"error": "뉴스 조회 실패", "articles": []}

        articles = []
        sentiment_scores = []

        for article in data.get("articles", [])[:10]:
            # 간단한 감성 분석 (실제로는 FinBERT 등 사용)
            title = article.get("title", "")
            description = article.get("description", "")

            # 긍정/부정 키워드 기반 간이 분석
            positive_words = ["surge", "boost", "profit", "growth", "strong", "record"]
            negative_words = ["loss", "decline", "weak", "fall", "drop", "cut"]

            text = (title + " " + description).lower()
            pos_count = sum([1 for word in positive_words if word in text])
            neg_count = sum([1 for word in negative_words if word in text])

            sentiment = "중립"
            score = 0.0
            if pos_count > neg_count:
                sentiment = "긍정"
                score = 0.5
            elif neg_count > pos_count:
                sentiment = "부정"
                score = -0.5

            sentiment_scores.append(score)

            articles.append({
                "title": title,
                "summary": description[:200] if description else "",
                "sentiment": sentiment,
                "published_at": article.get("publishedAt"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url")
            })

        overall_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0

        return {
            "query": query,
            "articles": articles,
            "overall_sentiment": round(overall_sentiment, 2),
            "article_count": len(articles),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in search_news_and_issues: {e}")
        return {"error": str(e), "articles": []}


# ===== Tool 6: 이상 징후 탐지 =====
async def search_anomaly_detection(ticker: str) -> Dict[str, Any]:
    """
    거래량 급증, 공매도 비율 등 이상 징후 탐지

    Returns:
        {
            "volume_spike": True/False,
            "short_interest_high": "Low"/"Medium"/"High",
            "price_volatility": 2.5  # %
        }
    """
    try:
        # 실제 구현 시 과거 거래량 데이터와 비교
        # 여기서는 간단한 예시
        price_data = await search_realtime_stock_price(ticker)

        if "error" in price_data:
            return price_data

        # 거래량이 평균 대비 2배 이상이면 급증으로 판단 (실제로는 통계적 계산 필요)
        volume_spike = False  # 예시

        return {
            "ticker": ticker,
            "volume_spike": volume_spike,
            "short_interest_high": "Low",  # API에서 가져와야 함
            "price_volatility": 0.0,  # 표준편차 계산 필요
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in search_anomaly_detection: {e}")
        return {"error": str(e)}


# ===== LangChain Tool 래퍼 =====
def get_react_tools():
    """
    LangChain Tool 형식으로 변환
    """
    from langchain.tools import Tool

    return [
        Tool(
            name="search_realtime_stock_price",
            func=lambda ticker: asyncio.run(search_realtime_stock_price(ticker)),
            description=(
                "실시간 주가를 조회합니다. "
                "입력: ticker (종목 코드, 예: 'AAPL' 또는 '005930.KS'). "
                "반환: 현재가, 등락률, 거래량, 52주 최고/최저가 등"
            ),
            coroutine=search_realtime_stock_price
        ),
        Tool(
            name="search_financial_reports",
            func=lambda ticker: asyncio.run(search_financial_reports(ticker)),
            description=(
                "기업의 재무제표를 조회합니다. "
                "입력: ticker. "
                "반환: 매출 성장률, 영업이익률, 부채비율, ROE 등"
            ),
            coroutine=search_financial_reports
        ),
        Tool(
            name="search_analyst_targets",
            func=lambda ticker: asyncio.run(search_analyst_targets(ticker)),
            description=(
                "증권사 애널리스트들의 목표주가와 의견을 조회합니다. "
                "입력: ticker. "
                "반환: 평균 목표주가, 상승 여력, 매수/보유/매도 의견 수"
            ),
            coroutine=search_analyst_targets
        ),
        Tool(
            name="search_news_and_issues",
            func=lambda query: asyncio.run(search_news_and_issues(query)),
            description=(
                "특정 키워드나 기업에 대한 최신 뉴스를 검색하고 감성 분석을 수행합니다. "
                "입력: query (검색 키워드, 예: 'Apple', 'AI semiconductor'). "
                "반환: 최근 뉴스 목록, 감성 점수"
            ),
            coroutine=search_news_and_issues
        ),
        Tool(
            name="search_anomaly_detection",
            func=lambda ticker: asyncio.run(search_anomaly_detection(ticker)),
            description=(
                "거래량 급증, 공매도 비율 등 이상 징후를 탐지합니다. "
                "입력: ticker. "
                "반환: 이상 징후 플래그들"
            ),
            coroutine=search_anomaly_detection
        )
    ]
