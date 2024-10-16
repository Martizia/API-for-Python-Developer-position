from pydantic import BaseModel
from datetime import datetime


class AnalyticsDailyBreakdown(BaseModel):
    date: datetime
    created_count: int
    blocked_count: int


class AnalyticsDailyBreakdownResponse(BaseModel):
    breakdown: list[AnalyticsDailyBreakdown]
