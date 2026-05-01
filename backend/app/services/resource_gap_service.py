"""
Resource gap intelligence service for detecting missing information
"""
import logging
import re
from app.services.llm_provider import get_llm_provider

logger = logging.getLogger(__name__)

class ResourceGapService:
    def __init__(self):
        self.llm_provider = get_llm_provider()
        if not self.llm_provider.is_available():
            logger.warning("LLM provider is not available. Using mock responses.")

    def detect_resource_gaps(self, project_data: dict) -> list:
        """
        Detect missing resources or information in project data.
        Returns a list of detected gaps with suggested solutions.
        """
        gaps = []
        
        # Check requirements
        requirements = project_data.get("requirements", [])
        for req in requirements:
            if not req.get("refined_text"):
                gaps.append({
                    "gap_type": "requirement",
                    "description": f"Requirement '{req.get('raw_text', '')[:50]}...' needs refinement",
                    "suggested_solution": "Use AI refinement service to clarify and improve the requirement",
                    "severity": "medium"
                })
            elif req.get("refined_text") and not req.get("clarification_questions"):
                # Even refined requirements might benefit from explicit clarification check
                pass  # This is okay
        
        # Check user stories
        user_stories = project_data.get("user_stories", [])
        for story in user_stories:
            if not story.get("title") or not story.get("description"):
                gaps.append({
                    "gap_type": "user_story",
                    "description": f"User story is incomplete: missing title or description",
                    "suggested_solution": "Generate user story from requirement using AI service",
                    "severity": "high"
                })
            elif not story.get("acceptance_criteria"):
                gaps.append({
                    "gap_type": "acceptance_criteria",
                    "description": f"User story '{story.get('title', '')}' missing acceptance criteria",
                    "suggested_solution": "Generate acceptance criteria using AI service",
                    "severity": "medium"
                })
            elif not story.get("story_points"):
                gaps.append({
                    "gap_type": "estimation",
                    "description": f"User story '{story.get('title', '')}' missing effort estimation",
                    "suggested_solution": "Estimate effort using AI/heuristic service",
                    "severity": "medium"
                })
        
        # Check for design suggestions
        design_suggestions = project_data.get("design_suggestions", [])
        user_story_ids_with_design = {ds.get("user_story_id") for ds in design_suggestions if ds.get("user_story_id")}
        for story in user_stories:
            if story.get("id") and story["id"] not in user_story_ids_with_design:
                gaps.append({
                    "gap_type": "design",
                    "description": f"User story '{story.get('title', '')}' missing design suggestions",
                    "suggested_solution": "Generate design suggestions using AI service",
                    "severity": "low"
                })
        
        # Check for test cases
        test_cases = project_data.get("test_cases", [])
        user_story_ids_with_tests = {tc.get("user_story_id") for tc in test_cases if tc.get("user_story_id")}
        for story in user_stories:
            if story.get("id") and story["id"] not in user_story_ids_with_tests:
                gaps.append({
                    "gap_type": "testing",
                    "description": f"User story '{story.get('title', '')}' missing test cases",
                    "suggested_solution": "Generate test cases using AI service",
                    "severity": "medium"
                })
        
        # Use LLM for deeper analysis if available
        if self.llm_provider.is_available() and len(gaps) < 3:  # Only use LLM if we have few gaps already
            try:
                llm_gaps = self._detect_gaps_with_llm(project_data)
                # Merge LLM gaps, avoiding duplicates
                existing_descriptions = {gap["description"] for gap in gaps}
                for gap in llm_gaps:
                    if gap["description"] not in existing_descriptions:
                        gaps.append(gap)
            except Exception as e:
                logger.debug(f"LLM gap detection failed: {e}")
        
        return gaps

    def _detect_gaps_with_llm(self, project_data: dict) -> list:
        """
        Use LLM to detect more subtle resource gaps.
        """
        # Prepare a summary of the project for analysis
        req_summary = []
        for req in project_data.get("requirements", [])[:3]:  # Limit to avoid token issues
            req_summary.append(f"- Raw: {req.get('raw_text', '')[:100]}...")
            if req.get("refined_text"):
                req_summary.append(f"  Refined: {req.get('refined_text', '')[:100]}...")
        
        story_summary = []
        for story in project_data.get("user_stories", [])[:3]:
            story_summary.append(f"- Title: {story.get('title', '')}")
            story_summary.append(f"  Description: {story.get('description', '')[:100]}...")
            if story.get("acceptance_criteria"):
                story_summary.append(f"  AC: {story.get('acceptance_criteria', '')[:100]}...")
        
        prompt = f"""
You are an experienced project manager reviewing a software project for completeness.
Analyze the following project artifacts and identify any missing information, resources, or artifacts that would be needed to proceed with development.

Requirements:
{chr(10).join(req_summary) if req_summary else "No requirements provided"}

User Stories:
{chr(10).join(story_summary) if story_summary else "No user stories provided"}

Please identify gaps in the following categories:
1. Missing or unclear requirements
2. Missing user story details (title, description, acceptance criteria)
3. Missing effort estimations
4. Missing design considerations (wireframes, UI components)
5. Missing test strategies or test cases
6. Missing technical specifications (API contracts, data models, tech stack)
7. Missing resource information (skills needed, external dependencies)
8. Missing compliance or security considerations

For each gap identified, provide:
- Gap type (from the categories above)
- Description of what's missing
- Suggested solution to obtain/create the missing item
- Severity (low, medium, high)

Format your response as:
GAP:
Type: [gap type]
Description: [description]
Solution: [suggested solution]
Severity: [low/medium/high]

[Repeat for each gap]
"""
        try:
            response = self.llm_provider.generate(prompt, max_tokens=1500, temperature=0.3)
            
            # Parse the response
            gaps = []
            current_gap = {}
            
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("GAP:") or line.startswith("Type:"):
                    # Save previous gap if exists
                    if current_gap and "type" in current_gap:
                        gaps.append({
                            "gap_type": current_gap.get("type", "").lower().replace(" ", "_"),
                            "description": current_gap.get("description", ""),
                            "suggested_solution": current_gap.get("solution", ""),
                            "severity": current_gap.get("severity", "medium").lower()
                        })
                    current_gap = {}
                    if line.startswith("Type:"):
                        current_gap["type"] = line.replace("Type:", "").strip()
                elif line.startswith("Description:"):
                    current_gap["description"] = line.replace("Description:", "").strip()
                elif line.startswith("Solution:"):
                    current_gap["solution"] = line.replace("Solution:", "").strip()
                elif line.startswith("Severity:"):
                    current_gap["severity"] = line.replace("Severity:", "").strip()
            
            # Save last gap
            if current_gap and "type" in current_gap:
                gaps.append({
                    "gap_type": current_gap.get("type", "").lower().replace(" ", "_"),
                    "description": current_gap.get("description", ""),
                    "suggested_solution": current_gap.get("solution", ""),
                    "severity": current_gap.get("severity", "medium").lower()
                })
                
            return gaps
        except Exception as e:
            logger.error(f"Error in LLM gap detection: {e}")
            return []

    def get_resource_recommendations(self, gap: dict) -> dict:
        """
        Get specific recommendations for obtaining missing resources.
        """
        gap_type = gap.get("gap_type", "")
        description = gap.get("description", "")
        
        # Base recommendations
        recommendations = {
            "requirement": {
                "actions": [
                    "Schedule a requirements workshop with stakeholders",
                    "Use AI refinement service to clarify ambiguous requirements",
                    "Create user personas to better understand needs"
                ],
                "resources": [
                    "Stakeholder availability",
                    "Domain expertise",
                    "Requirements gathering templates"
                ]
            },
            "user_story": {
                "actions": [
                    "Generate user story from requirement using AI service",
                    "Follow INVEST criteria for good user stories",
                    "Break large stories into smaller, manageable ones"
                ],
                "resources": [
                    "Product manager or business analyst",
                    "User story mapping tools",
                    "Acceptance criteria examples"
                ]
            },
            "estimation": {
                "actions": [
                    "Use AI/heuristic estimation service",
                    "Planning poker with development team",
                    "Reference similar completed stories for analogy"
                ],
                "resources": [
                    "Development team availability",
                    "Historical velocity data",
                    "Estimation planning cards or tools"
                ]
            },
            "design": {
                "actions": [
                    "Generate design suggestions using AI service",
                    "Create low-fidelity wireframes first",
                    "Review with stakeholders for feedback"
                ],
                "resources": [
                    "UX/UI designer or design tools",
                    "UI component library (e.g., Material-UI, Ant Design)",
                    "Prototyping tools (Figma, Sketch, Adobe XD)"
                ]
            },
            "testing": {
                "actions": [
                    "Generate test cases using AI service",
                    "Define test strategy (unit, integration, UI, performance)",
                    "Set up test environment and test data management"
                ],
                "resources": [
                    "QA engineer or testing expertise",
                    "Testing frameworks (Jest, PyTest, Selenium)",
                    "Test data generation tools"
                ]
            },
            "design": {
                "actions": [
                    "Generate design suggestions using AI service",
                    "Create low-fidelity wireframes first",
                    "Review with stakeholders for feedback"
                ],
                "resources": [
                    "UX/UI designer or design tools",
                    "UI component library (e.g., Material-UI, Ant Design)",
                    "Prototyping tools (Figma, Sketch, Adobe XD)"
                ]
            }
        }
        
        # Return specific recommendations or fallback
        return recommendations.get(gap_type, {
            "actions": [
                "Consult with team members to identify missing information",
                "Review similar projects for reference",
                "Use AI services where applicable to generate missing artifacts"
            ],
            "resources": [
                "Team expertise",
                "Project documentation",
                "AI generation services"
            ]
        })