@echo off
echo ======================================
echo ScreenOCR Build Script
echo ======================================
echo.

REM Python 가상환경 활성화 (있는 경우)
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM 의존성 설치
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ======================================
echo Building executable...
echo ======================================
echo.

REM 빌드 실행
python build_exe.py

echo.
echo ======================================
echo Build completed!
echo ======================================
echo.

pause
