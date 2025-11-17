"""
Watchlist (관심 목록) API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.api.schemas.stock import WatchlistAdd, WatchlistUpdate, WatchlistItem
from loguru import logger

router = APIRouter(prefix="/api/v1/watchlist", tags=["Watchlist"])


# 임시 인메모리 저장소 (실제로는 DB 사용)
_watchlist_db: List[dict] = []
_id_counter = 1


@router.get("/", response_model=List[WatchlistItem])
async def get_watchlist(user_id: int = 1):
    """
    사용자의 관심 목록 조회

    Args:
        user_id: 사용자 ID (현재는 하드코딩, 실제로는 JWT 인증)

    Returns:
        관심 목록 항목들
    """
    try:
        user_items = [item for item in _watchlist_db if item["user_id"] == user_id]
        return user_items

    except Exception as e:
        logger.error(f"Error in get_watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=201)
async def add_to_watchlist(item: WatchlistAdd, user_id: int = 1):
    """
    관심 목록에 종목 추가 (⭐️ 찜하기)

    Args:
        item: 추가할 종목 정보
        user_id: 사용자 ID
    """
    global _id_counter

    try:
        # 중복 체크
        existing = next(
            (i for i in _watchlist_db if i["user_id"] == user_id and i["ticker"] == item.ticker),
            None
        )

        if existing:
            raise HTTPException(status_code=400, detail="이미 관심 목록에 있는 종목입니다.")

        new_item = {
            "id": _id_counter,
            "user_id": user_id,
            "ticker": item.ticker,
            "company_name": item.company_name,
            "memo": item.memo,
            "current_price": None,  # 백그라운드 작업으로 업데이트
            "change_percent": None,
            "added_at": "2025-11-17T10:00:00Z"
        }

        _watchlist_db.append(new_item)
        _id_counter += 1

        return {"message": "관심 목록에 추가되었습니다.", "item": new_item}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in add_to_watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{item_id}")
async def update_watchlist_item(item_id: int, update: WatchlistUpdate, user_id: int = 1):
    """
    관심 목록 항목 업데이트 (메모 수정)
    """
    try:
        item = next((i for i in _watchlist_db if i["id"] == item_id and i["user_id"] == user_id), None)

        if not item:
            raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다.")

        if update.memo is not None:
            item["memo"] = update.memo

        return {"message": "업데이트되었습니다.", "item": item}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_watchlist_item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}")
async def delete_from_watchlist(item_id: int, user_id: int = 1):
    """
    관심 목록에서 종목 제거
    """
    global _watchlist_db

    try:
        item = next((i for i in _watchlist_db if i["id"] == item_id and i["user_id"] == user_id), None)

        if not item:
            raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다.")

        _watchlist_db = [i for i in _watchlist_db if i["id"] != item_id]

        return {"message": "관심 목록에서 제거되었습니다."}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_from_watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))
