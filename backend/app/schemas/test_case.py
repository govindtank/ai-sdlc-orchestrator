"""
Pydantic schemas for Test Case
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TestCaseBase(BaseModel):
    user_story_id: int
    title: str
    description: str
    test_type: str  # functional, edge_case, performance, security, ui
    steps: str
    expected_result: str

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseUpdate(BaseModel):
    user_story_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    test_type: Optional[str] = None
    steps: Optional[str] = None
    expected_result: Optional[str] = None

class TestCaseResponse(TestCaseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True