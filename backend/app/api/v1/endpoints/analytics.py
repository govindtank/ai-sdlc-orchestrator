"""
Analytics API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.db.session import get_db
from app.services.analytics_service import AnalyticsService
from app.core.security.deps import get_current_active_user

router = APIRouter()

@router.get("/project/{project_id}/overview", response_model=schemas.ProjectOverviewResponse)
def get_project_overview(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get overview statistics for a project."""
    # Verify user has access to this project (simplified check)
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    analytics_service = AnalyticsService(db)
    overview = analytics_service.get_project_overview(project_id)
    return overview

@router.get("/project/{project_id}/burndown", response_model=List[schemas.BurndownDataPoint])
def get_burndown_data(
    project_id: int,
    days: Optional[int] = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get burndown chart data for a project."""
    # Verify user has access to this project
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    analytics_service = AnalyticsService(db)
    burndown_data = analytics_service.get_burndown_data(project_id, days)
    return burndown_data

@router.get("/project/{project_id}/velocity", response_model=List[schemas.VelocityDataPoint])
def get_velocity_data(
    project_id: int,
    sprints: Optional[int] = 6,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get velocity chart data for a project."""
    # Verify user has access to this project
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    analytics_service = AnalyticsService(db)
    velocity_data = analytics_service.get_velocity_data(project_id, sprints)
    return velocity_data

@router.get("/project/{project_id}/gap-trends", response_model=schemas.ResourceGapTrendsResponse)
def get_resource_gap_trends(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get resource gap trends for a project."""
    # Verify user has access to this project
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    analytics_service = AnalyticsService(db)
    gap_trends = analytics_service.get_resource_gap_trends(project_id)
    return gap_trends

@router.get("/project/{project_id}/ai-stats", response_model=schemas.AIUsageStatsResponse)
def get_ai_usage_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get AI usage statistics for a project."""
    # Verify user has access to this project
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    analytics_service = AnalyticsService(db)
    ai_stats = analytics_service.get_ai_usage_stats(project_id)
    return ai_stats

@router.get("/project/{project_id}/report", response_model=schemas.ComprehensiveReportResponse)
def get_comprehensive_report(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get a comprehensive report for a project."""
    # Verify user has access to this project
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    analytics_service = AnalyticsService(db)
    report = analytics_service.generate_comprehensive_report(project_id)
    return report