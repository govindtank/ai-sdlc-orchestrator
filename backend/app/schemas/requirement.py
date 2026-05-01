"""
Pydantic schemas for Requirement
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequirementBase(BaseModel):
    raw_text: str
    refined_text: Optional[str] = None
    clarification_questions: Optional[str] = None
    status: Optional[str] = "raw"

class RequirementCreate(RequirementBase):
    pass

class RequirementUpdate(BaseModel):
    raw_text: Optional[str] = None
    refined_text: Optional[str] = None
    clarification_questions: Optional[str] = None
    status: Optional[str] = None

class RequirementResponse(RequirementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True