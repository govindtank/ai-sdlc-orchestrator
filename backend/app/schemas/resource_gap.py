"""
Pydantic schemas for Resource Gap
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResourceGapBase(BaseModel):
    project_id: int
    gap_type: str  # requirement, design, data, api, asset, user_story, estimation, testing
    description: str
    suggested_solution: str
    severity: str  # low, medium, high
    status: Optional[str] = None

class ResourceGapCreate(ResourceGapBase):
    pass

class ResourceGapUpdate(BaseModel):
    project_id: Optional[int] = None
    gap_type: Optional[str] = None
    description: Optional[str] = None
    suggested_solution: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None

class ResourceGapResponse(ResourceGapBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True