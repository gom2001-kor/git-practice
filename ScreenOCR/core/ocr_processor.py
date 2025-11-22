"""
OCR 처리 엔진
Tesseract OCR을 사용한 텍스트 추출
"""
import pytesseract
from PIL import Image
import logging
import os


class OCRProcessor:
    """OCR 처리 클래스"""

    def __init__(self, tesseract_path=None):
        """
        Args:
            tesseract_path (str): Tesseract 실행 파일 경로 (선택적)
        """
        self.logger = logging.getLogger(__name__)

        # Tesseract 경로 설정
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            # Windows 기본 설치 경로 시도
            default_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'tesseract.exe'  # PATH에 있는 경우
            ]

            for path in default_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    self.logger.info(f"Tesseract 경로 설정: {path}")
                    break

        # 지원 언어
        self.languages = 'kor+eng+jpn+chi_tra'

    def extract_text(self, image, preprocess=True):
        """
        이미지에서 텍스트 추출

        Args:
            image (PIL.Image): OCR을 수행할 이미지
            preprocess (bool): 전처리 수행 여부

        Returns:
            str: 추출된 텍스트
        """
        try:
            # Tesseract 설정
            custom_config = r'--oem 1 --psm 3'

            # OCR 수행
            text = pytesseract.image_to_string(
                image,
                lang=self.languages,
                config=custom_config
            )

            self.logger.info(f"OCR 완료: {len(text)} 글자 추출")

            # 빈 텍스트 확인
            if not text.strip():
                self.logger.warning("추출된 텍스트가 없습니다")
                return ""

            return text.strip()

        except pytesseract.TesseractNotFoundError:
            self.logger.error("Tesseract가 설치되지 않았습니다")
            raise Exception(
                "Tesseract OCR이 설치되지 않았습니다.\n\n"
                "다음 링크에서 다운로드하여 설치해주세요:\n"
                "https://github.com/UB-Mannheim/tesseract/wiki\n\n"
                "설치 후 언어 데이터(kor, eng, jpn, chi_tra)도 함께 설치해주세요."
            )

        except Exception as e:
            self.logger.error(f"OCR 처리 중 오류 발생: {e}")
            raise

    def extract_text_with_confidence(self, image):
        """
        이미지에서 텍스트와 신뢰도 추출

        Args:
            image (PIL.Image): OCR을 수행할 이미지

        Returns:
            tuple: (텍스트, 평균 신뢰도)
        """
        try:
            # Tesseract 설정
            custom_config = r'--oem 1 --psm 3'

            # OCR 수행 및 상세 정보 추출
            data = pytesseract.image_to_data(
                image,
                lang=self.languages,
                config=custom_config,
                output_type=pytesseract.Output.DICT
            )

            # 텍스트와 신뢰도 계산
            text_parts = []
            confidences = []

            for i, conf in enumerate(data['conf']):
                if int(conf) > 0:  # 신뢰도가 0보다 큰 경우만
                    text = data['text'][i]
                    if text.strip():
                        text_parts.append(text)
                        confidences.append(int(conf))

            full_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            self.logger.info(f"OCR 완료: {len(full_text)} 글자, 평균 신뢰도: {avg_confidence:.2f}%")

            return full_text.strip(), avg_confidence

        except Exception as e:
            self.logger.error(f"OCR 처리 중 오류 발생: {e}")
            raise

    def check_tesseract(self):
        """
        Tesseract 설치 확인

        Returns:
            bool: 설치 여부
        """
        try:
            version = pytesseract.get_tesseract_version()
            self.logger.info(f"Tesseract 버전: {version}")
            return True
        except pytesseract.TesseractNotFoundError:
            self.logger.error("Tesseract가 설치되지 않았습니다")
            return False

    def get_available_languages(self):
        """
        사용 가능한 언어 목록 확인

        Returns:
            list: 언어 코드 리스트
        """
        try:
            languages = pytesseract.get_languages()
            self.logger.info(f"사용 가능한 언어: {languages}")
            return languages
        except Exception as e:
            self.logger.error(f"언어 목록 확인 중 오류: {e}")
            return []

    def validate_languages(self):
        """
        필요한 언어팩 설치 확인

        Returns:
            tuple: (설치 여부, 누락된 언어 리스트)
        """
        try:
            available = self.get_available_languages()
            required = ['kor', 'eng', 'jpn', 'chi_tra']

            missing = [lang for lang in required if lang not in available]

            if missing:
                self.logger.warning(f"누락된 언어팩: {missing}")
                return False, missing
            else:
                self.logger.info("모든 필요한 언어팩이 설치되어 있습니다")
                return True, []

        except Exception as e:
            self.logger.error(f"언어팩 확인 중 오류: {e}")
            return False, []
