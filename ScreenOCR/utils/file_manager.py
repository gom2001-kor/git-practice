"""
파일 관리자
기본 저장 경로 관리 및 로깅
"""
import os
import logging
from datetime import datetime
from pathlib import Path


class FileManager:
    """파일 관리 클래스"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.default_save_dir = self.get_default_save_dir()
        self.log_file = self.get_log_file_path()

    def get_default_save_dir(self):
        """
        기본 저장 디렉토리 경로 반환
        사용자 문서 폴더/ScreenOCR/

        Returns:
            str: 기본 저장 디렉토리 경로
        """
        try:
            # Windows: 사용자 문서 폴더
            documents_dir = Path.home() / "Documents"

            # ScreenOCR 폴더 생성
            save_dir = documents_dir / "ScreenOCR"
            save_dir.mkdir(parents=True, exist_ok=True)

            self.logger.info(f"기본 저장 경로: {save_dir}")
            return str(save_dir)

        except Exception as e:
            self.logger.error(f"기본 저장 경로 생성 실패: {e}")
            # 실패 시 현재 디렉토리 반환
            return os.getcwd()

    def get_log_file_path(self):
        """
        로그 파일 경로 반환

        Returns:
            str: 로그 파일 경로
        """
        try:
            # 앱 실행 디렉토리에 로그 파일 생성
            log_dir = Path.home() / "Documents" / "ScreenOCR"
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / "app.log"
            return str(log_file)

        except Exception as e:
            # 실패 시 현재 디렉토리
            return "app.log"

    def setup_logging(self, level=logging.INFO):
        """
        로깅 설정

        Args:
            level: 로그 레벨
        """
        try:
            # 로그 포맷
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

            # 파일 핸들러
            file_handler = logging.FileHandler(
                self.log_file,
                encoding='utf-8'
            )
            file_handler.setFormatter(logging.Formatter(log_format))

            # 콘솔 핸들러
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(log_format))

            # 루트 로거 설정
            root_logger = logging.getLogger()
            root_logger.setLevel(level)
            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)

            self.logger.info("=" * 50)
            self.logger.info("ScreenOCR 애플리케이션 시작")
            self.logger.info("=" * 50)

        except Exception as e:
            print(f"로깅 설정 실패: {e}")

    def log_capture(self, image_path, text_path, success=True):
        """
        캡처 기록 로깅

        Args:
            image_path (str): 이미지 파일 경로
            text_path (str): 텍스트 파일 경로
            success (bool): 성공 여부
        """
        try:
            if success:
                self.logger.info(f"캡처 성공 - 이미지: {image_path}, 텍스트: {text_path}")
            else:
                self.logger.warning(f"캡처 실패 - {image_path}")

        except Exception as e:
            self.logger.error(f"로그 기록 실패: {e}")

    def create_backup_dir(self):
        """
        백업 디렉토리 생성

        Returns:
            str: 백업 디렉토리 경로
        """
        try:
            backup_dir = Path(self.default_save_dir) / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)

            self.logger.info(f"백업 디렉토리: {backup_dir}")
            return str(backup_dir)

        except Exception as e:
            self.logger.error(f"백업 디렉토리 생성 실패: {e}")
            return self.default_save_dir

    def get_file_list(self, extension=".png"):
        """
        저장 디렉토리의 파일 목록 반환

        Args:
            extension (str): 파일 확장자

        Returns:
            list: 파일 경로 리스트
        """
        try:
            save_dir = Path(self.default_save_dir)
            files = list(save_dir.glob(f"*{extension}"))
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            self.logger.info(f"파일 목록: {len(files)}개 파일")
            return [str(f) for f in files]

        except Exception as e:
            self.logger.error(f"파일 목록 조회 실패: {e}")
            return []

    def cleanup_old_files(self, days=30):
        """
        오래된 파일 정리

        Args:
            days (int): 보관 일수
        """
        try:
            save_dir = Path(self.default_save_dir)
            current_time = datetime.now().timestamp()
            cutoff_time = current_time - (days * 24 * 60 * 60)

            deleted_count = 0

            for file in save_dir.glob("*"):
                if file.is_file():
                    if file.stat().st_mtime < cutoff_time:
                        file.unlink()
                        deleted_count += 1
                        self.logger.info(f"오래된 파일 삭제: {file}")

            self.logger.info(f"총 {deleted_count}개 파일 정리 완료")

        except Exception as e:
            self.logger.error(f"파일 정리 실패: {e}")

    def open_save_directory(self):
        """
        저장 폴더를 탐색기로 열기
        """
        try:
            import subprocess
            import platform

            if platform.system() == "Windows":
                os.startfile(self.default_save_dir)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.default_save_dir])
            else:  # Linux
                subprocess.run(["xdg-open", self.default_save_dir])

            self.logger.info(f"저장 폴더 열기: {self.default_save_dir}")

        except Exception as e:
            self.logger.error(f"저장 폴더 열기 실패: {e}")
