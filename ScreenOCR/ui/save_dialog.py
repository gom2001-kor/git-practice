"""
저장 다이얼로그 UI
이미지와 텍스트를 저장하기 위한 다이얼로그
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QImage
from PIL import Image
import os


class SaveDialog(QDialog):
    """저장 다이얼로그 클래스"""

    # 색상 테마
    PRIMARY_COLOR = "#4A90E2"
    BACKGROUND = "#2C3E50"
    TEXT_COLOR = "#ECF0F1"
    SUCCESS_COLOR = "#27AE60"
    ERROR_COLOR = "#E74C3C"

    def __init__(self, image, extracted_text, default_path=""):
        """
        Args:
            image (PIL.Image): 캡처된 이미지
            extracted_text (str): OCR로 추출된 텍스트
            default_path (str): 기본 저장 경로
        """
        super().__init__()
        self.image = image
        self.extracted_text = extracted_text
        self.default_path = default_path
        self.save_path = ""
        self.filename = ""

        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("파일 저장")
        self.setFixedSize(500, 600)

        # 스타일시트 적용
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #ECF0F1;
            }}
            QLabel {{
                color: #2C3E50;
                font-family: 'Malgun Gothic';
            }}
            QLineEdit {{
                padding: 8px;
                border: 2px solid {self.PRIMARY_COLOR};
                border-radius: 5px;
                background-color: white;
                color: #2C3E50;
                font-family: 'Malgun Gothic';
                font-size: 10pt;
            }}
            QTextEdit {{
                padding: 8px;
                border: 2px solid {self.PRIMARY_COLOR};
                border-radius: 5px;
                background-color: white;
                color: #2C3E50;
                font-family: 'Malgun Gothic';
                font-size: 9pt;
            }}
            QPushButton {{
                padding: 10px 20px;
                background-color: {self.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                font-family: 'Malgun Gothic';
                font-size: 10pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #357ABD;
            }}
            QPushButton#cancelButton {{
                background-color: #95A5A6;
            }}
            QPushButton#cancelButton:hover {{
                background-color: #7F8C8D;
            }}
        """)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 제목
        title_label = QLabel("📁 파일 저장")
        title_font = QFont("Malgun Gothic", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 파일명 입력
        filename_label = QLabel("파일명:")
        filename_font = QFont("Malgun Gothic", 10)
        filename_label.setFont(filename_font)
        main_layout.addWidget(filename_label)

        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("파일명을 입력하세요 (확장자 제외)")
        # 기본 파일명: screenshot_YYYYMMDD_HHMMSS
        from datetime import datetime
        default_filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.filename_input.setText(default_filename)
        main_layout.addWidget(self.filename_input)

        # 저장 위치 선택
        path_layout = QHBoxLayout()
        path_label = QLabel("저장 위치:")
        path_label.setFont(filename_font)

        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setText(self.default_path)

        browse_button = QPushButton("폴더 선택")
        browse_button.clicked.connect(self.browse_folder)

        path_layout.addWidget(self.path_display, stretch=3)
        path_layout.addWidget(browse_button, stretch=1)

        main_layout.addWidget(path_label)
        main_layout.addLayout(path_layout)

        # 미리보기 섹션
        preview_label = QLabel("미리보기:")
        preview_label.setFont(filename_font)
        main_layout.addWidget(preview_label)

        # 이미지 미리보기
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet(f"""
            border: 2px solid {self.PRIMARY_COLOR};
            border-radius: 5px;
            background-color: white;
            padding: 5px;
        """)
        self.image_preview.setFixedHeight(150)
        self.set_preview_image()
        main_layout.addWidget(self.image_preview)

        # 추출된 텍스트 미리보기
        text_preview_label = QLabel("추출된 텍스트 (첫 100자):")
        text_preview_label.setFont(filename_font)
        main_layout.addWidget(text_preview_label)

        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setFixedHeight(120)
        # 첫 100자만 표시
        preview_text = self.extracted_text[:100] if self.extracted_text else "[텍스트가 추출되지 않았습니다]"
        if len(self.extracted_text) > 100:
            preview_text += "..."
        self.text_preview.setText(preview_text)
        main_layout.addWidget(self.text_preview)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        save_button = QPushButton("저장")
        save_button.clicked.connect(self.save_files)

        cancel_button = QPushButton("취소")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def set_preview_image(self):
        """이미지 미리보기 설정"""
        try:
            # PIL Image를 QPixmap으로 변환
            # 썸네일 생성
            thumbnail = self.image.copy()
            thumbnail.thumbnail((400, 120), Image.Resampling.LANCZOS)

            # PIL Image를 QImage로 변환
            img_bytes = thumbnail.tobytes()
            qimage = QImage(
                img_bytes,
                thumbnail.width,
                thumbnail.height,
                thumbnail.width * 3,
                QImage.Format.Format_RGB888
            )

            pixmap = QPixmap.fromImage(qimage)
            self.image_preview.setPixmap(pixmap)

        except Exception as e:
            self.image_preview.setText("이미지 미리보기 실패")

    def browse_folder(self):
        """폴더 선택 다이얼로그"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "저장 폴더 선택",
            self.path_display.text()
        )

        if folder:
            self.path_display.setText(folder)

    def save_files(self):
        """파일 저장 처리"""
        # 파일명 확인
        filename = self.filename_input.text().strip()
        if not filename:
            QMessageBox.warning(self, "경고", "파일명을 입력해주세요.")
            return

        # 저장 경로 확인
        save_dir = self.path_display.text()
        if not save_dir or not os.path.exists(save_dir):
            QMessageBox.warning(self, "경고", "유효한 저장 경로를 선택해주세요.")
            return

        # 파일 경로 생성
        image_path = os.path.join(save_dir, f"{filename}.png")
        text_path = os.path.join(save_dir, f"{filename}.txt")

        # 파일 존재 확인
        if os.path.exists(image_path) or os.path.exists(text_path):
            reply = QMessageBox.question(
                self,
                "확인",
                "파일이 이미 존재합니다. 덮어쓰시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                return

        try:
            # 이미지 저장
            self.image.save(image_path, format='PNG', optimize=False)

            # 텍스트 파일 저장
            from datetime import datetime
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("OCR 추출 결과\n")
                f.write("=" * 50 + "\n")
                f.write(f"캡처 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"이미지 파일: {filename}.png\n")
                f.write("=" * 50 + "\n\n")
                f.write(self.extracted_text if self.extracted_text else "[텍스트가 추출되지 않았습니다]")
                f.write("\n\n" + "=" * 50 + "\n")
                f.write("End of OCR Result\n")
                f.write("=" * 50 + "\n")

            # 성공 메시지
            QMessageBox.information(
                self,
                "성공",
                f"파일이 저장되었습니다.\n\n"
                f"이미지: {image_path}\n"
                f"텍스트: {text_path}"
            )

            # 저장된 경로 설정
            self.save_path = save_dir
            self.filename = filename

            # 다이얼로그 닫기
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                "오류",
                f"파일 저장 중 오류가 발생했습니다:\n{str(e)}"
            )

    def get_saved_paths(self):
        """
        저장된 파일 경로 반환

        Returns:
            tuple: (이미지 경로, 텍스트 경로)
        """
        if self.save_path and self.filename:
            image_path = os.path.join(self.save_path, f"{self.filename}.png")
            text_path = os.path.join(self.save_path, f"{self.filename}.txt")
            return image_path, text_path
        return None, None
