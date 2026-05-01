"""
Analytics service for generating insights and reports
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app import models
from app.db.session import get_db

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_project_overview(self, project_id: int) -> Dict[str, Any]:
        """Get overview statistics for a project."""
        # Get project
        project = self.db.query(models.Project).filter(models.Project.id == project_id).first()
        if not project:
            return {}

        # Count requirements by status
        requirements = self.db.query(models.Requirement).filter(
            models.Requirement.project_id == project_id
        ).all()
        req_stats = {
            "total": len(requirements),
            "raw": len([r for r in requirements if r.status == "raw"]),
            "refined": len([r for r in requirements if r.status == "refined"]),
            "clarified": len([r for r in requirements if r.status == "clarified"])
        }

        # Count user stories by status
        user_stories = self.db.query(models.UserStory).filter(
            models.UserStory.project_id == project_id
        ).all()
        story_stats = {
            "total": len(user_stories),
            "draft": len([s for s in user_stories if s.status == "draft"]),
            "estimated": len([s for s in user_stories if s.status == "estimated"]),
            "approved": len([s for s in user_stories if s.status == "approved"])
        }

        # Count test cases
        test_cases = self.db.query(models.TestCase).join(models.UserStory).filter(
            models.UserStory.project_id == project_id
        ).all()

        # Calculate average story points
        estimated_stories = [s for s in user_stories if s.story_points is not None]
        avg_story_points = sum(s.story_points for s in estimated_stories) / len(estimated_stories) if estimated_stories else 0

        # Count design suggestions
        design_suggestions = self.db.query(models.DesignSuggestion).filter(
            models.DesignSuggestion.project_id == project_id
        ).all()

        # Count resource gaps
        resource_gaps = self.db.query(models.ResourceGap).filter(
            models.ResourceGap.project_id == project_id
        ).all()
        gap_stats = {
            "total": len(resource_gaps),
            "open": len([g for g in resource_gaps if g.status == "open"]),
            "in_progress": len([g for g in resource_gaps if g.status == "in_progress"]),
            "resolved": len([g for g in resource_gaps if g.status == "resolved"])
        }

        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at.isoformat() if project.created_at else None
            },
            "requirements": req_stats,
            "user_stories": story_stats,
            "test_cases": {
                "total": len(test_cases)
            },
            "design_suggestions": {
                "total": len(design_suggestions)
            },
            "resource_gaps": gap_stats,
            "estimated_total_story_points": sum(s.story_points for s in estimated_stories) if estimated_stories else 0,
            "average_story_points": round(avg_story_points, 2)
        }

    def get_burndown_data(self, project_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Generate burndown chart data for the last N days."""
        # This is a simplified version - in a real app, you'd track actual completed work over time
        # For now, we'll generate sample data based on estimates
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get total estimated story points
        overview = self.get_project_overview(project_id)
        total_points = overview.get("estimated_total_story_points", 0)
        
        # Generate sample burndown data (linear decrease for demo)
        burndown_data = []
        for i in range(days + 1):
            date = start_date + timedelta(days=i)
            # Simple linear burndown for demo - in reality this would be based on actual completed work
            remaining = max(0, total_points - (total_points * i / days)) if days > 0 else total_points
            
            burndown_data.append({
                "date": date.isoformat(),
                "remaining_story_points": round(remaining, 2),
                "completed_story_points": round(total_points - remaining, 2)
            })
        
        return burndown_data

    def get_velocity_data(self, project_id: int, sprints: int = 6) -> List[Dict[str, Any]]:
        """Generate velocity chart data for the last N sprints."""
        # This would normally come from sprint data
        # For demo, we'll generate sample data
        
        velocity_data = []
        base_velocity = 20  # Sample base velocity
        
        for i in range(sprints):
            # Add some variation to make it look realistic
            variation = (i % 3 - 1) * 2  # -2, 0, 2 pattern
            velocity = max(5, base_velocity + variation)
            
            velocity_data.append({
                "sprint": f"Sprint {sprints - i}",
                "story_points_committed": velocity + 5,  # Usually commit a bit more
                "story_points_completed": velocity
            })
        
        return list(reversed(velocity_data))  # Most recent first

    def get_resource_gap_trends(self, project_id: int) -> Dict[str, Any]:
        """Analyze resource gap trends over time."""
        gaps = self.db.query(models.ResourceGap).filter(
            models.ResourceGap.project_id == project_id
        ).all()
        
        # Group by gap type
        gap_types = {}
        for gap in gaps:
            gap_type = gap.gap_type
            if gap_type not in gap_types:
                gap_types[gap_type] = {"total": 0, "open": 0, "resolved": 0}
            
            gap_types[gap_type]["total"] += 1
            if gap.status == "open":
                gap_types[gap_type]["open"] += 1
            elif gap.status == "resolved":
                gap_types[gap_type]["resolved"] += 1
        
        # Calculate resolution rate
        for gap_type in gap_types:
            total = gap_types[gap_type]["total"]
            resolved = gap_types[gap_type]["resolved"]
            gap_types[gap_type]["resolution_rate"] = round(resolved / total * 100, 2) if total > 0 else 0
        
        return gap_types

    def get_ai_usage_stats(self, project_id: int) -> Dict[str, Any]:
        """Get statistics about AI usage in the project."""
        # This would track actual AI service calls
        # For demo, we'll return placeholder data
        
        return {
            "total_ai_calls": 0,  # Would be tracked in real implementation
            "requirement_refinements": 0,
            "user_story_generations": 0,
            "design_suggestions": 0,
            "test_case_generations": 0,
            "effort_estimations": 0,
            "resource_gap_detections": 0,
            "average_response_time_ms": 0,
            "success_rate_percent": 100.0
        }

    def generate_comprehensive_report(self, project_id: int) -> Dict[str, Any]:
        """Generate a comprehensive project report."""
        overview = self.get_project_overview(project_id)
        burndown = self.get_burndown_data(project_id, 14)  # Last 2 weeks
        velocity = self.get_velocity_data(project_id, 6)   # Last 6 sprints
        gap_trends = self.get_resource_gap_trends(project_id)
        ai_stats = self.get_ai_usage_stats(project_id)
        
        return {
            "project_overview": overview,
            "burndown_chart": burndown,
            "velocity_chart": velocity,
            "resource_gap_trends": gap_trends,
            "ai_usage_statistics": ai_stats,
            "generated_at": datetime.now().isoformat()
        }