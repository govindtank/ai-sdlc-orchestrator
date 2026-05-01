"""
Resource gap intelligence API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db.session import get_db
from app.services.resource_gap_service import ResourceGapService

router = APIRouter()
resource_gap_service = ResourceGapService()

@router.post("/", response_model=schemas.ResourceGapResponse)
def create_resource_gap(resource_gap: schemas.ResourceGapCreate, db: Session = Depends(get_db)):
    db_resource_gap = models.ResourceGap(**resource_gap.dict())
    db.add(db_resource_gap)
    db.commit()
    db.refresh(db_resource_gap)
    return db_resource_gap

@router.get("/", response_model=List[schemas.ResourceGapResponse])
def read_resource_gaps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resource_gaps = db.query(models.ResourceGap).offset(skip).limit(limit).all()
    return resource_gaps

@router.get("/{resource_gap_id}", response_model=schemas.ResourceGapResponse)
def read_resource_gap(resource_gap_id: int, db: Session = Depends(get_db)):
    resource_gap = db.query(models.ResourceGap).filter(models.ResourceGap.id == resource_gap_id).first()
    if resource_gap is None:
        raise HTTPException(status_code=404, detail="Resource gap not found")
    return resource_gap

@router.put("/{resource_gap_id}", response_model=schemas.ResourceGapResponse)
def update_resource_gap(resource_gap_id: int, resource_gap: schemas.ResourceGapUpdate, db: Session = Depends(get_db)):
    db_resource_gap = db.query(models.ResourceGap).filter(models.ResourceGap.id == resource_gap_id).first()
    if db_resource_gap is None:
        raise HTTPException(status_code=404, detail="Resource gap not found")
    for key, value in resource_gap.dict(exclude_unset=True).items():
        setattr(db_resource_gap, key, value)
    db.commit()
    db.refresh(db_resource_gap)
    return db_resource_gap

@router.delete("/{resource_gap_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource_gap(resource_gap_id: int, db: Session = Depends(get_db)):
    db_resource_gap = db.query(models.ResourceGap).filter(models.ResourceGap.id == resource_gap_id).first()
    if db_resource_gap is None:
        raise HTTPException(status_code=404, detail="Resource gap not found")
    db.delete(db_resource_gap)
    db.commit()
    return None

@router.post("/{project_id}/detect-gaps", response_model=List[schemas.ResourceGapResponse])
def detect_resource_gaps_for_project(project_id: int, db: Session = Depends(get_db)):
    """
    Detect resource gaps for a project using AI/heuristics and create gap records.
    """
    # Get the project
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Gather project data for analysis
    requirements = db.query(models.Requirement).filter(models.Requirement.project_id == project_id).all()
    user_stories = db.query(models.UserStory).filter(models.UserStory.project_id == project_id).all()
    design_suggestions = db.query(models.DesignSuggestion).filter(models.DesignSuggestion.project_id == project_id).all()
    test_cases = db.query(models.TestCase).join(models.UserStory).filter(models.UserStory.project_id == project_id).all()
    
    # Prepare data dict for gap detection
    project_data = {
        "requirements": [
            {
                "raw_text": req.raw_text,
                "refined_text": req.refined_text,
                "clarification_questions": req.clarification_questions
            }
            for req in requirements
        ],
        "user_stories": [
            {
                "id": story.id,
                "title": story.title,
                "description": story.description,
                "acceptance_criteria": story.acceptance_criteria,
                "story_points": story.story_points
            }
            for story in user_stories
        ],
        "design_suggestions": [
            {
                "id": ds.id,
                "user_story_id": ds.user_story_id,
                "wireframe_description": ds.wireframe_description,
                "ui_component_suggestions": ds.ui_component_suggestions,
                "design_notes": ds.design_notes
            }
            for ds in design_suggestions
        ],
        "test_cases": [
            {
                "id": tc.id,
                "user_story_id": tc.user_story_id,
                "title": tc.title,
                "description": tc.description,
                "test_type": tc.test_type,
                "steps": tc.steps,
                "expected_result": tc.expected_result
            }
            for tc in test_cases
        ]
    }
    
    # Detect gaps using the service
    gaps_result = resource_gap_service.detect_resource_gaps(project_data)
    
    # Create resource gap records
    created_gaps = []
    for gap_data in gaps_result:
        gap_data["project_id"] = project_id
        db_resource_gap = models.ResourceGap(**gap_data)
        db.add(db_resource_gap)
        created_gaps.append(db_resource_gap)
    
    db.commit()
    
    # Refresh to get IDs
    for gap in created_gaps:
        db.refresh(gap)
        
    return created_gaps

@router.post("/{resource_gap_id}/recommendations", response_model=schemas.ResourceGapRecommendationResponse)
def get_resource_gap_recommendations(resource_gap_id: int, db: Session = Depends(get_db)):
    """
    Get recommendations for obtaining missing resources for a specific gap.
    """
    resource_gap = db.query(models.ResourceGap).filter(models.ResourceGap.id == resource_gap_id).first()
    if resource_gap is None:
        raise HTTPException(status_code=404, detail="Resource gap not found")
    
    # Get recommendations using the service
    gap_data = {
        "gap_type": resource_gap.gap_type,
        "description": resource_gap.description
    }
    recommendations = resource_gap_service.get_resource_recommendations(gap_data)
    
    return recommendations