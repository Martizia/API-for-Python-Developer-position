from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository.analytics import (
    get_comments_daily_breakdown,
    get_posts_daily_breakdown,
)
from src.schemas.analytics import AnalyticsDailyBreakdownResponse
from datetime import datetime

router = APIRouter(tags=["Analytics"])


@router.get("/posts-daily-breakdown", response_model=AnalyticsDailyBreakdownResponse)
async def posts_daily_breakdown(
    date_from: datetime = Query(..., description="Start date"),
    date_to: datetime = Query(..., description="End date"),
    db: AsyncSession = Depends(get_db),
):
    breakdown = await get_posts_daily_breakdown(db, date_from, date_to)
    return {
        "breakdown": [
            {
                "date": row.date,
                "created_count": row.created_count,
                "blocked_count": row.blocked_count,
            }
            for row in breakdown
        ]
    }


@router.get("/comments-daily-breakdown", response_model=AnalyticsDailyBreakdownResponse)
async def comments_daily_breakdown(
    date_from: datetime = Query(..., description="Start date"),
    date_to: datetime = Query(..., description="End date"),
    db: AsyncSession = Depends(get_db),
):
    breakdown = await get_comments_daily_breakdown(db, date_from, date_to)
    return {
        "breakdown": [
            {
                "date": row.date,
                "created_count": row.created_count,
                "blocked_count": row.blocked_count,
            }
            for row in breakdown
        ]
    }
