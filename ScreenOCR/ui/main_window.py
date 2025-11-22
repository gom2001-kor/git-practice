"""
메인 윈도우 UI
항상 최상위에 표시되는 작은 실행창
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPalette, QColor, QFont


class MainWindow(QWidget):
    """메인 실행창"""

    # 색상 테마
    PRIMARY_COLOR = "#4A90E2"
    BACKGROUND = "#2C3E50"
    TEXT_COLOR = "#ECF0F1"
    SUCCESS_COLOR = "#27AE60"
    ERROR_COLOR = "#E74C3C"

    def __init__(self):
        super().__init__()
        self.dragging = False
        self.drag_position = QPoint()
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        # 창 크기 고정 (150x100)
        self.setFixedSize(150, 120)

        # 창 플래그 설정: 항상 최상위, 프레임 없음
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        # 투명도 설정 (90%)
        self.setWindowOpacity(0.9)

        # 배경 색상 설정
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.BACKGROUND))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # 스타일시트 적용 (둥근 모서리)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.BACKGROUND};
                border-radius: 10px;
                border: 2px solid {self.PRIMARY_COLOR};
            }}
            QLabel {{
                color: {self.TEXT_COLOR};
                background-color: transparent;
                border: none;
            }}
        """)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # 제목 라벨
        title_label = QLabel("📸 OCR Capture")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Malgun Gothic", 10, QFont.Weight.Bold)
        title_label.setFont(title_font)

        # 안내 메시지 라벨
        info_label = QLabel("스페이스바를 누르면\n화면이 캡쳐됩니다.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_font = QFont("Malgun Gothic", 8)
        info_label.setFont(info_font)
        info_label.setWordWrap(True)

        # 종료 안내 라벨
        exit_label = QLabel("[종료: ESC]")
        exit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exit_font = QFont("Malgun Gothic", 7)
        exit_label.setFont(exit_font)
        exit_label.setStyleSheet(f"color: {self.PRIMARY_COLOR};")

        # 레이아웃에 위젯 추가
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addStretch()
        layout.addWidget(exit_label)

        self.setLayout(layout)

        # 창을 화면 우측 상단에 배치
        self.position_window()

    def position_window(self):
        """창을 모니터 우측 상단에 배치"""
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 20  # 우측에서 20px 여백
        y = 20  # 상단에서 20px 여백
        self.move(x, y)

    def mousePressEvent(self, event):
        """마우스 클릭 이벤트 - 드래그 시작"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """마우스 이동 이벤트 - 드래그 중"""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """마우스 릴리즈 이벤트 - 드래그 종료"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()

    def show_capturing_message(self):
        """캡처 중 메시지 표시"""
        # 기존 레이아웃의 모든 위젯 제거
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 캡처 중 메시지
        capturing_label = QLabel("📸\n캡처 중...")
        capturing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        capturing_font = QFont("Malgun Gothic", 10, QFont.Weight.Bold)
        capturing_label.setFont(capturing_font)
        capturing_label.setStyleSheet(f"color: {self.SUCCESS_COLOR};")

        layout.addWidget(capturing_label)

    def show_processing_message(self):
        """OCR 처리 중 메시지 표시"""
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # OCR 처리 중 메시지
        processing_label = QLabel("⏳\nOCR 처리 중...\n잠시만 기다려주세요")
        processing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        processing_font = QFont("Malgun Gothic", 9)
        processing_label.setFont(processing_font)
        processing_label.setStyleSheet(f"color: {self.PRIMARY_COLOR};")

        layout.addWidget(processing_label)

    def reset_ui(self):
        """UI를 초기 상태로 복원"""
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 원래 UI 복원
        title_label = QLabel("📸 OCR Capture")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Malgun Gothic", 10, QFont.Weight.Bold)
        title_label.setFont(title_font)

        info_label = QLabel("스페이스바를 누르면\n화면이 캡쳐됩니다.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_font = QFont("Malgun Gothic", 8)
        info_label.setFont(info_font)
        info_label.setWordWrap(True)

        exit_label = QLabel("[종료: ESC]")
        exit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exit_font = QFont("Malgun Gothic", 7)
        exit_label.setFont(exit_font)
        exit_label.setStyleSheet(f"color: {self.PRIMARY_COLOR};")

        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addStretch()
        layout.addWidget(exit_label)
