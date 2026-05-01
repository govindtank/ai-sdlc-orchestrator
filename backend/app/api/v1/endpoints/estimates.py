"""
Effort Estimation API endpoints with AI/heuristic estimation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db.session import get_db
from app.services.estimate_service import EstimateService

router = APIRouter()
estimate_service = EstimateService()

@router.post("/", response_model=schemas.EstimateResponse)
def create_estimate(estimate: schemas.EstimateCreate, db: Session = Depends(get_db)):
    db_estimate = models.Estimate(**estimate.dict())
    db.add(db_estimate)
    db.commit()
    db.refresh(db_estimate)
    return db_estimate

@router.get("/", response_model=List[schemas.EstimateResponse])
def read_estimates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    estimates = db.query(models.Estimate).offset(skip).limit(limit).all()
    return estimates

@router.get("/{estimate_id}", response_model=schemas.EstimateResponse)
def read_estimate(estimate_id: int, db: Session = Depends(get_db)):
    estimate = db.query(models.Estimate).filter(models.Estimate.id == estimate_id).first()
    if estimate is None:
        raise HTTPException(status_code=404, detail="Estimate not found")
    return estimate

@router.put("/{estimate_id}", response_model=schemas.EstimateResponse)
def update_estimate(estimate_id: int, estimate: schemas.EstimateUpdate, db: Session = Depends(get_db)):
    db_estimate = db.query(models.Estimate).filter(models.Estimate.id == estimate_id).first()
    if db_estimate is None:
        raise HTTPException(status_code=404, detail="Estimate not found")
    for key, value in estimate.dict(exclude_unset=True).items():
        setattr(db_estimate, key, value)
    db.commit()
    db.refresh(db_estimate)
    return db_estimate

@router.delete("/{estimate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estimate(estimate_id: int, db: Session = Depends(get_db)):
    db_estimate = db.query(models.Estimate).filter(models.Estimate.id == estimate_id).first()
    if db_estimate is None:
        raise HTTPException(status_code=404, detail="Estimate not found")
    db.delete(db_estimate)
    db.commit()
    return None

@router.post("/{user_story_id}/estimate", response_model=schemas.EstimateResponse)
def estimate_user_story(user_story_id: int, db: Session = Depends(get_db)):
    """
    Estimate effort for a user story using AI/heuristics and create an estimate record.
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
    estimate_result = estimate_service.estimate_effort(story_dict)
    
    # Create the estimate record
    estimate_data = {
        "user_story_id": user_story_id,
        "story_points": estimate_result["story_points"],
        "confidence": estimate_result["confidence"],
        "method": estimate_result["method"],
        "notes": f"Estimated using {estimate_result['method']} method with {estimate_result['confidence']} confidence."
    }
    
    db_estimate = models.Estimate(**estimate_data)
    db.add(db_estimate)
    db.commit()
    db.refresh(db_estimate)
    return db_estimate