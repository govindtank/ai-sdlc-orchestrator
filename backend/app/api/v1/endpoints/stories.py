"""
User Story API endpoints with AI generation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db.session import get_db
from app.services.story_service import StoryService

router = APIRouter()
story_service = StoryService()

@router.post("/", response_model=schemas.UserStoryResponse)
def create_user_story(user_story: schemas.UserStoryCreate, db: Session = Depends(get_db)):
    db_user_story = models.UserStory(**user_story.dict())
    db.add(db_user_story)
    db.commit()
    db.refresh(db_user_story)
    return db_user_story

@router.get("/", response_model=List[schemas.UserStoryResponse])
def read_user_stories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_stories = db.query(models.UserStory).offset(skip).limit(limit).all()
    return user_stories

@router.get("/{user_story_id}", response_model=schemas.UserStoryResponse)
def read_user_story(user_story_id: int, db: Session = Depends(get_db)):
    user_story = db.query(models.UserStory).filter(models.UserStory.id == user_story_id).first()
    if user_story is None:
        raise HTTPException(status_code=404, detail="User story not found")
    return user_story

@router.put("/{user_story_id}", response_model=schemas.UserStoryResponse)
def update_user_story(user_story_id: int, user_story: schemas.UserStoryUpdate, db: Session = Depends(get_db)):
    db_user_story = db.query(models.UserStory).filter(models.UserStory.id == user_story_id).first()
    if db_user_story is None:
        raise HTTPException(status_code=404, detail="User story not found")
    for key, value in user_story.dict(exclude_unset=True).items():
        setattr(db_user_story, key, value)
    db.commit()
    db.refresh(db_user_story)
    return db_user_story

@router.delete("/{user_story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_story(user_story_id: int, db: Session = Depends(get_db)):
    db_user_story = db.query(models.UserStory).filter(models.UserStory.id == user_story_id).first()
    if db_user_story is None:
        raise HTTPException(status_code=404, detail="User story not found")
    db.delete(db_user_story)
    db.commit()
    return None

@router.post("/{requirement_id}/generate-story", response_model=schemas.UserStoryResponse)
def generate_user_story_from_requirement(requirement_id: int, db: Session = Depends(get_db)):
    """
    Generate a user story from a refined requirement using AI.
    """
    # Get the requirement
    requirement = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).first()
    if requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    # Check if requirement is refined
    if not requirement.refined_text:
        raise HTTPException(status_code=400, detail="Requirement must be refined before generating user story")
    
    # Generate user story using the service
    story_result = story_service.generate_user_story(requirement.refined_text)
    
    # Create the user story
    user_story_data = {
        "project_id": requirement.project_id,
        "requirement_id": requirement_id,
        "title": story_result["title"],
        "description": story_result["description"],
        "acceptance_criteria": "\n".join([f"- {ac}" for ac in story_result["acceptance_criteria"]]) if story_result["acceptance_criteria"] else None,
        "status": "draft"
    }
    
    db_user_story = models.UserStory(**user_story_data)
    db.add(db_user_story)
    db.commit()
    db.refresh(db_user_story)
    return db_user_story

@router.post("/{user_story_id}/estimate", response_model=schemas.UserStoryResponse)
def estimate_user_story_effort(user_story_id: int, db: Session = Depends(get_db)):
    """
    Estimate effort for a user story using AI/heuristics and update the story with story points.
    """
    # Get the user story
    user_story = db.query(models.UserStory).filter(models.UserStory.id == user_story_id).first()
    if user_story is None:
        raise HTTPException(status_code=404, detail="User story not found")
    
    # Prepare user story dict for estimation
    story_dict = {
        "title": user_story.title,
        "description": user_story.description,
        "acceptance_criteria": user_story.acceptance_criteria.split("\n") if user_story.acceptance_criteria else []
    }
    
    # Estimate effort using the service
    estimate_result = story_service.estimate_effort(story_dict)
    
    # Update the user story
    user_story.story_points = estimate_result["story_points"]
    user_story.status = "estimated"
    
    db.commit()
    db.refresh(user_story)
    return user_story