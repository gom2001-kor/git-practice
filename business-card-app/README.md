# 디지털 명함 앱 (Digital Business Card PWA)

모바일과 데스크톱에서 사용할 수 있는 Progressive Web App 기반 디지털 명함 애플리케이션입니다.

## 주요 기능

### 1. 명함 생성 및 관리
- 사진, 이름, 주소 등 기본 정보 입력
- 전화번호, 이메일, 웹사이트, FAX 번호를 동적으로 추가 (각 최대 3개)
- 각 필드에 라벨 지정 가능 (예: "회사", "개인", "본사" 등)
- 10가지 템플릿 선택
- 2가지 색상 테마 (파란색, 핑크색)
- 공개 범위 설정 (전체 공개, 링크만, 비공개)

### 2. 명함 상호작용
- 📞 전화번호 클릭 → 전화 앱 실행
- 📧 이메일 클릭 → 클립보드 복사
- 🌐 웹사이트 클릭 → 브라우저 실행
- 📍 주소 클릭 → 지도 앱 실행
- 📠 FAX 클릭 → 클립보드 복사

### 3. QR 코드 및 공유
- QR 코드 생성 및 표시
- 다양한 방법으로 명함 공유 (카카오톡, 문자, 이메일 등)
- 웹 브라우저에서 명함 조회 (앱 설치 불필요)

### 4. 명함첩
- 받은 명함 저장 및 관리
- 이름으로 검색

### 5. 인증 시스템
- 익명 인증으로 즉시 시작
- 선택적으로 구글 계정 연동 가능
- 다른 기기에서도 동일한 데이터 접근 (계정 연동 시)

### 6. 다국어 지원
- 한국어 (기본)
- English
- 中文 (중국어)
- 日本語 (일본어)

### 7. PWA 기능
- 홈 화면에 앱 설치 가능
- 오프라인 지원
- 빠른 로딩 속도

## 기술 스택

### Frontend
- **React** - UI 라이브러리
- **Vite** - 빌드 도구
- **React Router** - 라우팅
- **i18next** - 다국어 지원
- **qrcode.react** - QR 코드 생성

### Backend
- **Firebase Authentication** - 익명 인증 및 구글 로그인
- **Cloud Firestore** - 데이터베이스
- **Firebase Storage** - 이미지 저장
- **Firebase Hosting** - 웹 호스팅

### PWA
- **vite-plugin-pwa** - PWA 기능
- **Workbox** - 서비스 워커 및 캐싱

## 시작하기

### 1. 저장소 클론

\`\`\`bash
git clone <repository-url>
cd business-card-app
\`\`\`

### 2. 의존성 설치

\`\`\`bash
npm install
\`\`\`

### 3. Firebase 프로젝트 설정

1. [Firebase Console](https://console.firebase.google.com/)에서 새 프로젝트 생성
2. 웹 앱 추가
3. Firebase 설정 정보 복사
4. \`src/services/firebase.js\` 파일에서 Firebase 설정 업데이트:

\`\`\`javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
\`\`\`

### 4. Firebase 서비스 활성화

Firebase Console에서 다음 서비스들을 활성화하세요:

#### Authentication
1. Authentication > Sign-in method
2. 익명 (Anonymous) 활성화
3. Google 활성화 (선택사항)

#### Firestore Database
1. Firestore Database 생성
2. 테스트 모드로 시작 (나중에 보안 규칙 추가)
3. 보안 규칙 설정:

\`\`\`
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Cards collection
    match /cards/{cardId} {
      // Anyone can read public cards
      allow read: if resource.data.privacy == 'public'
                  || request.auth.uid == resource.data.userId;

      // Only owner can write
      allow write: if request.auth.uid == resource.data.userId;
    }

    // Collections
    match /collections/{collectionId} {
      allow read, write: if request.auth.uid == resource.data.userId;
    }
  }
}
\`\`\`

#### Storage
1. Storage 활성화
2. 보안 규칙 설정:

\`\`\`
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /photos/{userId}/{fileName} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
\`\`\`

### 5. 개발 서버 실행

\`\`\`bash
npm run dev
\`\`\`

앱이 http://localhost:3000 에서 실행됩니다.

### 6. 프로덕션 빌드

\`\`\`bash
npm run build
\`\`\`

빌드된 파일은 \`dist\` 폴더에 생성됩니다.

### 7. Firebase Hosting 배포

1. Firebase CLI 설치:
\`\`\`bash
npm install -g firebase-tools
\`\`\`

2. Firebase 로그인:
\`\`\`bash
firebase login
\`\`\`

3. Firebase 프로젝트 초기화:
\`\`\`bash
firebase init hosting
\`\`\`
- Public directory: \`dist\`
- Single-page app: Yes
- GitHub 자동 배포: 선택사항

4. 배포:
\`\`\`bash
npm run build
firebase deploy
\`\`\`

## 프로젝트 구조

\`\`\`
business-card-app/
├── public/                 # 정적 파일
├── src/
│   ├── components/        # 재사용 가능한 컴포넌트
│   │   ├── BottomNav.jsx
│   │   ├── BusinessCardPreview.jsx
│   │   └── DynamicFieldEditor.jsx
│   ├── screens/          # 화면 컴포넌트
│   │   ├── HomeScreen.jsx
│   │   ├── CreateCardScreen.jsx
│   │   ├── CardDetailScreen.jsx
│   │   ├── CardCollectionScreen.jsx
│   │   ├── SettingsScreen.jsx
│   │   └── ViewCardScreen.jsx
│   ├── services/         # 서비스 레이어
│   │   └── firebase.js
│   ├── models/           # 데이터 모델
│   │   └── BusinessCard.js
│   ├── utils/            # 유틸리티 함수
│   │   └── helpers.js
│   ├── i18n/             # 다국어 설정
│   │   └── config.js
│   ├── App.jsx           # 메인 앱 컴포넌트
│   ├── main.jsx          # 엔트리 포인트
│   └── index.css         # 전역 스타일
├── index.html
├── vite.config.js        # Vite 설정
└── package.json
\`\`\`

## 사용 방법

### 명함 만들기
1. 홈 화면에서 '+' 버튼 클릭
2. 사진 업로드
3. 이름, 주소 등 기본 정보 입력
4. 필요한 필드 추가 (전화, 이메일, 웹사이트, FAX)
5. 템플릿 및 색상 테마 선택
6. 공개 범위 설정
7. 저장

### 명함 공유하기
1. 명함 상세 화면에서 '명함 공유' 버튼 클릭
2. 공유 방법 선택 (카카오톡, 문자, 이메일 등)
3. 또는 QR 코드 표시하여 스캔

### 받은 명함 저장
1. 명함 링크 또는 QR 코드로 접근
2. 명함 정보 확인
3. '명함첩에 저장' 버튼 클릭 (앱 설치 필요)

## 주의사항

- Firebase 무료 플랜(Spark Plan) 한도:
  - 스토리지: 1GB
  - 다운로드: 10GB/월
  - Firestore 읽기: 50,000회/일
  - Firestore 쓰기: 20,000회/일

- 프로덕션 환경에서는 반드시 Firebase 보안 규칙을 설정하세요.
- 이미지는 자동으로 압축되지만, 용량 관리에 주의하세요.

## 향후 개발 계획

- [ ] 명함 템플릿 추가 디자인
- [ ] 명함 분석 기능 (조회수, 클릭 통계)
- [ ] 오프라인 QR 스캔 기능
- [ ] 애플 로그인 추가
- [ ] 명함 백업 및 내보내기
- [ ] 다크 모드 지원
- [ ] 위젯 지원

## 라이선스

MIT

## 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.
