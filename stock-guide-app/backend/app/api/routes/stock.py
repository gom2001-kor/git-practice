"""
Stock Analysis API Routes
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from app.api.schemas.stock import (
    StockQuery,
    AgentResponse,
    DiagnosisResponse,
    KeywordResponse
)
from app.agents.react_agent import (
    get_agent,
    generate_company_diagnosis,
    generate_daily_keyword,
    analyze_stock_for_beginners
)
from app.agents.tools import (
    search_realtime_stock_price,
    search_financial_reports,
    search_analyst_targets,
    search_news_and_issues
)
from loguru import logger

router = APIRouter(prefix="/api/v1/stock", tags=["Stock Analysis"])


@router.post("/analyze", response_model=AgentResponse)
async def analyze_stock(query: StockQuery):
    """
    주식 분석 (ReAct 에이전트 사용)

    초보자 질문에 대해 AI 에이전트가 추론하고 도구를 사용하여 답변합니다.
    """
    try:
        question = query.question or "이 주식에 대해 종합적으로 분석해주세요."

        result = await analyze_stock_for_beginners(query.ticker, question)

        return AgentResponse(
            answer=result["answer"],
            tools_used=result["tools_used"],
            success=result["success"],
            intermediate_steps=result.get("intermediate_steps")
        )

    except Exception as e:
        logger.error(f"Error in analyze_stock: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diagnosis/{ticker}")
async def get_company_diagnosis(ticker: str):
    """
    기업 건강진단서 2.0

    ReAct 에이전트가 모든 도구를 사용하여 종합 건강진단서를 생성합니다.
    """
    try:
        result = await generate_company_diagnosis(ticker)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error"))

        return {
            "ticker": ticker,
            "diagnosis": result["answer"],
            "tools_used": result["tools_used"],
            "generated_at": "2025-11-17T10:00:00Z"  # 실제로는 datetime.now()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_company_diagnosis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/price/{ticker}")
async def get_stock_price(ticker: str):
    """
    실시간 주가 조회 (단순 도구 호출)
    """
    try:
        price_data = await search_realtime_stock_price(ticker)

        if "error" in price_data:
            raise HTTPException(status_code=404, detail=price_data["error"])

        return price_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stock_price: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/financials/{ticker}")
async def get_financials(ticker: str):
    """
    재무제표 조회
    """
    try:
        financials = await search_financial_reports(ticker)

        if "error" in financials:
            raise HTTPException(status_code=404, detail=financials["error"])

        return financials

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_financials: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/news")
async def get_news(query: str, days: int = 7):
    """
    뉴스 검색 및 감성 분석
    """
    try:
        news_data = await search_news_and_issues(query, days)

        if "error" in news_data:
            raise HTTPException(status_code=400, detail=news_data["error"])

        return news_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/daily-keyword")
async def get_daily_keyword():
    """
    오늘의 산업 키워드

    매일 8시 50분에 자동 생성되며, 이 API로 조회합니다.
    (실제로는 DB에서 가져오되, 없으면 생성)
    """
    try:
        # TODO: DB에서 오늘 날짜 키워드 조회
        # 없으면 generate_daily_keyword() 실행

        result = await generate_daily_keyword()

        return {
            "keyword": "AI Semiconductor (예시)",  # 파싱 필요
            "description": result["answer"][:200],
            "sentiment": "긍정",
            "generated_at": "2025-11-17T09:00:00Z"
        }

    except Exception as e:
        logger.error(f"Error in get_daily_keyword: {e}")
        raise HTTPException(status_code=500, detail=str(e))
