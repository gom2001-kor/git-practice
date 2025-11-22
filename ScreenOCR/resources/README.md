# Resources 폴더

이 폴더에는 ScreenOCR 애플리케이션의 리소스 파일이 포함됩니다.

## 📁 폴더 구조

```
resources/
├── icon.ico              # 앱 아이콘 (선택사항)
├── tessdata/            # Tesseract 언어 데이터 (선택사항)
└── README.md            # 이 파일
```

## 🎨 아이콘 파일 (icon.ico)

### 요구사항
- **형식**: ICO (Windows 아이콘)
- **크기**: 256x256 픽셀 권장
- **색상**: 32비트 (알파 채널 포함)

### 생성 방법

#### 온라인 도구 사용
1. [ConvertICO](https://convertico.com/) 방문
2. PNG/JPG 이미지 업로드
3. ICO 파일 다운로드
4. `resources/icon.ico`로 저장

#### Photoshop/GIMP 사용
1. 256x256 이미지 생성
2. ICO 형식으로 저장
3. `resources/icon.ico`로 저장

### 기본 동작
- 아이콘 파일이 없으면: 기본 Python 아이콘 사용
- 아이콘 파일이 있으면: 빌드 시 자동으로 포함됨

## 📚 Tesseract 언어 데이터 (tessdata/)

### 개요
이 폴더는 Tesseract OCR 언어 데이터를 포함할 수 있습니다.
단일 실행 파일(.exe)에 언어 데이터를 포함시키려면 이 폴더에 `.traineddata` 파일을 넣으세요.

### 필요한 파일
- `kor.traineddata` - 한국어
- `eng.traineddata` - 영어
- `jpn.traineddata` - 일본어
- `chi_tra.traineddata` - 중국어 번체

### 다운로드 방법

#### 방법 1: Tesseract 설치 폴더에서 복사
```
C:\Program Files\Tesseract-OCR\tessdata\
```
위 경로에서 필요한 `.traineddata` 파일을 이 폴더로 복사

#### 방법 2: GitHub에서 다운로드
1. [tessdata 저장소](https://github.com/tesseract-ocr/tessdata) 방문
2. 필요한 파일 다운로드:
   - kor.traineddata
   - eng.traineddata
   - jpn.traineddata
   - chi_tra.traineddata
3. 이 폴더에 저장

### 빌드 시 포함

`build_exe.py`에서 다음 줄의 주석 해제:
```python
'--add-data=resources/tessdata;tessdata',
```

이렇게 하면 실행 파일에 언어 데이터가 포함됩니다.

### 주의사항
- 파일 크기가 크므로(각 10-20MB) 실행 파일 크기가 증가합니다
- 시스템에 Tesseract가 설치되어 있다면 이 파일들은 선택사항입니다
- 포터블 앱으로 만들려면 언어 데이터를 포함하는 것이 좋습니다

## 📝 기타 리소스

필요에 따라 다음 파일들을 추가할 수 있습니다:

### 이미지 파일
- 로고 이미지
- UI 아이콘
- 스플래시 스크린

### 폰트 파일
- 사용자 정의 폰트 (.ttf, .otf)

### 설정 파일
- 기본 설정 JSON
- 테마 파일

## 🔧 사용 예시

### 아이콘 추가 후 빌드
```bash
# 1. icon.ico 파일을 resources/ 폴더에 복사
# 2. 빌드 실행
python build_exe.py
```

### 언어 데이터 포함 빌드
```bash
# 1. .traineddata 파일을 resources/tessdata/ 폴더에 복사
# 2. build_exe.py에서 --add-data 주석 해제
# 3. 빌드 실행
python build_exe.py
```

---

**문서 버전**: 1.0.0
**최종 업데이트**: 2025-01-22
