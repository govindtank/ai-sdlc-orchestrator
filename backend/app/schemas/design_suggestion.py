"""
Pydantic schemas for Design Suggestion
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DesignSuggestionBase(BaseModel):
    user_story_id: int
    wireframe_description: Optional[str] = None
    ui_component_suggestions: Optional[List[str]] = None
    design_notes: Optional[str] = None
    status: Optional[str] = None

class DesignSuggestionCreate(DesignSuggestionBase):
    pass

class DesignSuggestionUpdate(BaseModel):
    user_story_id: Optional[int] = None
    wireframe_description: Optional[str] = None
    ui_component_suggestions: Optional[List[str]] = None
    design_notes: Optional[str] = None
    status: Optional[str] = None

class DesignSuggestionResponse(DesignSuggestionBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True