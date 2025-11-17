"""
ReAct Agent Executor
LangChain을 사용하여 추론-행동-관찰 사이클 구현
"""
from typing import Dict, Any, Optional
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from app.core.config import settings
from app.agents.tools import get_react_tools
from loguru import logger


# ReAct 프롬프트 템플릿 (초보자 친화적)
REACT_PROMPT_TEMPLATE = """
당신은 주식 초보자('주린이')를 위한 친절한 투자 가이드 AI입니다.

**핵심 원칙:**
1. 환각 방지: 모든 정보는 도구(Tools)로 얻은 실제 데이터만 사용합니다.
2. 초보자 언어: 전문 용어는 괄호로 쉽게 설명합니다.
3. 객관성: 단정적 추천보다는 "참고용 정보"임을 명시합니다.
4. 면책 조항: 최종 답변에 투자 책임은 본인에게 있음을 알립니다.

**사용 가능한 도구:**
{tools}

**도구 이름 목록:**
{tool_names}

**답변 형식:**
항상 다음 형식을 따르세요.

Thought: (한국어로 현재 상황을 분석하고 다음 행동을 계획)
Action: (도구 이름, 위 목록 중 하나 정확히 선택)
Action Input: (도구에 전달할 파라미터)
Observation: (도구 실행 결과가 여기 표시됨)

... (필요시 Thought/Action/Action Input/Observation 반복)

Thought: 최종 답변을 할 준비가 되었습니다.
Final Answer: (초보자가 이해하기 쉬운 한국어로 답변. 이모지 사용 가능. 반드시 출처와 면책 조항 포함)

**현재 질문:** {input}

**이전 대화 (있다면):**
{chat_history}

**생각 과정:**
{agent_scratchpad}
"""


class StockGuideAgent:
    """주식 가이드 ReAct 에이전트"""

    def __init__(self):
        """에이전트 초기화"""
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0,  # 환각 방지 위해 0으로 설정
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.tools = get_react_tools()
        self.prompt = PromptTemplate.from_template(REACT_PROMPT_TEMPLATE)
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,  # 개발 시 디버깅용
            max_iterations=6,  # 최대 6번 반복
            early_stopping_method="generate",
            handle_parsing_errors=True,
            return_intermediate_steps=True  # 중간 과정 반환
        )

        logger.info("StockGuideAgent initialized successfully")

    async def run(self, query: str, chat_history: str = "") -> Dict[str, Any]:
        """
        사용자 질문에 대해 ReAct 에이전트 실행

        Args:
            query: 사용자 질문
            chat_history: 이전 대화 기록 (선택)

        Returns:
            {
                "answer": "최종 답변",
                "intermediate_steps": [...],  # 중간 과정
                "tools_used": ["tool1", "tool2"]
            }
        """
        try:
            logger.info(f"Running agent for query: {query}")

            result = await self.agent_executor.ainvoke({
                "input": query,
                "chat_history": chat_history
            })

            # 사용된 도구 목록 추출
            tools_used = [
                step[0].tool for step in result.get("intermediate_steps", [])
            ]

            return {
                "answer": result["output"],
                "intermediate_steps": result.get("intermediate_steps", []),
                "tools_used": list(set(tools_used)),
                "success": True
            }

        except Exception as e:
            logger.error(f"Error in agent execution: {e}")
            return {
                "answer": f"죄송합니다. 처리 중 오류가 발생했습니다: {str(e)}",
                "intermediate_steps": [],
                "tools_used": [],
                "success": False,
                "error": str(e)
            }


# 싱글톤 인스턴스
_agent_instance: Optional[StockGuideAgent] = None


def get_agent() -> StockGuideAgent:
    """에이전트 싱글톤 인스턴스 반환"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = StockGuideAgent()
    return _agent_instance


# ===== 특화된 에이전트 함수들 =====

async def generate_company_diagnosis(ticker: str) -> Dict[str, Any]:
    """
    기업 건강진단서 생성 (ReAct 에이전트 활용)

    Args:
        ticker: 종목 코드

    Returns:
        건강진단서 JSON
    """
    agent = get_agent()

    query = f"""
{ticker} 기업의 건강진단서를 작성해주세요.

다음 항목을 반드시 포함해야 합니다:

**1. 기본 검진**
- 수익성: 영업이익률, ROE 등을 기반으로 평가 (상/중/하)
- 안정성: 부채비율, 당좌비율 등을 기반으로 평가
- 미래가치: 매출 성장률을 기반으로 평가

**2. 정밀 검진**
- CEO 평판/최근 이슈: 뉴스 검색으로 확인
- 투자자 관심: 외국인/기관 보유 비율
- 이상 징후: 거래량 급증, 공매도 비율 등

**3. 가격 매력도**
- 전문가 의견: 애널리스트 목표주가, 상승 여력
- 현재 주가: 52주 최고/최저 대비 위치

각 항목을 초보자가 이해하기 쉽게 설명하고, 최종적으로 종합 점수(100점 만점)를 부여해주세요.
"""

    result = await agent.run(query)
    return result


async def generate_daily_keyword() -> Dict[str, Any]:
    """
    오늘의 산업 키워드 생성 (매일 8시 50분 실행)

    Returns:
        {
            "keyword": "AI 반도체",
            "description": "...",
            "related_companies": [...],
            "sentiment": 0.7
        }
    """
    agent = get_agent()

    query = """
오늘의 가장 주목받는 산업 키워드 1개를 선정하고 설명해주세요.

절차:
1. 최근 뉴스에서 "technology trends", "market movers", "industry news" 등으로 검색
2. 가장 많이 언급되는 산업/기술 키워드 찾기
3. 해당 키워드와 관련된 주요 기업 3-5개 찾기
4. 초보자용 설명 작성 (왜 중요한지, 어떤 기회가 있는지)

답변 형식:
- 키워드: [선정된 키워드]
- 설명: [100자 이내 설명]
- 관련 기업: [티커, 회사명]
- 감성: [긍정/중립/부정]
"""

    result = await agent.run(query)
    return result


async def analyze_stock_for_beginners(ticker: str, user_question: str) -> Dict[str, Any]:
    """
    초보자를 위한 주식 분석 (자유 질문)

    Args:
        ticker: 종목 코드
        user_question: 사용자 질문 (예: "지금 살 만해?", "위험할까?")

    Returns:
        ReAct 에이전트 답변
    """
    agent = get_agent()

    query = f"""
{ticker} 주식에 대해 다음 질문에 답변해주세요: "{user_question}"

답변 시 유의사항:
1. 현재 주가, 재무 상태, 최근 뉴스 등을 종합적으로 고려
2. "좋은 점"과 "주의할 점"을 균형있게 제시
3. 초보자도 이해할 수 있는 언어 사용
4. 면책 조항 반드시 포함 ("이 정보는 참고용이며...")
"""

    result = await agent.run(query)
    return result
