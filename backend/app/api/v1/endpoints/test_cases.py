"""
Test Case API endpoints with AI generation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db.session import get_db
from app.services.estimate_service import EstimateService

router = APIRouter()
estimate_service = EstimateService()

@router.post("/", response_model=schemas.TestCaseResponse)
def create_test_case(test_case: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    db_test_case = models.TestCase(**test_case.dict())
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@router.get("/", response_model=List[schemas.TestCaseResponse])
def read_test_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    test_cases = db.query(models.TestCase).offset(skip).limit(limit).all()
    return test_cases

@router.get("/{test_case_id}", response_model=schemas.TestCaseResponse)
def read_test_case(test_case_id: int, db: Session = Depends(get_db)):
    test_case = db.query(models.TestCase).filter(models.TestCase.id == test_case_id).first()
    if test_case is None:
        raise HTTPException(status_code=404, detail="Test case not found")
    return test_case

@router.put("/{test_case_id}", response_model=schemas.TestCaseResponse)
def update_test_case(test_case_id: int, test_case: schemas.TestCaseUpdate, db: Session = Depends(get_db)):
    db_test_case = db.query(models.TestCase).filter(models.TestCase.id == test_case_id).first()
    if db_test_case is None:
        raise HTTPException(status_code=404, detail="Test case not found")
    for key, value in test_case.dict(exclude_unset=True).items():
        setattr(db_test_case, key, value)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

@router.delete("/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test_case(test_case_id: int, db: Session = Depends(get_db)):
    db_test_case = db.query(models.TestCase).filter(models.TestCase.id == test_case_id).first()
    if db_test_case is None:
        raise HTTPException(status_code=404, detail="Test case not found")
    db.delete(db_test_case)
    db.commit()
    return None

@router.post("/{user_story_id}/generate-tests", response_model=List[schemas.TestCaseResponse])
def generate_test_cases_from_user_story(user_story_id: int, db: Session = Depends(get_db)):
    """
    Generate test cases from a user story using AI.
    """
    # Get the user story
    user_story = db.query(models.UserStory).filter(models.UserStory.id == user_story_id).first()
    if user_story is None:
        raise HTTPException(status_code=404, detail="User story not found")
    
    # Prepare user story dict for test generation
    story_dict = {
        "title": user_story.title,
        "description": user_story.description,
        "acceptance_criteria": user_story.acceptance_criteria.split("\n") if user_story.acceptance_criteria else []
    }
    
    # Generate test cases using the service
    test_cases_result = estimate_service.generate_test_cases(story_dict)
    
    # Create test case records
    created_test_cases = []
    for tc_data in test_cases_result:
        test_case_data = {
            "user_story_id": user_story_id,
            "title": tc_data["title"],
            "description": tc_data["description"],
            "test_type": tc_data["test_type"],
            "steps": tc_data["steps"],
            "expected_result": tc_data["expected_result"]
        }
        
        db_test_case = models.TestCase(**test_case_data)
        db.add(db_test_case)
        created_test_cases.append(db_test_case)
    
    db.commit()
    
    # Refresh to get IDs
    for tc in created_test_cases:
        db.refresh(tc)
        
    return created_test_cases