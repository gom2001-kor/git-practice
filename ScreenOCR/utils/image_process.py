"""
이미지 전처리 유틸리티
OCR 정확도 향상을 위한 이미지 전처리
"""
import cv2
import numpy as np
from PIL import Image
import logging


class ImageProcessor:
    """이미지 전처리 클래스"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def preprocess_for_ocr(self, image, method='auto'):
        """
        OCR을 위한 이미지 전처리

        Args:
            image (PIL.Image): 원본 이미지
            method (str): 전처리 방법 ('auto', 'simple', 'advanced')

        Returns:
            PIL.Image: 전처리된 이미지
        """
        try:
            # PIL Image를 OpenCV 형식으로 변환
            img_array = np.array(image)
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            if method == 'simple':
                processed = self._simple_preprocess(img_cv)
            elif method == 'advanced':
                processed = self._advanced_preprocess(img_cv)
            else:  # auto
                processed = self._auto_preprocess(img_cv)

            # OpenCV 이미지를 PIL Image로 변환
            processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(processed_rgb)

            return pil_image

        except Exception as e:
            self.logger.error(f"이미지 전처리 중 오류 발생: {e}")
            # 오류 발생 시 원본 반환
            return image

    def _simple_preprocess(self, img_cv):
        """
        간단한 전처리
        - 그레이스케일 변환

        Args:
            img_cv: OpenCV 이미지

        Returns:
            OpenCV 이미지
        """
        # 그레이스케일 변환
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # 다시 BGR로 변환 (일관성 유지)
        processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        return processed

    def _advanced_preprocess(self, img_cv):
        """
        고급 전처리
        - 그레이스케일 변환
        - 대비 향상 (CLAHE)
        - 샤프닝
        - 노이즈 제거

        Args:
            img_cv: OpenCV 이미지

        Returns:
            OpenCV 이미지
        """
        # 1. 그레이스케일 변환
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # 2. 대비 향상 (CLAHE - Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 3. 샤프닝
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)

        # 4. 노이즈 제거 (Bilateral Filter)
        denoised = cv2.bilateralFilter(sharpened, 9, 75, 75)

        # 다시 BGR로 변환
        processed = cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)

        return processed

    def _auto_preprocess(self, img_cv):
        """
        자동 전처리
        이미지 특성에 따라 적절한 전처리 선택

        Args:
            img_cv: OpenCV 이미지

        Returns:
            OpenCV 이미지
        """
        # 1. 그레이스케일 변환
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # 2. 대비 향상 (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 3. 적응형 이진화 (선택적)
        # 텍스트가 명확한 경우 이진화가 도움이 될 수 있음
        # 하지만 기본적으로는 그레이스케일로 진행

        # 4. 샤프닝 (약하게)
        kernel = np.array([[0, -1, 0],
                          [-1, 5, -1],
                          [0, -1, 0]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)

        # 다시 BGR로 변환
        processed = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)

        return processed

    def resize_image(self, image, scale_factor=2.0):
        """
        이미지 크기 조정 (OCR 정확도 향상을 위해 확대)

        Args:
            image (PIL.Image): 원본 이미지
            scale_factor (float): 확대 비율

        Returns:
            PIL.Image: 크기 조정된 이미지
        """
        try:
            new_width = int(image.width * scale_factor)
            new_height = int(image.height * scale_factor)

            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.logger.info(f"이미지 크기 조정: {image.size} -> {resized.size}")

            return resized

        except Exception as e:
            self.logger.error(f"이미지 크기 조정 중 오류 발생: {e}")
            return image

    def create_thumbnail(self, image, max_size=(300, 300)):
        """
        썸네일 생성

        Args:
            image (PIL.Image): 원본 이미지
            max_size (tuple): 최대 크기 (width, height)

        Returns:
            PIL.Image: 썸네일 이미지
        """
        try:
            thumbnail = image.copy()
            thumbnail.thumbnail(max_size, Image.Resampling.LANCZOS)
            self.logger.info(f"썸네일 생성: {image.size} -> {thumbnail.size}")

            return thumbnail

        except Exception as e:
            self.logger.error(f"썸네일 생성 중 오류 발생: {e}")
            return image
