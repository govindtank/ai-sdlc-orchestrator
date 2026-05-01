"""
Requirement API endpoints with AI refinement
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db.session import get_db
from app.services.requirement_service import RequirementService

router = APIRouter()
requirement_service = RequirementService()

@router.post("/", response_model=schemas.RequirementResponse)
def create_requirement(requirement: schemas.RequirementCreate, db: Session = Depends(get_db)):
    db_requirement = models.Requirement(**requirement.dict())
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@router.get("/", response_model=List[schemas.RequirementResponse])
def read_requirements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requirements = db.query(models.Requirement).offset(skip).limit(limit).all()
    return requirements

@router.get("/{requirement_id}", response_model=schemas.RequirementResponse)
def read_requirement(requirement_id: int, db: Session = Depends(get_db)):
    requirement = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).first()
    if requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return requirement

@router.put("/{requirement_id}", response_model=schemas.RequirementResponse)
def update_requirement(requirement_id: int, requirement: schemas.RequirementUpdate, db: Session = Depends(get_db)):
    db_requirement = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    for key, value in requirement.dict(exclude_unset=True).items():
        setattr(db_requirement, key, value)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requirement(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    db.delete(db_requirement)
    db.commit()
    return None

@router.post("/{requirement_id}/refine", response_model=schemas.RequirementResponse)
def refine_requirement(requirement_id: int, db: Session = Depends(get_db)):
    """
    Refine a requirement using AI and update the requirement with refined text and clarification questions.
    """
    db_requirement = db.query(models.Requirement).filter(models.Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    # Refine the requirement using the service
    refinement_result = requirement_service.refine_requirement(db_requirement.raw_text)
    
    # Update the requirement
    db_requirement.refined_text = refinement_result["refined_text"]
    db_requirement.clarification_questions = refinement_result["clarification_questions"]
    db_requirement.status = "refined"
    
    db.commit()
    db.refresh(db_requirement)
    return db_requirement