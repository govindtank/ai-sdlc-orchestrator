"""
Design Suggestion API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db.session import get_db
from app.services.design_service import DesignService

router = APIRouter()
design_service = DesignService()

@router.post("/", response_model=schemas.DesignSuggestionResponse)
def create_design_suggestion(design_suggestion: schemas.DesignSuggestionCreate, db: Session = Depends(get_db)):
    db_design_suggestion = models.DesignSuggestion(**design_suggestion.dict())
    db.add(db_design_suggestion)
    db.commit()
    db.refresh(db_design_suggestion)
    return db_design_suggestion

@router.get("/", response_model=List[schemas.DesignSuggestionResponse])
def read_design_suggestions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    design_suggestions = db.query(models.DesignSuggestion).offset(skip).limit(limit).all()
    return design_suggestions

@router.get("/{design_suggestion_id}", response_model=schemas.DesignSuggestionResponse)
def read_design_suggestion(design_suggestion_id: int, db: Session = Depends(get_db)):
    design_suggestion = db.query(models.DesignSuggestion).filter(models.DesignSuggestion.id == design_suggestion_id).first()
    if design_suggestion is None:
        raise HTTPException(status_code=404, detail="Design suggestion not found")
    return design_suggestion

@router.put("/{design_suggestion_id}", response_model=schemas.DesignSuggestionResponse)
def update_design_suggestion(design_suggestion_id: int, design_suggestion: schemas.DesignSuggestionUpdate, db: Session = Depends(get_db)):
    db_design_suggestion = db.query(models.DesignSuggestion).filter(models.DesignSuggestion.id == design_suggestion_id).first()
    if db_design_suggestion is None:
        raise HTTPException(status_code=404, detail="Design suggestion not found")
    for key, value in design_suggestion.dict(exclude_unset=True).items():
        setattr(db_design_suggestion, key, value)
    db.commit()
    db.refresh(db_design_suggestion)
    return db_design_suggestion

@router.delete("/{design_suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_design_suggestion(design_suggestion_id: int, db: Session = Depends(get_db)):
    db_design_suggestion = db.query(models.DesignSuggestion).filter(models.DesignSuggestion.id == design_suggestion_id).first()
    if db_design_suggestion is None:
        raise HTTPException(status_code=404, detail="Design suggestion not found")
    db.delete(db_design_suggestion)
    db.commit()
    return None

@router.post("/{user_story_id}/generate-design", response_model=schemas.DesignSuggestionResponse)
def generate_design_suggestion_from_user_story(user_story_id: int, db: Session = Depends(get_db)):
    """
    Generate a design suggestion from a user story using AI.
    """
    # Get the user story
    user_story = db.query(models.UserStory).filter(models.UserStory.id == user_story_id).first()
    if user_story is None:
        raise HTTPException(status_code=404, detail="User story not found")
    
    # Prepare user story dict for design generation
    story_dict = {
        "title": user_story.title,
        "description": user_story.description,
        "acceptance_criteria": user_story.acceptance_criteria.split("\n") if user_story.acceptance_criteria else []
    }
    
    # Generate design suggestion using the service
    design_result = design_service.generate_design_suggestion(story_dict)
    
    # Create the design suggestion
    design_suggestion_data = {
        "user_story_id": user_story_id,
        "project_id": user_story.project_id,
        "wireframe_description": design_result["wireframe_description"],
        "ui_component_suggestions": design_result["ui_component_suggestions"],
        "design_notes": design_result["design_notes"],
        "status": "generated"
    }
    
    db_design_suggestion = models.DesignSuggestion(**design_suggestion_data)
    db.add(db_design_suggestion)
    db.commit()
    db.refresh(db_design_suggestion)
    return db_design_suggestion