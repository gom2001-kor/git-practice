# Changelog

All notable changes to ScreenOCR will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-22

### Added
- 전체 화면 캡처 기능
- Tesseract OCR을 사용한 텍스트 추출
- 다국어 지원 (한국어, 영어, 일본어, 중국어 번체)
- 이미지 전처리 (대비 향상, 샤프닝)
- 스페이스바 전역 핫키로 캡처
- ESC 키로 앱 종료
- 항상 최상위 표시되는 메인 윈도우
- 드래그 가능한 UI
- 저장 다이얼로그 (이미지 + 텍스트 미리보기)
- 자동 파일명 생성 (타임스탬프)
- 멀티모니터 지원
- 로깅 시스템
- PyInstaller를 통한 단일 실행 파일 빌드

### Features
- **UI/UX**
  - 간편한 우측 상단 실행창 (150x120px)
  - 반투명 배경 (90%)
  - 둥근 모서리 디자인
  - 직관적인 저장 다이얼로그

- **OCR**
  - 자동 이미지 전처리
  - CLAHE 대비 향상
  - 샤프닝 필터
  - 4개 언어 동시 인식

- **파일 관리**
  - PNG 이미지 (원본 화질)
  - TXT 텍스트 (UTF-8, 메타데이터 포함)
  - 기본 저장 위치: Documents/ScreenOCR/
  - 자동 로그 생성

- **성능**
  - 별도 스레드에서 OCR 처리 (UI 블로킹 방지)
  - 고속 화면 캡처 (mss 라이브러리)
  - 최적화된 이미지 처리

### Technical
- Python 3.10+ 지원
- PyQt6 GUI 프레임워크
- OpenCV 이미지 처리
- keyboard/pynput 전역 핫키
- mss 화면 캡처
- pytesseract OCR 인터페이스

### Documentation
- README.md
- INSTALL.md (설치 가이드)
- USAGE.md (사용 가이드)
- CHANGELOG.md
- 코드 주석 및 docstring

### Build
- PyInstaller 빌드 스크립트
- Windows 배치 파일 (build.bat)
- .gitignore 설정

## [Unreleased]

### Planned Features
- [ ] 영역 선택 캡처
- [ ] 사용자 정의 단축키
- [ ] 설정 UI
- [ ] 시스템 트레이 아이콘
- [ ] 캡처 히스토리
- [ ] 클립보드 자동 복사
- [ ] 다양한 이미지 형식 지원 (JPEG, BMP 등)
- [ ] OCR 결과 편집 기능
- [ ] 자동 번역 기능
- [ ] 스크린샷 주석 기능

### Known Issues
- 일부 시스템에서 관리자 권한 필요
- 매우 흐릿한 이미지는 OCR 정확도 낮음
- 손글씨 인식 불가

---

## Version History

- **1.0.0** (2025-01-22): 초기 릴리스
