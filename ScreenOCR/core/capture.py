"""
화면 캡처 로직
mss를 사용한 고속 스크린샷
"""
import mss
import mss.tools
from PIL import Image
import io
import logging


class ScreenCapture:
    """화면 캡처 클래스"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def capture_all_screens(self):
        """
        모든 모니터의 전체 화면을 캡처

        Returns:
            PIL.Image: 캡처된 이미지
        """
        try:
            with mss.mss() as sct:
                # 모든 모니터를 포함하는 전체 영역 캡처
                monitor = sct.monitors[0]  # 0번은 모든 모니터를 포함하는 가상 화면

                self.logger.info(f"캡처 영역: {monitor}")

                # 스크린샷 촬영
                screenshot = sct.grab(monitor)

                # mss 이미지를 PIL Image로 변환
                img = Image.frombytes(
                    'RGB',
                    (screenshot.width, screenshot.height),
                    screenshot.rgb
                )

                self.logger.info(f"캡처 완료: {img.size}")
                return img

        except Exception as e:
            self.logger.error(f"화면 캡처 중 오류 발생: {e}")
            raise

    def capture_specific_monitor(self, monitor_index=1):
        """
        특정 모니터만 캡처

        Args:
            monitor_index (int): 모니터 인덱스 (1부터 시작)

        Returns:
            PIL.Image: 캡처된 이미지
        """
        try:
            with mss.mss() as sct:
                # 특정 모니터 선택
                if monitor_index >= len(sct.monitors):
                    self.logger.warning(f"모니터 {monitor_index}가 존재하지 않음. 기본 모니터 사용")
                    monitor_index = 1

                monitor = sct.monitors[monitor_index]
                self.logger.info(f"모니터 {monitor_index} 캡처: {monitor}")

                # 스크린샷 촬영
                screenshot = sct.grab(monitor)

                # PIL Image로 변환
                img = Image.frombytes(
                    'RGB',
                    (screenshot.width, screenshot.height),
                    screenshot.rgb
                )

                self.logger.info(f"캡처 완료: {img.size}")
                return img

        except Exception as e:
            self.logger.error(f"화면 캡처 중 오류 발생: {e}")
            raise

    def get_monitor_count(self):
        """
        연결된 모니터 개수 반환

        Returns:
            int: 모니터 개수
        """
        try:
            with mss.mss() as sct:
                # 0번 인덱스는 가상 화면이므로 제외
                return len(sct.monitors) - 1
        except Exception as e:
            self.logger.error(f"모니터 개수 확인 중 오류 발생: {e}")
            return 1  # 기본값

    def save_screenshot(self, image, filepath):
        """
        스크린샷을 파일로 저장

        Args:
            image (PIL.Image): 저장할 이미지
            filepath (str): 저장 경로
        """
        try:
            image.save(filepath, format='PNG', optimize=False)
            self.logger.info(f"이미지 저장 완료: {filepath}")
        except Exception as e:
            self.logger.error(f"이미지 저장 중 오류 발생: {e}")
            raise
