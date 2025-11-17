# 빠른 시작 가이드

## 🚀 5분 안에 실행하기

### 사전 준비
1. **Node.js 설치** (https://nodejs.org - LTS 버전)
2. **Python 3.11+ 설치** (https://www.python.org/downloads/)
3. **Git 설치** (선택)

---

## 방법 1: 프론트엔드만 실행 (데모 모드)

백엔드 없이 UI만 확인하려면:

```bash
# 1. 프론트엔드 폴더로 이동
cd stock-guide-app/frontend

# 2. 패키지 설치 (최초 1회만)
npm install

# 3. 개발 서버 실행
npm run dev
```

**결과:**
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

브라우저에서 **http://localhost:3000** 열기

⚠️ **주의**: 백엔드가 없어서 데이터 조회는 작동하지 않습니다.

---

## 방법 2: 백엔드 + 프론트엔드 전체 실행

### 2-1. 백엔드 실행

```bash
# 1. 백엔드 폴더로 이동
cd stock-guide-app/backend

# 2. 가상환경 생성 (최초 1회만)
python -m venv venv

# 3. 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. 패키지 설치 (최초 1회만)
pip install -r requirements.txt

# 5. 환경변수 설정
cp .env.example .env

# .env 파일을 메모장으로 열어서 아래 필수 항목만 입력:
# OPENAI_API_KEY=sk-your-key-here (선택)
# SECRET_KEY=any-random-string-here (필수)
# 나머지는 임시로 "test" 입력해도 됨

# 6. 서버 실행
uvicorn app.main:app --reload --port 8000
```

**성공 메시지:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**API 문서 확인:** http://localhost:8000/docs

### 2-2. 프론트엔드 실행 (새 터미널)

```bash
# 1. 프론트엔드 폴더로 이동
cd stock-guide-app/frontend

# 2. 패키지 설치 (최초 1회만)
npm install

# 3. 개발 서버 실행
npm run dev
```

**브라우저에서 열기:** http://localhost:3000

---

## 방법 3: Docker로 한 번에 실행 (가장 쉬움)

**Docker Desktop 설치 후:**

```bash
cd stock-guide-app

# 환경변수 설정
cp backend/.env.example backend/.env
# backend/.env 파일 편집 (위와 동일)

# 실행
docker-compose up
```

**접속:**
- 프론트엔드: http://localhost:3000
- 백엔드: http://localhost:8000

**종료:** `Ctrl + C` 누르고 `docker-compose down`

---

## 문제 해결

### "npm: command not found"
→ Node.js 미설치. https://nodejs.org 에서 설치

### "python: command not found"
→ Python 미설치. https://python.org 에서 설치

### "포트 3000이 이미 사용 중"
```bash
# 다른 포트로 실행
npm run dev -- --port 3001
```

### "포트 8000이 이미 사용 중"
```bash
# 다른 포트로 실행
uvicorn app.main:app --reload --port 8001
```

### "Module not found 에러"
```bash
# 패키지 재설치
rm -rf node_modules package-lock.json
npm install
```

---

## 최소 실행 환경 (API 키 없이)

API 키가 없어도 UI는 확인 가능합니다:

### backend/.env
```env
SECRET_KEY=test-secret-key-12345
DATABASE_URL=sqlite:///./test.db
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=test
ALPHA_VANTAGE_API_KEY=test
FMP_API_KEY=test
NEWS_API_KEY=test
PINECONE_API_KEY=test
PINECONE_ENVIRONMENT=test
```

**주의:** 실제 데이터는 조회되지 않지만 UI 확인은 가능합니다.

---

## 실제 데이터 사용을 위한 API 키 발급

### 1. OpenAI (GPT-4)
- https://platform.openai.com/api-keys
- 신용카드 등록 필요 ($5-20/월)

### 2. Alpha Vantage (주가 데이터)
- https://www.alphavantage.co/support/#api-key
- **무료** (1일 500 요청)

### 3. Financial Modeling Prep (재무 데이터)
- https://site.financialmodelingprep.com/developer/docs/
- **무료** (1일 250 요청)

### 4. News API
- https://newsapi.org/register
- **무료** (1일 100 요청)

### 5. Pinecone (벡터 DB)
- https://www.pinecone.io/
- **무료** (Starter 플랜)

---

## 빠른 체크리스트

- [ ] Node.js 설치 완료
- [ ] Python 3.11+ 설치 완료
- [ ] `cd stock-guide-app/frontend && npm install` 실행
- [ ] `cd stock-guide-app/backend && pip install -r requirements.txt` 실행
- [ ] `backend/.env` 파일 생성 및 설정
- [ ] 백엔드 실행: `uvicorn app.main:app --reload`
- [ ] 프론트엔드 실행: `npm run dev`
- [ ] 브라우저에서 http://localhost:3000 열기

---

**도움이 필요하면 이슈를 남겨주세요!**
