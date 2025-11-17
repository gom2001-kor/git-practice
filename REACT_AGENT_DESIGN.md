# ReAct + RAG 에이전트 설계 문서

## ReAct 프레임워크 개요

**ReAct (Reasoning + Acting)** 는 LLM이 단순히 텍스트 생성이 아닌, 도구를 사용하여 문제를 해결하도록 하는 프레임워크입니다.

### 핵심 사이클
```
1. Thought (사고): 현재 상황을 분석하고 다음 행동을 계획
2. Action (행동): 특정 도구를 선택하여 실행
3. Observation (관찰): 도구 실행 결과를 확인
4. [반복] → Final Answer (최종 답변)
```

---

## 도구(Tools) 정의

각 도구는 **하나의 명확한 책임**을 가지며, 환각 방지를 위해 **실제 API/데이터베이스**에서만 정보를 가져옵니다.

### Tool 1: search_realtime_stock_price
```python
{
    "name": "search_realtime_stock_price",
    "description": "지정된 종목의 실시간 주가 정보를 조회합니다. 현재가, 등락률, 거래량, 52주 최고/최저가를 반환합니다.",
    "parameters": {
        "ticker": {
            "type": "string",
            "description": "주식 종목 코드 (예: 'AAPL', '005930.KS')"
        }
    },
    "returns": {
        "current_price": "현재가 (USD/KRW)",
        "change_percent": "등락률 (%)",
        "volume": "거래량",
        "52w_high": "52주 최고가",
        "52w_low": "52주 최저가",
        "market_cap": "시가총액"
    }
}
```

**구현 예시** (Alpha Vantage API):
```python
async def search_realtime_stock_price(ticker: str) -> dict:
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": settings.ALPHA_VANTAGE_KEY
    }
    response = await httpx.get(url, params=params)
    data = response.json()["Global Quote"]

    return {
        "current_price": float(data["05. price"]),
        "change_percent": float(data["10. change percent"].rstrip('%')),
        "volume": int(data["06. volume"]),
        # ... Redis 캐싱 (1분)
    }
```

---

### Tool 2: search_financial_reports
```python
{
    "name": "search_financial_reports",
    "description": "기업의 최근 재무제표를 조회합니다. 수익성(영업이익률), 안정성(부채비율), 성장성(매출 증가율)을 반환합니다.",
    "parameters": {
        "ticker": "종목 코드"
    },
    "returns": {
        "revenue_growth": "매출 성장률 (YoY %)",
        "operating_margin": "영업이익률 (%)",
        "debt_to_equity": "부채비율",
        "roe": "자기자본이익률 (ROE %)",
        "quick_ratio": "당좌비율",
        "period": "재무제표 기준 분기"
    }
}
```

**구현 예시** (Financial Modeling Prep API):
```python
async def search_financial_reports(ticker: str) -> dict:
    # Income Statement + Balance Sheet 조회
    # 초보자용 번역: "영업이익률 15% → 건강함"
    pass
```

---

### Tool 3: search_analyst_targets
```python
{
    "name": "search_analyst_targets",
    "description": "증권사 애널리스트들의 목표 주가와 의견(매수/보유/매도)을 조회합니다.",
    "parameters": {
        "ticker": "종목 코드"
    },
    "returns": {
        "target_price_avg": "평균 목표주가",
        "target_price_high": "최고 목표주가",
        "target_price_low": "최저 목표주가",
        "upside_potential": "상승 여력 (%)",
        "buy_ratings": "매수 의견 수",
        "hold_ratings": "보유 의견 수",
        "sell_ratings": "매도 의견 수"
    }
}
```

---

### Tool 4: search_corporate_ownership
```python
{
    "name": "search_corporate_ownership",
    "description": "외국인, 기관, 개인 투자자의 보유 비율 및 최근 매수/매도 동향을 조회합니다.",
    "parameters": {
        "ticker": "종목 코드"
    },
    "returns": {
        "foreign_ownership": "외국인 보유 비율 (%)",
        "institutional_ownership": "기관 보유 비율 (%)",
        "recent_foreign_net_buy": "최근 5일 외국인 순매수 (주)",
        "recent_institutional_net_buy": "최근 5일 기관 순매수 (주)"
    }
}
```

---

### Tool 5: search_news_and_issues
```python
{
    "name": "search_news_and_issues",
    "description": "특정 키워드나 기업에 대한 최신 뉴스, CEO 평판, 호재/악재를 검색합니다.",
    "parameters": {
        "query": "검색 키워드 (기업명, CEO 이름, 산업 키워드 등)"
    },
    "returns": {
        "articles": [
            {
                "title": "기사 제목",
                "summary": "기사 요약 (100자)",
                "sentiment": "긍정/중립/부정",
                "published_at": "발행 시각",
                "source": "언론사"
            }
        ],
        "overall_sentiment": "전체 감성 점수 (-1.0 ~ 1.0)"
    }
}
```

**구현 예시** (News API + Sentiment Analysis):
```python
async def search_news_and_issues(query: str) -> dict:
    # 1. News API에서 최근 7일 기사 검색
    # 2. HuggingFace FinBERT로 감성 분석
    # 3. RAG: 기사 임베딩 → Pinecone 저장
    pass
```

---

### Tool 6: search_anomaly_detection
```python
{
    "name": "search_anomaly_detection",
    "description": "거래량 급증, 공매도 비율 급등 등 이상 징후를 탐지합니다.",
    "parameters": {
        "ticker": "종목 코드"
    },
    "returns": {
        "volume_spike": "거래량 폭증 여부 (True/False)",
        "short_interest_high": "공매도 비율 위험 수준 (Low/Medium/High)",
        "price_volatility": "최근 변동성 (표준편차 %)"
    }
}
```

---

## RAG (Retrieval-Augmented Generation) 구조

### 환각 방지 메커니즘
```
1. 뉴스/보고서 수집 → 텍스트 청킹 (512 토큰 단위)
2. OpenAI Embeddings로 벡터화
3. Pinecone/Qdrant에 저장
4. 사용자 질문 → 유사도 검색 (Top-K=5)
5. 검색된 문서만 LLM 컨텍스트로 제공
6. LLM이 문서 기반 답변 생성 (인용 포함)
```

### 예시 플로우: "삼성전자 건강진단서 요청"
```
User Query: "삼성전자의 건강진단서를 보여줘"

[RAG 검색]
→ Pinecone에서 "삼성전자" 관련 최근 재무보고서 임베딩 검색
→ Top 3 문서 반환:
  1. "2024 Q3 실적 발표: 영업이익 6.6조원..."
  2. "반도체 업황 개선... HBM3E 양산..."
  3. "외국인 3일 연속 순매수..."

[LLM 프롬프트]
"""
당신은 주식 초보자를 위한 친절한 가이드입니다.
아래 문서들을 참고하여 삼성전자의 건강진단서를 작성하세요.

[문서 1] ...
[문서 2] ...
[문서 3] ...

답변 형식:
- 수익성: [평가] (근거)
- 안정성: [평가] (근거)
- 투자자 관심: [평가] (근거)
"""
```

---

## ReAct 사이클 실행 예시

### 시나리오: "애플 주식이 지금 살 만해?"

#### Turn 1
**Thought (사고):**
```
사용자가 애플 주식의 매수 적정성을 묻고 있다.
이를 판단하려면:
1. 현재 주가 확인
2. 재무 건전성 확인
3. 애널리스트 목표주가와 비교
4. 최근 뉴스/이슈 확인

먼저 현재 주가를 조회하자.
```

**Action:**
```json
{
    "tool": "search_realtime_stock_price",
    "parameters": {"ticker": "AAPL"}
}
```

**Observation:**
```json
{
    "current_price": 178.50,
    "change_percent": -1.2,
    "52w_high": 199.62,
    "52w_low": 164.08
}
```

---

#### Turn 2
**Thought:**
```
현재 178.50달러로, 52주 최고가(199.62) 대비 10.6% 낮다.
이제 재무 건전성을 확인해보자.
```

**Action:**
```json
{
    "tool": "search_financial_reports",
    "parameters": {"ticker": "AAPL"}
}
```

**Observation:**
```json
{
    "revenue_growth": 2.1,
    "operating_margin": 29.8,
    "debt_to_equity": 1.97,
    "roe": 160.5
}
```

---

#### Turn 3
**Thought:**
```
영업이익률 29.8%는 매우 우수하다 (일반적으로 10% 이상이면 양호).
ROE 160%는 자본 효율이 극히 높다.
이제 전문가 의견을 확인하자.
```

**Action:**
```json
{
    "tool": "search_analyst_targets",
    "parameters": {"ticker": "AAPL"}
}
```

**Observation:**
```json
{
    "target_price_avg": 195.30,
    "upside_potential": 9.4,
    "buy_ratings": 28,
    "hold_ratings": 10,
    "sell_ratings": 2
}
```

---

#### Turn 4
**Thought:**
```
애널리스트들은 평균 195.30달러 목표주가로, 9.4% 상승 여력을 보고 있다.
매수 의견이 28개로 압도적이다.
최근 이슈를 확인하고 최종 답변을 하자.
```

**Action:**
```json
{
    "tool": "search_news_and_issues",
    "parameters": {"query": "Apple AAPL"}
}
```

**Observation:**
```json
{
    "articles": [
        {
            "title": "Apple Vision Pro sales exceed expectations",
            "sentiment": "긍정"
        },
        {
            "title": "iPhone 16 demand weaker than expected in China",
            "sentiment": "부정"
        }
    ],
    "overall_sentiment": 0.3
}
```

---

#### Final Answer
**Thought:**
```
모든 정보를 종합했다. 이제 초보자가 이해하기 쉽게 답변하자.
```

**Final Answer (초보자용 번역):**
```
애플 주식 간단 분석 결과입니다.

✅ 좋은 점
• 현재 주가(178.50달러)가 52주 최고가 대비 10% 저렴해요
• 회사가 버는 돈(영업이익률 29.8%)이 업계 최상위 수준이에요
• 전문가 28명 중 28명이 '살 만하다'고 평가했어요
• 목표 주가는 195달러로, 9% 더 오를 가능성이 있어요

⚠️ 주의할 점
• 중국에서 아이폰 16 판매가 예상보다 약해요
• 최근 1.2% 하락했어요

💡 결론
재무적으로 매우 건강하고, 전문가들도 긍정적입니다.
다만 중국 시장 이슈는 지켜봐야 해요.
분할 매수(여러 번 나눠 사기)를 추천드려요.

⚠️ 이 정보는 참고용이며, 최종 투자 결정은 본인의 판단이 중요합니다.
```

---

## LangChain 구현 예시

### ReAct 에이전트 초기화
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

# LLM 초기화
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

# Tools 정의
tools = [
    Tool(
        name="search_realtime_stock_price",
        func=search_realtime_stock_price,
        description="지정된 종목의 실시간 주가를 조회합니다. 입력: ticker (예: 'AAPL')"
    ),
    Tool(
        name="search_financial_reports",
        func=search_financial_reports,
        description="기업의 재무제표(수익성, 안정성)를 조회합니다. 입력: ticker"
    ),
    Tool(
        name="search_analyst_targets",
        func=search_analyst_targets,
        description="증권사 애널리스트 목표주가를 조회합니다. 입력: ticker"
    ),
    Tool(
        name="search_news_and_issues",
        func=search_news_and_issues,
        description="최신 뉴스와 이슈를 검색합니다. 입력: query (키워드)"
    ),
    Tool(
        name="search_anomaly_detection",
        func=search_anomaly_detection,
        description="거래량 급증, 공매도 비율 등 이상 징후를 탐지합니다. 입력: ticker"
    )
]

# ReAct 프롬프트 템플릿
react_prompt = PromptTemplate.from_template("""
당신은 주식 초보자('주린이')를 위한 친절한 투자 가이드 AI입니다.

사용 가능한 도구:
{tools}

현재 질문: {input}

다음 형식으로 답변하세요:

Thought: 현재 상황을 분석하고 다음에 할 행동을 계획합니다.
Action: 사용할 도구 이름
Action Input: 도구에 전달할 파라미터
Observation: 도구 실행 결과

... (필요시 반복)

Thought: 최종 답변을 할 준비가 되었습니다.
Final Answer: 초보자가 이해하기 쉬운 언어로 답변합니다. 전문 용어는 괄호로 설명을 추가합니다.

{agent_scratchpad}
""")

# 에이전트 생성
agent = create_react_agent(llm, tools, react_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    early_stopping_method="generate"
)

# 실행
result = agent_executor.invoke({
    "input": "삼성전자 주식이 지금 살 만해?"
})
print(result["output"])
```

---

## RAG 구현 예시 (LlamaIndex)

### 벡터 스토어 구축
```python
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import PineconeVectorStore
from llama_index.embeddings import OpenAIEmbedding
import pinecone

# Pinecone 초기화
pinecone.init(api_key=settings.PINECONE_KEY, environment="us-west1-gcp")
index = pinecone.Index("stock-news")

# 뉴스 문서 임베딩 및 저장
async def index_news_articles(articles: List[str]):
    vector_store = PineconeVectorStore(pinecone_index=index)
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    service_context = ServiceContext.from_defaults(embed_model=embed_model)
    vector_index = VectorStoreIndex.from_documents(
        articles,
        service_context=service_context,
        vector_store=vector_store
    )
    return vector_index

# RAG 검색 및 답변 생성
async def rag_query(question: str):
    query_engine = vector_index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(question)

    # 인용 출처 포함
    sources = [node.metadata["source"] for node in response.source_nodes]
    return {
        "answer": response.response,
        "sources": sources
    }
```

---

## 환각 방지 체크리스트

1. ✅ **모든 데이터는 실제 API에서 조회**: 임의 생성 금지
2. ✅ **RAG로 문서 기반 답변**: "모르면 모른다"고 답변
3. ✅ **타임스탬프 명시**: "2024년 11월 17일 기준"
4. ✅ **신뢰도 점수 표시**: "이 정보는 3개 출처에서 확인됨"
5. ✅ **면책 조항 자동 삽입**: "참고용이며, 투자 판단은 본인 책임"

---

## 다음 단계

1. FastAPI 프로젝트 구조 생성
2. 각 Tool을 실제 API와 연동
3. LangChain Agent Executor 통합
4. Redis 캐싱 레이어 추가
5. 프론트엔드에서 사용할 REST API 엔드포인트 설계

---

**작성자**: AI 시스템 아키텍트
**작성일**: 2025-11-17
**문서 버전**: 1.0
