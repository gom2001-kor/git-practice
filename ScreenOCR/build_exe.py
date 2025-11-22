"""
PyInstaller 빌드 스크립트
단일 실행 파일(.exe) 생성
"""
import PyInstaller.__main__
import os
import sys


def build_exe():
    """실행 파일 빌드"""

    # 현재 디렉토리
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 아이콘 파일 경로 (있는 경우)
    icon_path = os.path.join(current_dir, 'resources', 'icon.ico')

    # PyInstaller 옵션
    pyinstaller_args = [
        'main.py',  # 메인 스크립트
        '--name=ScreenOCR',  # 실행 파일 이름
        '--onefile',  # 단일 파일로 빌드
        '--windowed',  # 콘솔 창 숨김 (GUI 앱)
        '--clean',  # 빌드 전 캐시 정리

        # 숨겨진 import 모듈 추가
        '--hidden-import=PIL',
        '--hidden-import=PIL._imaging',
        '--hidden-import=pytesseract',
        '--hidden-import=cv2',
        '--hidden-import=numpy',
        '--hidden-import=mss',
        '--hidden-import=keyboard',
        '--hidden-import=pynput',

        # 데이터 파일 추가 (있는 경우)
        # '--add-data=resources/tessdata;tessdata',

        # 로그 레벨
        '--log-level=INFO',
    ]

    # 아이콘 파일이 있으면 추가
    if os.path.exists(icon_path):
        pyinstaller_args.append(f'--icon={icon_path}')

    print("=" * 60)
    print("ScreenOCR 빌드 시작")
    print("=" * 60)
    print(f"현재 디렉토리: {current_dir}")
    print(f"빌드 옵션: {' '.join(pyinstaller_args)}")
    print("=" * 60)

    try:
        # PyInstaller 실행
        PyInstaller.__main__.run(pyinstaller_args)

        print("\n" + "=" * 60)
        print("빌드 완료!")
        print("=" * 60)
        print(f"실행 파일 위치: {os.path.join(current_dir, 'dist', 'ScreenOCR.exe')}")
        print("=" * 60)

    except Exception as e:
        print(f"\n빌드 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
