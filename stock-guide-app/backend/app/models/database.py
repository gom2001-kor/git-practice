"""
Database Models
SQLAlchemy 2.0 async style
"""
from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, Boolean, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional, Dict, Any


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class User(Base):
    """사용자 테이블 (향후 확장용)"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Watchlist(Base):
    """관심 목록 (찜하기)"""
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)  # FK to users
    ticker: Mapped[str] = mapped_column(String(20), index=True)  # 종목 코드
    company_name: Mapped[str] = mapped_column(String(255))
    memo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 사용자 메모
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 캐싱된 현재가 정보 (정기 업데이트)
    current_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    change_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class DailyKeyword(Base):
    """오늘의 산업 키워드"""
    __tablename__ = "daily_keywords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, index=True, unique=True)
    keyword: Mapped[str] = mapped_column(String(100))  # 예: "AI 반도체"
    description: Mapped[str] = mapped_column(Text)  # 초보자용 설명
    related_companies: Mapped[Dict[str, Any]] = mapped_column(JSON)  # {"tickers": ["NVDA", "AMD"], "names": [...]}
    sentiment_score: Mapped[float] = mapped_column(Float)  # -1.0 ~ 1.0
    source_articles: Mapped[Dict[str, Any]] = mapped_column(JSON)  # 출처 뉴스
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CompanyDiagnosis(Base):
    """기업 건강진단서 캐시"""
    __tablename__ = "company_diagnosis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    company_name: Mapped[str] = mapped_column(String(255))

    # 기본 검진
    profitability_score: Mapped[float] = mapped_column(Float)  # 수익성 점수 (0-100)
    stability_score: Mapped[float] = mapped_column(Float)  # 안정성 점수
    future_value_score: Mapped[float] = mapped_column(Float)  # 미래가치 점수

    # 정밀 검진
    ceo_reputation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ownership_data: Mapped[Dict[str, Any]] = mapped_column(JSON)  # 외국인/기관 비율
    anomaly_flags: Mapped[Dict[str, Any]] = mapped_column(JSON)  # 이상 징후

    # 가격 매력도
    analyst_target_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    upside_potential: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # 초보자용 요약
    summary_for_beginners: Mapped[str] = mapped_column(Text)  # AI 생성 요약

    # 메타데이터
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime)  # 10분 후 만료


class Alert(Base):
    """사용자 알림 로그"""
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    ticker: Mapped[str] = mapped_column(String(20))
    alert_type: Mapped[str] = mapped_column(String(50))  # "volume_spike", "news", "price_change"
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
