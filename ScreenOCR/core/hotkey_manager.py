"""
전역 핫키 관리자
keyboard 라이브러리를 사용한 전역 단축키 감지
"""
import keyboard
import logging
from typing import Callable


class HotkeyManager:
    """전역 핫키 관리 클래스"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.space_callback = None
        self.esc_callback = None
        self.enabled = True

    def register_space_hotkey(self, callback: Callable):
        """
        스페이스바 핫키 등록

        Args:
            callback: 스페이스바 눌렀을 때 실행할 콜백 함수
        """
        self.space_callback = callback

        try:
            # 스페이스바 핫키 등록 (다른 앱에서도 감지)
            keyboard.add_hotkey('space', self._on_space_pressed, suppress=False)
            self.logger.info("스페이스바 핫키 등록 완료")
        except Exception as e:
            self.logger.error(f"스페이스바 핫키 등록 실패: {e}")

    def register_esc_hotkey(self, callback: Callable):
        """
        ESC 키 핫키 등록

        Args:
            callback: ESC 키 눌렀을 때 실행할 콜백 함수
        """
        self.esc_callback = callback

        try:
            # ESC 키 핫키 등록
            keyboard.add_hotkey('esc', self._on_esc_pressed, suppress=False)
            self.logger.info("ESC 핫키 등록 완료")
        except Exception as e:
            self.logger.error(f"ESC 핫키 등록 실패: {e}")

    def _on_space_pressed(self):
        """스페이스바 눌림 이벤트 처리"""
        if self.enabled and self.space_callback:
            self.logger.info("스페이스바 감지됨")
            try:
                self.space_callback()
            except Exception as e:
                self.logger.error(f"스페이스바 콜백 실행 중 오류: {e}")

    def _on_esc_pressed(self):
        """ESC 키 눌림 이벤트 처리"""
        if self.enabled and self.esc_callback:
            self.logger.info("ESC 키 감지됨")
            try:
                self.esc_callback()
            except Exception as e:
                self.logger.error(f"ESC 콜백 실행 중 오류: {e}")

    def enable(self):
        """핫키 활성화"""
        self.enabled = True
        self.logger.info("핫키 활성화")

    def disable(self):
        """핫키 비활성화"""
        self.enabled = False
        self.logger.info("핫키 비활성화")

    def unregister_all(self):
        """모든 핫키 등록 해제"""
        try:
            keyboard.unhook_all()
            self.logger.info("모든 핫키 등록 해제")
        except Exception as e:
            self.logger.error(f"핫키 등록 해제 실패: {e}")

    def is_enabled(self):
        """
        핫키 활성화 상태 확인

        Returns:
            bool: 활성화 여부
        """
        return self.enabled
