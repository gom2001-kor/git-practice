"""
ScreenOCR 메인 애플리케이션
화면 캡처 + OCR 텍스트 추출 데스크톱 애플리케이션
"""
import sys
import time
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer, QThread, pyqtSignal

# 로컬 모듈
from ui.main_window import MainWindow
from ui.save_dialog import SaveDialog
from core.capture import ScreenCapture
from core.hotkey_manager import HotkeyManager
from core.ocr_processor import OCRProcessor
from utils.image_process import ImageProcessor
from utils.file_manager import FileManager


class OCRThread(QThread):
    """OCR 처리를 위한 별도 스레드"""
    finished = pyqtSignal(str)  # OCR 완료 시 텍스트 전달
    error = pyqtSignal(str)  # 에러 발생 시 에러 메시지 전달

    def __init__(self, image):
        super().__init__()
        self.image = image
        self.ocr_processor = OCRProcessor()
        self.image_processor = ImageProcessor()

    def run(self):
        """OCR 처리 실행"""
        try:
            # 이미지 전처리
            processed_image = self.image_processor.preprocess_for_ocr(
                self.image,
                method='auto'
            )

            # OCR 수행
            extracted_text = self.ocr_processor.extract_text(processed_image)

            # 완료 시그널 전송
            self.finished.emit(extracted_text)

        except Exception as e:
            # 에러 시그널 전송
            self.error.emit(str(e))


class ScreenOCRApp:
    """메인 애플리케이션 클래스"""

    def __init__(self):
        # QApplication 초기화
        self.app = QApplication(sys.argv)

        # 로거
        self.logger = logging.getLogger(__name__)

        # 파일 매니저 초기화 및 로깅 설정
        self.file_manager = FileManager()
        self.file_manager.setup_logging()

        # 컴포넌트 초기화
        self.main_window = MainWindow()
        self.capture = ScreenCapture()
        self.hotkey_manager = HotkeyManager()
        self.ocr_processor = OCRProcessor()
        self.image_processor = ImageProcessor()

        # 상태 변수
        self.current_image = None
        self.current_text = ""
        self.ocr_thread = None
        self.is_processing = False

        # Tesseract 확인
        self.check_tesseract()

        # 핫키 등록
        self.setup_hotkeys()

        # 메인 윈도우 표시
        self.main_window.show()

        self.logger.info("애플리케이션 초기화 완료")

    def check_tesseract(self):
        """Tesseract 설치 확인"""
        try:
            if not self.ocr_processor.check_tesseract():
                QMessageBox.critical(
                    None,
                    "Tesseract 미설치",
                    "Tesseract OCR이 설치되지 않았습니다.\n\n"
                    "다음 링크에서 다운로드하여 설치해주세요:\n"
                    "https://github.com/UB-Mannheim/tesseract/wiki\n\n"
                    "설치 후 언어 데이터(kor, eng, jpn, chi_tra)도 함께 설치해주세요.\n\n"
                    "애플리케이션을 종료합니다."
                )
                sys.exit(1)

            # 언어팩 확인
            is_valid, missing = self.ocr_processor.validate_languages()
            if not is_valid:
                QMessageBox.warning(
                    None,
                    "언어팩 누락",
                    f"다음 언어팩이 설치되지 않았습니다:\n{', '.join(missing)}\n\n"
                    "OCR 정확도가 떨어질 수 있습니다.\n"
                    "Tesseract 설치 시 해당 언어 데이터를 함께 설치해주세요."
                )

        except Exception as e:
            self.logger.error(f"Tesseract 확인 중 오류: {e}")

    def setup_hotkeys(self):
        """핫키 설정"""
        # 스페이스바: 캡처
        self.hotkey_manager.register_space_hotkey(self.on_capture_triggered)

        # ESC: 종료
        self.hotkey_manager.register_esc_hotkey(self.on_exit_triggered)

        self.logger.info("핫키 등록 완료")

    def on_capture_triggered(self):
        """스페이스바 눌림 - 캡처 시작"""
        if self.is_processing:
            self.logger.warning("이미 처리 중입니다")
            return

        self.is_processing = True
        self.logger.info("캡처 트리거됨")

        try:
            # 1. 캡처 중 메시지 표시
            self.main_window.show_capturing_message()
            QApplication.processEvents()

            # 2. 메인 윈도우 숨김
            self.main_window.hide()
            QApplication.processEvents()

            # 3. 0.3초 대기 (창이 완전히 사라질 시간)
            time.sleep(0.3)

            # 4. 화면 캡처
            self.current_image = self.capture.capture_all_screens()
            self.logger.info("화면 캡처 완료")

            # 5. 메인 윈도우 다시 표시
            self.main_window.show()
            QApplication.processEvents()

            # 6. OCR 처리 중 메시지 표시
            self.main_window.show_processing_message()
            QApplication.processEvents()

            # 7. OCR 처리 (별도 스레드)
            self.start_ocr_processing()

        except Exception as e:
            self.logger.error(f"캡처 중 오류 발생: {e}")
            QMessageBox.critical(
                self.main_window,
                "오류",
                f"화면 캡처 중 오류가 발생했습니다:\n{str(e)}"
            )
            self.reset_state()

    def start_ocr_processing(self):
        """OCR 처리 시작 (별도 스레드)"""
        self.ocr_thread = OCRThread(self.current_image)
        self.ocr_thread.finished.connect(self.on_ocr_finished)
        self.ocr_thread.error.connect(self.on_ocr_error)
        self.ocr_thread.start()

    def on_ocr_finished(self, extracted_text):
        """OCR 처리 완료"""
        self.logger.info(f"OCR 완료: {len(extracted_text)} 글자")
        self.current_text = extracted_text

        # UI 복원
        self.main_window.reset_ui()

        # 저장 다이얼로그 표시
        self.show_save_dialog()

        # 상태 초기화
        self.is_processing = False

    def on_ocr_error(self, error_message):
        """OCR 처리 오류"""
        self.logger.error(f"OCR 오류: {error_message}")

        # UI 복원
        self.main_window.reset_ui()

        # 오류 메시지 표시
        reply = QMessageBox.question(
            self.main_window,
            "OCR 오류",
            f"OCR 처리 중 오류가 발생했습니다:\n{error_message}\n\n"
            "이미지만 저장하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.current_text = "[OCR 처리 실패]"
            self.show_save_dialog()

        # 상태 초기화
        self.reset_state()

    def show_save_dialog(self):
        """저장 다이얼로그 표시"""
        try:
            dialog = SaveDialog(
                self.current_image,
                self.current_text,
                self.file_manager.default_save_dir
            )

            result = dialog.exec()

            if result == SaveDialog.DialogCode.Accepted:
                # 저장 성공
                image_path, text_path = dialog.get_saved_paths()
                if image_path and text_path:
                    self.file_manager.log_capture(image_path, text_path, success=True)
                    self.logger.info("파일 저장 완료")
            else:
                # 취소
                self.logger.info("저장 취소됨")

        except Exception as e:
            self.logger.error(f"저장 다이얼로그 오류: {e}")
            QMessageBox.critical(
                self.main_window,
                "오류",
                f"저장 다이얼로그 표시 중 오류가 발생했습니다:\n{str(e)}"
            )

    def on_exit_triggered(self):
        """ESC 키 눌림 - 종료"""
        self.logger.info("종료 트리거됨")

        reply = QMessageBox.question(
            self.main_window,
            "종료 확인",
            "ScreenOCR을 종료하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.cleanup()
            sys.exit(0)

    def reset_state(self):
        """상태 초기화"""
        self.is_processing = False
        self.current_image = None
        self.current_text = ""
        self.main_window.reset_ui()

    def cleanup(self):
        """정리 작업"""
        try:
            # 핫키 등록 해제
            self.hotkey_manager.unregister_all()

            # 로그
            self.logger.info("=" * 50)
            self.logger.info("ScreenOCR 애플리케이션 종료")
            self.logger.info("=" * 50)

        except Exception as e:
            self.logger.error(f"정리 작업 중 오류: {e}")

    def run(self):
        """애플리케이션 실행"""
        try:
            return self.app.exec()
        except Exception as e:
            self.logger.error(f"애플리케이션 실행 중 오류: {e}")
            return 1


def main():
    """메인 함수"""
    try:
        app = ScreenOCRApp()
        sys.exit(app.run())
    except Exception as e:
        logging.error(f"애플리케이션 시작 실패: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
