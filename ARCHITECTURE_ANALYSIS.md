# 주식투자 가이드 앱 - Tree-of-Thought 기술 스택 분석

## 요구사항 요약
- **플랫폼**: PC, 모바일, 웹 크로스플랫폼 지원
- **타겟**: 주식 초보자('주린이')
- **핵심 기능**: 실시간 데이터 분석, 푸시 알림, 건강진단서 생성
- **성능 요구**: 빠른 응답 속도, 안정적인 알림, 실시간 데이터 처리

---

## 전략 1: PWA (React) + FastAPI + PostgreSQL

### 기술 스택 구성
- **프론트엔드**: React 18 + TypeScript + PWA (Service Worker)
- **백엔드**: Python FastAPI + LangChain (ReAct/RAG)
- **데이터베이스**: PostgreSQL + Redis (캐싱)
- **배포**: Vercel (Frontend) + Railway/Render (Backend)

### 평가

#### (1) 개발 속도: ⭐⭐⭐⭐⭐ (5/5)
- **장점**:
  - React PWA는 단일 코드베이스로 웹/모바일 동시 지원
  - FastAPI는 빠른 API 개발 가능 (자동 문서화)
  - Python 생태계로 AI/ML 라이브러리(LangChain, RAG) 즉시 활용
- **단점**:
  - iOS 푸시 알림은 제한적 (Web Push API 제약)

#### (2) 확장성: ⭐⭐⭐⭐ (4/5)
- **장점**:
  - FastAPI는 비동기 처리로 높은 동시성 지원
  - PostgreSQL은 복잡한 쿼리와 트랜잭션 안정적
  - Redis로 실시간 데이터 캐싱 가능
- **단점**:
  - Python은 Node.js 대비 속도가 약간 느릴 수 있음 (GIL 제약)

#### (3) 유지보수 비용: ⭐⭐⭐⭐⭐ (5/5)
- **장점**:
  - TypeScript로 타입 안정성 확보
  - FastAPI 자동 문서화로 API 관리 용이
  - 단일 코드베이스로 유지보수 포인트 최소화
- **단점**:
  - 없음

#### (4) 실시간 데이터 처리 성능: ⭐⭐⭐⭐ (4/5)
- **장점**:
  - Redis 캐싱으로 주가 데이터 빠른 응답
  - WebSocket 지원으로 실시간 업데이트 가능
  - LangChain ReAct 에이전트로 지능형 데이터 분석
- **단점**:
  - Python GIL로 인한 멀티스레드 제약

---

## 전략 2: React Native + Node.js (Express) + MongoDB

### 기술 스택 구성
- **프론트엔드**: React Native (Expo) + TypeScript
- **백엔드**: Node.js Express + LangChain.js
- **데이터베이스**: MongoDB Atlas + Redis
- **배포**: Expo (Mobile) + AWS EC2 (Backend)

### 평가

#### (1) 개발 속도: ⭐⭐⭐ (3/5)
- **장점**:
  - React Native로 iOS/Android 네이티브 앱 개발
  - JavaScript 풀스택으로 언어 통일
- **단점**:
  - 웹 지원을 위해 별도 React 웹 프로젝트 필요 (코드 중복)
  - Expo의 네이티브 모듈 제약 가능성

#### (2) 확장성: ⭐⭐⭐⭐ (4/5)
- **장점**:
  - Node.js 이벤트 루프로 높은 동시성
  - MongoDB NoSQL로 스키마 유연성
- **단점**:
  - MongoDB는 복잡한 관계형 쿼리에 비효율적
  - 트랜잭션 처리가 PostgreSQL 대비 약함

#### (3) 유지보수 비용: ⭐⭐⭐ (3/5)
- **장점**:
  - JavaScript 단일 언어로 학습 곡선 낮음
- **단점**:
  - 웹/모바일 코드베이스 분리로 유지보수 포인트 증가
  - React Native 버전 업데이트 시 호환성 이슈 빈번

#### (4) 실시간 데이터 처리 성능: ⭐⭐⭐⭐⭐ (5/5)
- **장점**:
  - Node.js는 실시간 처리에 최적화
  - Socket.io로 실시간 푸시 쉽게 구현
  - LangChain.js도 ReAct/RAG 지원
- **단점**:
  - 없음

---

## 전략 3: Flutter + Django REST + PostgreSQL

### 기술 스택 구성
- **프론트엔드**: Flutter (Dart) - Web/iOS/Android
- **백엔드**: Django REST Framework + Celery (작업 큐)
- **데이터베이스**: PostgreSQL + Redis
- **배포**: Firebase Hosting (Web) + AWS ECS (Backend)

### 평가

#### (1) 개발 속도: ⭐⭐⭐ (3/5)
- **장점**:
  - Flutter 단일 코드로 웹/iOS/Android 완벽 지원
  - Django는 강력한 ORM과 Admin 기능 제공
- **단점**:
  - Dart 언어 학습 필요
  - Django는 FastAPI 대비 보일러플레이트 코드 많음
  - AI/ML 통합 시 FastAPI보다 복잡

#### (2) 확장성: ⭐⭐⭐⭐ (4/5)
- **장점**:
  - Django는 대규모 앱에 검증된 프레임워크
  - Celery로 백그라운드 작업 처리 우수
- **단점**:
  - 동기 방식 기본이라 비동기 처리는 별도 설정 필요

#### (3) 유지보수 비용: ⭐⭐⭐⭐ (4/5)
- **장점**:
  - Flutter 단일 코드베이스로 일관성 유지
  - Django의 강력한 보안 및 테스트 도구
- **단점**:
  - Dart 생태계가 JavaScript/Python 대비 작음

#### (4) 실시간 데이터 처리 성능: ⭐⭐⭐ (3/5)
- **장점**:
  - Redis + Celery로 비동기 작업 처리
- **단점**:
  - Django는 기본적으로 동기 방식
  - WebSocket은 Django Channels 추가 설정 필요

---

## 최종 선택: 전략 1 (PWA + FastAPI + PostgreSQL)

### 선택 이유

#### 1. 초보자 중심 UX에 최적화
- **PWA의 접근성**: 앱 설치 없이 브라우저에서 즉시 사용 가능
  - 주린이들이 "앱 다운로드" 장벽 없이 바로 시작
  - 나중에 "홈 화면에 추가"로 네이티브 앱처럼 사용 가능
- **크로스플랫폼 완벽 지원**: 단일 코드로 PC/모바일/태블릿 모두 대응

#### 2. AI 에이전트(ReAct + RAG) 구현의 용이성
- **Python 생태계 강점**:
  - LangChain, LlamaIndex 등 최신 AI 프레임워크 네이티브 지원
  - OpenAI API, HuggingFace 모델 즉시 통합 가능
  - RAG 구현 시 벡터 DB(Pinecone, Weaviate) 연동 쉬움
- **FastAPI의 비동기 성능**: AI 추론 시간이 긴 작업도 효율적 처리

#### 3. 개발 속도 및 비용 효율성
- **MVP 빠른 출시**:
  - React PWA는 1-2주 내 프로토타입 가능
  - FastAPI 자동 문서화로 API 개발/테스트 동시 진행
- **무료/저렴한 배포 옵션**:
  - Vercel(Frontend): 무료 티어
  - Render/Railway(Backend): 무료~$5/월
  - Supabase(PostgreSQL): 무료 티어

#### 4. 실시간 데이터 처리 전략
- **Redis 캐싱 레이어**:
  - 주가 데이터를 1분 단위로 캐싱 → API 호출 비용 절감
  - 건강진단서 결과를 10분간 캐싱 → 중복 계산 방지
- **WebSocket + Server-Sent Events**:
  - 관심 목록의 급등/급락 알림을 실시간 푸시
- **백그라운드 작업**:
  - Celery 대신 FastAPI BackgroundTasks로 경량화
  - 매일 8:50 "오늘의 키워드" 크론잡 실행

#### 5. 유지보수 및 확장성
- **TypeScript + Python**:
  - 프론트/백 모두 강력한 타입 시스템
  - IDE 자동완성으로 개발 생산성 향상
- **모듈화된 구조**:
  - React 컴포넌트 재사용
  - FastAPI의 라우터/의존성 주입으로 깔끔한 아키텍처

#### 6. 주요 단점 해결 방안
- **iOS 푸시 알림 제약**:
  - 초기 버전은 Web Push API 활용
  - 사용자 증가 시 React Native 래퍼 추가 검토
- **Python GIL 제약**:
  - 대부분의 작업이 I/O 바운드(API 호출)라 영향 적음
  - CPU 집약적 작업은 Rust/Go 마이크로서비스로 분리 가능

---

## 최종 기술 스택 상세

### 프론트엔드
```
- React 18.3+ (Vite 빌드 도구)
- TypeScript 5.0+
- TailwindCSS (스타일링)
- Zustand (상태 관리 - Redux보다 경량)
- React Query (서버 상태 관리)
- Chart.js (주가 차트)
- Workbox (Service Worker/PWA)
```

### 백엔드
```
- Python 3.11+
- FastAPI 0.104+
- LangChain 0.1+ (ReAct 에이전트)
- LlamaIndex (RAG 구현)
- Pydantic v2 (데이터 검증)
- SQLAlchemy 2.0 (ORM)
- Alembic (마이그레이션)
- APScheduler (크론 작업)
```

### 데이터베이스 & 인프라
```
- PostgreSQL 15+ (주 데이터베이스)
- Redis 7+ (캐싱 + 세션)
- Pinecone/Qdrant (벡터 DB - RAG용)
- Docker Compose (로컬 개발 환경)
```

### 외부 API/서비스
```
- OpenAI API (GPT-4 Turbo - 건강진단서 생성)
- Alpha Vantage / Yahoo Finance API (주가 데이터)
- News API (뉴스 검색)
- Firebase Cloud Messaging (푸시 알림)
```

---

## 아키텍처 다이어그램 (개념도)

```
[사용자 브라우저/PWA]
         ↓↑ (HTTPS/WSS)
    [Nginx/Caddy]
         ↓↑
  [FastAPI 서버]
    ├── /api/v1/keywords (오늘의 키워드)
    ├── /api/v1/diagnosis (건강진단서)
    ├── /api/v1/watchlist (관심 목록)
    └── /ws/alerts (실시간 알림)
         ↓↑
   [ReAct 에이전트 레이어]
    ├── Tool: search_stock_price()
    ├── Tool: search_financials()
    ├── Tool: search_news()
    └── RAG: 벡터 검색 → LLM 합성
         ↓↑
  [데이터 레이어]
    ├── PostgreSQL (사용자/관심목록)
    ├── Redis (캐싱)
    └── Pinecone (벡터 임베딩)
         ↓↑
  [외부 API]
    ├── Alpha Vantage (주가)
    ├── News API (뉴스)
    └── OpenAI API (LLM)
```

---

## 다음 단계

1. **프로젝트 구조 생성**: 모노레포 vs 폴리레포 결정
2. **ReAct 에이전트 설계**: Tools 정의 및 Reasoning Loop 구현
3. **프로토타입 개발**: 핵심 기능 1개(건강진단서)로 MVP 검증
4. **Self-Reflection**: 코드 리뷰 및 UX 개선

---

**작성자**: AI 시스템 아키텍트
**작성일**: 2025-11-17
**문서 버전**: 1.0
