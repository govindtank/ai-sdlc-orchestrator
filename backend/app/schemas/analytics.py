"""
Analytics API schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProjectOverviewResponse(BaseModel):
    project: Dict[str, Any]
    requirements: Dict[str, int]
    user_stories: Dict[str, int]
    test_cases: Dict[str, int]
    design_suggestions: Dict[str, int]
    resource_gaps: Dict[str, int]
    estimated_total_story_points: float
    average_story_points: float

class BurndownDataPoint(BaseModel):
    date: str
    remaining_story_points: float
    completed_story_points: float

class VelocityDataPoint(BaseModel):
    sprint: str
    story_points_committed: float
    story_points_completed: float

class ResourceGapTrendsResponse(BaseModel):
    [str]: Dict[str, Any]  # Dynamic keys for gap types

class AIUsageStatsResponse(BaseModel):
    total_ai_calls: int
    requirement_refinements: int
    user_story_generations: int
    design_suggestions: int
    test_case_generations: int
    effort_estimations: int
    resource_gap_detections: int
    average_response_time_ms: float
    success_rate_percent: float

class ComprehensiveReportResponse(BaseModel):
    project_overview: ProjectOverviewResponse
    burndown_chart: List[BurndownDataPoint]
    velocity_chart: List[VelocityDataPoint]
    resource_gap_trends: ResourceGapTrendsResponse
    ai_usage_statistics: AIUsageStatsResponse
    generated_at: str