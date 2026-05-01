"""
Pydantic schemas for Estimate
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EstimateBase(BaseModel):
    user_story_id: int
    story_points: int
    confidence: Optional[str] = None
    method: Optional[str] = None
    notes: Optional[str] = None

class EstimateCreate(EstimateBase):
    pass

class EstimateUpdate(BaseModel):
    user_story_id: Optional[int] = None
    story_points: Optional[int] = None
    confidence: Optional[str] = None
    method: Optional[str] = None
    notes: Optional[str] = None

class EstimateResponse(EstimateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True