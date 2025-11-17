# 주식투자 가이드 - AI 기반 주린이 투자 가이드 앱

## 프로젝트 개요

**주식투자 가이드**는 주식 지식이 전무한 초보자('주린이')를 위한 AI 기반 투자 정보 제공 앱입니다.

### 핵심 특징
- **ReAct (Reasoning + Acting) AI 에이전트**: 스스로 추론하고 도구를 사용하여 객관적인 분석 제공
- **RAG (Retrieval-Augmented Generation)**: 환각 방지, 실제 데이터 기반 답변만 제공
- **초보자 친화적 UI/UX**: PWA로 앱 설치 장벽 제거, 쉬운 언어로 번역
- **크로스플랫폼**: PC, 모바일, 태블릿 모두 지원

---

## 기술 스택

### 백엔드
- **Python 3.11+** + **FastAPI**
- **LangChain** (ReAct Agent)
- **OpenAI GPT-4 Turbo**
- **PostgreSQL** (사용자 데이터)
- **Redis** (캐싱)
- **Pinecone** (벡터 DB for RAG)

### 프론트엔드
- **React 18** + **TypeScript**
- **Vite** (빌드 도구)
- **TailwindCSS** (스타일링)
- **PWA** (Service Worker)
- **Zustand** (상태 관리)

### 외부 API
- **Alpha Vantage**: 실시간 주가
- **Financial Modeling Prep (FMP)**: 재무제표, 애널리스트 의견
- **News API**: 뉴스 검색

---

## 주요 기능

### 1. 오늘의 산업 키워드
- 매일 아침 9시, AI가 선정한 가장 주목받는 산업 키워드
- 관련 기업 목록 및 초보자용 설명 제공

### 2. 기업 건강진단서 2.0
- **기본 검진**: 수익성, 안정성, 미래가치
- **정밀 검진**: CEO 평판, 투자자 수급, 이상 징후
- **가격 매력도**: 전문가 목표주가, 잠재 수익률

### 3. 관심 목록 (찜하기)
- 관심 기업을 저장하고 메모 작성
- 실시간 주가 및 등락률 표시
- 이상 징후 발생 시 푸시 알림

---

## 아키텍처

```
[React PWA]
   ↓ HTTPS
[FastAPI Backend]
   ↓
[ReAct Agent] ← [5개 Tools]
   ├─ search_realtime_stock_price()
   ├─ search_financial_reports()
   ├─ search_analyst_targets()
   ├─ search_news_and_issues()
   └─ search_anomaly_detection()
   ↓
[외부 API] + [PostgreSQL] + [Redis] + [Pinecone]
```

---

## 설치 및 실행

### 사전 요구사항
- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **Redis 7+**

### 1. 저장소 클론
```bash
git clone https://github.com/your-repo/stock-guide-app.git
cd stock-guide-app
```

### 2. 백엔드 설정
```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어 API 키 입력:
# - OPENAI_API_KEY
# - ALPHA_VANTAGE_API_KEY
# - FMP_API_KEY
# - NEWS_API_KEY
# - PINECONE_API_KEY

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

### 3. 프론트엔드 설정
```bash
cd frontend

# 의존성 설치
npm install

# 환경변수 설정
cp .env.example .env

# 개발 서버 실행
npm run dev
```

### 4. 접속
- **프론트엔드**: http://localhost:3000
- **백엔드 API 문서**: http://localhost:8000/docs

---

## API 엔드포인트

### 주식 분석
```
POST /api/v1/stock/analyze
{
  "ticker": "AAPL",
  "question": "지금 살 만해?"
}
```

### 건강진단서
```
GET /api/v1/stock/diagnosis/{ticker}
```

### 오늘의 키워드
```
GET /api/v1/stock/daily-keyword
```

### 관심 목록
```
GET /api/v1/watchlist/
POST /api/v1/watchlist/
DELETE /api/v1/watchlist/{item_id}
```

---

## 프로젝트 구조

```
stock-guide-app/
├── backend/
│   ├── app/
│   │   ├── agents/          # ReAct 에이전트
│   │   │   ├── tools.py     # 5개 도구 구현
│   │   │   └── react_agent.py
│   │   ├── api/
│   │   │   ├── routes/      # FastAPI 라우터
│   │   │   └── schemas/     # Pydantic 스키마
│   │   ├── core/            # 설정, 보안
│   │   ├── models/          # 데이터베이스 모델
│   │   └── main.py          # FastAPI 앱
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React 컴포넌트
│   │   │   ├── Home.tsx
│   │   │   ├── Diagnosis.tsx
│   │   │   └── Watchlist.tsx
│   │   ├── api/             # API 클라이언트
│   │   ├── store/           # Zustand 상태 관리
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── ARCHITECTURE_ANALYSIS.md  # Tree-of-Thought 분석
├── REACT_AGENT_DESIGN.md     # ReAct 에이전트 설계
├── SELF_REFLECTION.md        # 비평적 검토 및 개선안
└── README.md
```

---

## 환경변수 설정

### 백엔드 (.env)
```env
# OpenAI
OPENAI_API_KEY=sk-...

# 주식 데이터 API
ALPHA_VANTAGE_API_KEY=your-key
FMP_API_KEY=your-key
NEWS_API_KEY=your-key

# 벡터 DB
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=us-west1-gcp

# 데이터베이스
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/stock_guide
REDIS_URL=redis://localhost:6379/0
```

### 프론트엔드 (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 테스트

### 백엔드 테스트
```bash
cd backend
pytest tests/ -v --cov=app
```

### 프론트엔드 테스트
```bash
cd frontend
npm run test
```

---

## 배포

### 백엔드 (Railway / Render)
```bash
# Dockerfile 사용
docker build -t stock-guide-backend .
docker run -p 8000:8000 stock-guide-backend
```

### 프론트엔드 (Vercel)
```bash
npm run build
# dist/ 폴더를 Vercel에 배포
```

---

## 주요 문서

1. **[ARCHITECTURE_ANALYSIS.md](./ARCHITECTURE_ANALYSIS.md)**: Tree-of-Thought 기술 스택 분석
2. **[REACT_AGENT_DESIGN.md](./REACT_AGENT_DESIGN.md)**: ReAct 에이전트 상세 설계
3. **[SELF_REFLECTION.md](./SELF_REFLECTION.md)**: 비평적 검토 및 개선안

---

## 라이선스

MIT License

---

## 기여

이슈 및 PR은 언제나 환영합니다!

---

## 문의

프로젝트 관련 문의: your-email@example.com

---

**작성일**: 2025-11-17
**버전**: 1.0.0
