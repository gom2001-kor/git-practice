"""
FastAPI Main Application
주식투자 가이드 백엔드 서버
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.routes import stock, watchlist
from loguru import logger
import sys

# 로거 설정
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO" if not settings.DEBUG else "DEBUG"
)


# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="주식 초보자를 위한 AI 기반 투자 가이드 API",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)


# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(stock.router)
app.include_router(watchlist.router)


# 헬스 체크
@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# 루트 엔드포인트
@app.get("/")
async def root():
    """API 루트"""
    return {
        "message": "주식투자 가이드 API에 오신 것을 환영합니다!",
        "docs": "/docs" if settings.DEBUG else "문서는 비공개입니다",
        "version": settings.APP_VERSION
    }


# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# 시작 이벤트
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # TODO: 데이터베이스 연결
    # TODO: Redis 연결
    # TODO: Pinecone 연결
    # TODO: APScheduler 크론잡 시작 (매일 8:50 키워드 생성)


# 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    # TODO: 데이터베이스 연결 종료
    # TODO: Redis 연결 종료


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
