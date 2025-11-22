# 📸 ScreenOCR - 화면 캡처 + OCR 텍스트 추출 앱

Windows 11 (x64)용 화면 캡처 및 OCR 텍스트 추출 데스크톱 애플리케이션입니다.

## ✨ 주요 기능

- 🖼️ **화면 캡처**: 스페이스바 한 번으로 전체 화면 캡처
- 📝 **OCR 텍스트 추출**: Tesseract OCR을 사용한 정확한 텍스트 추출
- 🌏 **다국어 지원**: 한국어, 영어, 일본어, 중국어(번체) 지원
- 💾 **자동 저장**: 이미지 파일(.png)과 텍스트 파일(.txt) 동시 저장
- 🎨 **간편한 UI**: 우측 상단에 위치한 작고 간편한 실행창
- ⌨️ **전역 핫키**: 다른 앱 사용 중에도 스페이스바로 캡처 가능

## 🚀 빠른 시작

### 1. 사전 요구사항

#### Tesseract OCR 설치 (필수)
1. [Tesseract OCR 다운로드](https://github.com/UB-Mannheim/tesseract/wiki)
2. 설치 시 **언어 데이터**도 함께 선택:
   - Korean (kor)
   - English (eng)
   - Japanese (jpn)
   - Chinese - Traditional (chi_tra)

#### Python 3.10 이상 (개발 시)
- [Python 다운로드](https://www.python.org/downloads/)

### 2. 실행 파일 사용 (권장)

```bash
# 단순히 ScreenOCR.exe 더블클릭으로 실행
ScreenOCR.exe
```

### 3. 소스 코드에서 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python main.py
```

## 📖 사용 방법

### 기본 사용법

1. **앱 실행**: `ScreenOCR.exe` 더블클릭
2. **화면 캡처**: 스페이스바 누르기
3. **자동 처리**: 화면 캡처 → OCR 텍스트 추출 (자동)
4. **파일 저장**: 저장 다이얼로그에서 파일명 입력 후 저장

### 단축키

| 키 | 기능 |
|---|---|
| `Space` | 화면 캡처 + OCR 시작 |
| `ESC` | 앱 종료 |

### 저장 파일

캡처된 내용은 두 개의 파일로 저장됩니다:

1. **이미지 파일**: `{파일명}.png`
   - 원본 화질의 PNG 이미지

2. **텍스트 파일**: `{파일명}.txt`
   - OCR로 추출된 텍스트
   - UTF-8 인코딩
   - 캡처 일시 정보 포함

**기본 저장 위치**: `C:\Users\{사용자명}\Documents\ScreenOCR\`

## 🛠️ 개발 및 빌드

### 프로젝트 구조

```
ScreenOCR/
├── main.py                 # 메인 애플리케이션
├── ui/
│   ├── main_window.py     # 실행창 UI
│   └── save_dialog.py     # 저장 다이얼로그
├── core/
│   ├── capture.py         # 화면 캡처 로직
│   ├── ocr_processor.py   # OCR 처리
│   └── hotkey_manager.py  # 전역 핫키 관리
├── utils/
│   ├── image_process.py   # 이미지 전처리
│   └── file_manager.py    # 파일 저장 로직
├── resources/             # 리소스 파일
├── requirements.txt       # Python 의존성
├── build_exe.py          # PyInstaller 빌드 스크립트
└── build.bat             # Windows 빌드 배치 파일
```

### 실행 파일 빌드

#### 방법 1: 배치 파일 사용 (Windows)
```bash
build.bat
```

#### 방법 2: Python 스크립트 사용
```bash
python build_exe.py
```

#### 방법 3: 수동 빌드
```bash
pyinstaller --onefile --windowed --name=ScreenOCR main.py
```

빌드 완료 후 `dist/ScreenOCR.exe` 생성

## 🔧 기술 스택

- **언어**: Python 3.10+
- **GUI 프레임워크**: PyQt6
- **OCR 엔진**: Tesseract OCR 4.x
- **이미지 처리**: OpenCV, Pillow
- **화면 캡처**: mss (Multi-Screen Screenshot)
- **전역 핫키**: keyboard, pynput
- **패키징**: PyInstaller

## 📋 시스템 요구사항

### 최소 사양
- **OS**: Windows 10/11 (x64)
- **RAM**: 4GB 이상
- **디스크**: 500MB 여유 공간
- **기타**: Tesseract OCR 설치 필수

### 권장 사양
- **OS**: Windows 11 (x64)
- **RAM**: 8GB 이상
- **디스크**: 1GB 여유 공간

## ❗ 문제 해결

### Tesseract 미설치 오류
```
Tesseract OCR이 설치되지 않았습니다.
```
**해결**: [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)을 다운로드하여 설치하고, 언어 데이터도 함께 설치하세요.

### 언어팩 누락 경고
```
다음 언어팩이 설치되지 않았습니다: kor, jpn, chi_tra
```
**해결**: Tesseract 설치 시 Additional Language Data에서 해당 언어를 선택하여 설치하세요.

### OCR 정확도가 낮음
- 이미지 품질이 낮거나 글자가 흐릿한 경우 정확도가 떨어질 수 있습니다
- 가능하면 선명하고 대비가 높은 화면을 캡처하세요
- 이미지 전처리 방법을 조정할 수 있습니다 (`utils/image_process.py`)

### 관리자 권한 요구
일부 시스템에서는 전역 핫키 사용을 위해 관리자 권한이 필요할 수 있습니다.
**해결**: `ScreenOCR.exe`를 우클릭 → "관리자 권한으로 실행"

## 📝 로그 및 디버깅

앱 실행 로그는 다음 위치에 저장됩니다:
```
C:\Users\{사용자명}\Documents\ScreenOCR\app.log
```

로그 파일을 확인하여 오류를 진단할 수 있습니다.

## 🤝 기여

버그 리포트, 기능 제안 등은 Issue를 통해 제출해 주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🙏 감사의 말

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- [mss](https://github.com/BoboTiG/python-mss)
- [OpenCV](https://opencv.org/)

---

**제작**: ScreenOCR Team
**버전**: 1.0.0
**최종 업데이트**: 2025-01-22
