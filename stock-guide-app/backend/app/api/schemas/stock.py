"""
Pydantic Schemas for API Request/Response
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ===== 요청 스키마 =====

class StockQuery(BaseModel):
    """주식 분석 요청"""
    ticker: str = Field(..., description="종목 코드 (예: AAPL, 005930.KS)")
    question: Optional[str] = Field(None, description="사용자 질문 (선택)")


class WatchlistAdd(BaseModel):
    """관심 목록 추가"""
    ticker: str
    company_name: str
    memo: Optional[str] = None


class WatchlistUpdate(BaseModel):
    """관심 목록 업데이트"""
    memo: Optional[str] = None


# ===== 응답 스키마 =====

class StockPriceResponse(BaseModel):
    """실시간 주가 응답"""
    ticker: str
    current_price: float
    change_percent: float
    volume: int
    timestamp: str


class DiagnosisResponse(BaseModel):
    """건강진단서 응답"""
    ticker: str
    company_name: str
    profitability_score: float
    stability_score: float
    future_value_score: float
    summary_for_beginners: str
    analyst_target_price: Optional[float] = None
    upside_potential: Optional[float] = None
    generated_at: datetime


class KeywordResponse(BaseModel):
    """오늘의 키워드 응답"""
    keyword: str
    description: str
    related_companies: List[Dict[str, str]]
    sentiment_score: float
    date: datetime


class WatchlistItem(BaseModel):
    """관심 목록 항목"""
    id: int
    ticker: str
    company_name: str
    memo: Optional[str]
    current_price: Optional[float]
    change_percent: Optional[float]
    added_at: datetime


class AgentResponse(BaseModel):
    """ReAct 에이전트 응답"""
    answer: str
    tools_used: List[str]
    success: bool
    intermediate_steps: Optional[List[Any]] = None
