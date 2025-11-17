# Netlify 배포 가이드

## 🚀 Netlify에 배포하기

### 방법 1: GitHub 연동 (권장)

#### 1단계: Netlify 계정 생성
1. https://www.netlify.com 접속
2. **"Sign up"** 클릭
3. GitHub 계정으로 로그인

#### 2단계: 새 사이트 생성
1. Netlify 대시보드에서 **"Add new site"** → **"Import an existing project"**
2. **"GitHub"** 선택
3. 저장소 선택: `your-username/git-practice` (또는 포크한 저장소)
4. 브랜치 선택: `main` 또는 `claude/stock-guide-app-ai-01X2Ep4EwxBmy4dakwRTitj8`

#### 3단계: 빌드 설정
```
Base directory: stock-guide-app/frontend
Build command: npm run build
Publish directory: stock-guide-app/frontend/dist
```

#### 4단계: 환경변수 설정 (선택)
**Site settings** → **Environment variables** → **Add a variable**

```
VITE_API_URL=demo
```

**또는 백엔드가 있다면:**
```
VITE_API_URL=https://your-backend.railway.app
```

#### 5단계: 배포
**"Deploy site"** 클릭!

---

## 방법 2: Netlify CLI 사용

### 설치
```bash
npm install -g netlify-cli
```

### 로그인
```bash
netlify login
```

### 배포
```bash
cd stock-guide-app/frontend

# 빌드
npm run build

# 배포
netlify deploy --prod --dir=dist
```

---

## 문제 해결

### 1. "Page Not Found" 오류
**원인:** SPA 라우팅 설정 누락

**해결:**
- `frontend/public/_redirects` 파일 확인
- 내용: `/*    /index.html   200`

---

### 2. 빈 화면 (Blank Screen)
**원인:** 빌드 경로 문제

**해결:**
```bash
# Netlify 설정 확인
Base directory: stock-guide-app/frontend
Publish directory: stock-guide-app/frontend/dist
```

---

### 3. API 호출 실패
**원인:** 백엔드 미연결

**해결 옵션:**

#### 옵션 A: 데모 모드 사용 (권장)
```
환경변수 없음 또는
VITE_API_URL=demo
```
→ 샘플 데이터로 UI 확인 가능

#### 옵션 B: 백엔드 연결
1. 백엔드를 Railway/Render에 배포
2. Netlify 환경변수 설정:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```

---

### 4. "Build Failed" 오류

**확인사항:**
```bash
# 로컬에서 빌드 테스트
cd stock-guide-app/frontend
npm install
npm run build

# 성공하면 dist/ 폴더 생성됨
```

**흔한 원인:**
- Node.js 버전 불일치 → Netlify에서 Node 18 사용 확인
- 패키지 설치 실패 → `package-lock.json` 커밋 확인

---

## 배포 후 확인사항

### ✅ 정상 작동 체크리스트

- [ ] 홈 화면이 보인다
- [ ] "오늘의 산업 키워드" 카드가 표시된다
- [ ] 검색창에 입력할 수 있다
- [ ] 인기 종목 버튼을 클릭하면 건강진단서로 이동한다
- [ ] 브라우저 뒤로가기가 작동한다

### ⚠️ 데모 모드일 때

상단에 노란색 배너가 표시됩니다:
```
⚠️ 데모 모드로 실행 중입니다. 표시되는 데이터는 샘플입니다.
```

이것은 **정상**입니다! 백엔드 없이도 UI를 확인할 수 있도록 한 것입니다.

---

## 실제 데이터 사용하기

### 백엔드 배포 (Railway 예시)

#### 1. Railway 계정 생성
https://railway.app

#### 2. 백엔드 배포
```bash
cd stock-guide-app/backend

# Railway CLI 설치
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 생성
railway init

# 환경변수 설정
railway variables set OPENAI_API_KEY=sk-...
railway variables set ALPHA_VANTAGE_API_KEY=...
# (나머지 API 키들)

# 배포
railway up
```

#### 3. URL 확인
```
https://your-app.up.railway.app
```

#### 4. Netlify에 연결
Netlify 환경변수 추가:
```
VITE_API_URL=https://your-app.up.railway.app
```

#### 5. Netlify 재배포
**Deploys** → **Trigger deploy** → **Deploy site**

---

## 커스텀 도메인 설정

### Netlify 무료 도메인
```
https://your-site-name.netlify.app
```

### 커스텀 도메인 연결
1. **Domain settings** → **Add custom domain**
2. 도메인 입력 (예: `stock-guide.com`)
3. DNS 설정 안내 따라하기
4. HTTPS 자동 활성화 (Let's Encrypt)

---

## 성능 최적화

### 1. 빌드 플러그인 추가
`netlify.toml`에 추가:
```toml
[[plugins]]
  package = "@netlify/plugin-lighthouse"

[[plugins]]
  package = "netlify-plugin-cache"
```

### 2. 헤더 설정
`frontend/public/_headers`:
```
/*
  Cache-Control: public, max-age=31536000, immutable

/index.html
  Cache-Control: no-cache
```

### 3. 리다이렉트 최적화
`frontend/public/_redirects`:
```
# SPA fallback
/*    /index.html   200

# 외부 API (프록시)
/api/*  https://your-backend.railway.app/api/:splat  200
```

---

## 모니터링

### Netlify Analytics (무료)
- 페이지 뷰
- 트래픽 소스
- 대역폭 사용량

### Netlify Functions (선택)
간단한 백엔드 로직을 Netlify에서 직접 실행:
```javascript
// netlify/functions/hello.js
exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello from Netlify!' })
  };
};
```

---

## 요금제

| 플랜 | 가격 | 대역폭 | 빌드 시간 |
|------|------|--------|-----------|
| **Free** | $0/월 | 100GB | 300분/월 |
| Starter | $19/월 | 1TB | 무제한 |
| Pro | $99/월 | 1TB | 무제한 |

**주식투자 가이드 앱**: Free 플랜으로 충분합니다!

---

## 자주 묻는 질문

### Q: 배포했는데 빈 화면만 보여요
**A:** 브라우저 개발자 도구(F12) → Console 탭 확인. 에러 메시지를 보고 해결하세요.

### Q: API 호출이 CORS 에러가 나요
**A:** 백엔드에서 CORS 설정 확인:
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-site.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Q: 환경변수를 바꿨는데 반영이 안 돼요
**A:** 환경변수 변경 후 반드시 재배포해야 합니다.
**Deploys** → **Trigger deploy** → **Clear cache and deploy site**

---

## 다음 단계

- [ ] Netlify에 배포 완료
- [ ] 커스텀 도메인 연결
- [ ] 백엔드 배포 (Railway/Render)
- [ ] 실제 API 키 발급 및 연결
- [ ] Analytics 모니터링

---

**축하합니다!** 🎉

앱이 이제 전 세계 어디서나 접속 가능합니다!

배포 URL: `https://your-site.netlify.app`
