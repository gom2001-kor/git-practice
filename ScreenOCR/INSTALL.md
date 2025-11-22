# 📦 ScreenOCR 설치 가이드

## 📥 방법 1: 실행 파일 사용 (권장)

가장 간단한 방법입니다. 설치가 필요 없습니다.

### 1단계: Tesseract OCR 설치

#### Windows 11/10

1. **Tesseract 다운로드**
   - [UB Mannheim Tesseract 다운로드 페이지](https://github.com/UB-Mannheim/tesseract/wiki) 방문
   - `tesseract-ocr-w64-setup-{버전}.exe` 다운로드 (64비트)

2. **Tesseract 설치**
   - 다운로드한 파일 실행
   - 기본 설치 경로 권장: `C:\Program Files\Tesseract-OCR`

3. **언어 데이터 선택**
   - 설치 중 "Additional Language Data" 선택
   - 다음 언어 체크:
     - ✅ Korean (kor)
     - ✅ English (eng)
     - ✅ Japanese (jpn)
     - ✅ Chinese - Traditional (chi_tra)

4. **설치 완료 확인**
   - 명령 프롬프트(CMD)에서 확인:
   ```bash
   tesseract --version
   ```
   - 버전 정보가 나오면 성공!

### 2단계: ScreenOCR 실행

1. `ScreenOCR.exe` 파일 다운로드
2. 더블클릭으로 실행
3. 완료! 🎉

---

## 🐍 방법 2: Python 소스 코드에서 실행

개발자이거나 소스 코드를 수정하고 싶은 경우

### 1단계: Python 설치

1. [Python 공식 웹사이트](https://www.python.org/downloads/) 방문
2. Python 3.10 이상 다운로드
3. 설치 시 "Add Python to PATH" 체크 ✅

### 2단계: Tesseract OCR 설치

위의 "방법 1 - 1단계" 참조

### 3단계: 프로젝트 설정

```bash
# 1. 프로젝트 클론 또는 다운로드
git clone <repository-url>
cd ScreenOCR

# 2. 가상환경 생성 (선택사항, 권장)
python -m venv venv

# 3. 가상환경 활성화
# Windows
venv\Scripts\activate

# 4. 의존성 설치
pip install -r requirements.txt
```

### 4단계: 애플리케이션 실행

```bash
python main.py
```

---

## 🔨 방법 3: 소스 코드에서 실행 파일 빌드

자신만의 실행 파일을 만들고 싶은 경우

### 1단계: Python 및 Tesseract 설치

위의 "방법 2 - 1단계, 2단계" 참조

### 2단계: 프로젝트 설정 및 빌드

```bash
# 1. 프로젝트 설정
cd ScreenOCR
pip install -r requirements.txt

# 2. 빌드 실행 (Windows)
build.bat

# 또는 Python으로 직접 빌드
python build_exe.py
```

### 3단계: 실행 파일 확인

빌드 완료 후 `dist/ScreenOCR.exe` 파일 생성

---

## ✅ 설치 확인

### Tesseract 설치 확인

```bash
# 명령 프롬프트(CMD)
tesseract --version
tesseract --list-langs
```

출력 예시:
```
tesseract 5.3.0
...
List of available languages (4):
chi_tra
eng
jpn
kor
```

### ScreenOCR 실행 확인

1. `ScreenOCR.exe` 실행
2. 우측 상단에 작은 창이 나타나면 성공
3. 스페이스바를 눌러 캡처 테스트

---

## 🔧 Tesseract 경로 수동 설정

Tesseract를 기본 경로가 아닌 다른 곳에 설치한 경우:

### 방법 1: 환경 변수 설정

1. "시스템 환경 변수 편집" 검색
2. "환경 변수" 클릭
3. "시스템 변수"에서 "Path" 선택 → "편집"
4. Tesseract 설치 경로 추가:
   ```
   C:\Program Files\Tesseract-OCR
   ```

### 방법 2: 코드 수정

`core/ocr_processor.py` 파일 수정:

```python
# OCRProcessor 클래스의 __init__ 메서드에서
pytesseract.pytesseract.tesseract_cmd = r'C:\YOUR\CUSTOM\PATH\tesseract.exe'
```

---

## ❗ 자주 발생하는 문제

### 문제 1: "Tesseract가 설치되지 않았습니다" 오류

**원인**: Tesseract가 설치되지 않았거나 PATH에 등록되지 않음

**해결**:
1. Tesseract 재설치
2. 환경 변수 PATH 확인
3. 명령 프롬프트에서 `tesseract --version` 확인

### 문제 2: "언어팩 누락" 경고

**원인**: 필요한 언어 데이터가 설치되지 않음

**해결**:
1. Tesseract 재설치 시 언어 데이터 선택
2. 또는 수동으로 언어 데이터 다운로드:
   - [tessdata 저장소](https://github.com/tesseract-ocr/tessdata)
   - 다운로드한 `.traineddata` 파일을 `C:\Program Files\Tesseract-OCR\tessdata\` 폴더에 복사

### 문제 3: Python 의존성 설치 실패

**원인**: pip 버전이 오래되었거나 네트워크 문제

**해결**:
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 의존성 재설치
pip install -r requirements.txt --upgrade
```

### 문제 4: 빌드 실패

**원인**: PyInstaller 호환성 문제

**해결**:
```bash
# PyInstaller 재설치
pip uninstall pyinstaller
pip install pyinstaller==6.3.0

# 빌드 재시도
python build_exe.py
```

---

## 📞 추가 도움말

문제가 계속되면:
1. `C:\Users\{사용자명}\Documents\ScreenOCR\app.log` 확인
2. Issue 등록
3. 로그 파일 첨부하여 문의

---

**설치 문서 버전**: 1.0.0
**최종 업데이트**: 2025-01-22
