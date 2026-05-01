"""
Design suggestion service using LLM
"""
import logging
from app.services.llm_provider import get_llm_provider

logger = logging.getLogger(__name__)

class DesignService:
    def __init__(self):
        self.llm_provider = get_llm_provider()
        if not self.llm_provider.is_available():
            logger.warning("LLM provider is not available. Using mock responses.")

    def generate_design_suggestion(self, user_story: dict) -> dict:
        """
        Generate design suggestions from a user story using LLM.
        Returns wireframe description, UI component suggestions, and design notes.
        """
        prompt = f"""
You are an expert UX/UI designer. Create design suggestions for the following user story.
Provide wireframe descriptions, UI component recommendations, and design notes.

User Story:
Title: {user_story.get('title', '')}
Description: {user_story.get('description', '')}
Acceptance Criteria: {chr(10).join(['- ' + ac for ac in user_story.get('acceptance_criteria', [])])}

Please provide:
1. Wireframe description: A textual description of the suggested layout and flow
2. UI component suggestions: List of recommended UI components (e.g., buttons, forms, charts)
3. Design notes: Additional considerations for accessibility, responsiveness, and user experience

Format your response as:
Wireframe Description:
[Your wireframe description here]

UI Component Suggestions:
- [Component 1]
- [Component 2]
- [Component 3]

Design Notes:
[Your design notes here]
"""
        try:
            response = self.llm_provider.generate(prompt, max_tokens=1000, temperature=0.4)
            
            # Parse the response
            wireframe_description = ""
            ui_component_suggestions = []
            design_notes = ""
            
            lines = response.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith("Wireframe Description:"):
                    current_section = "wireframe"
                    wireframe_description = line.replace("Wireframe Description:", "").strip()
                elif line.startswith("UI Component Suggestions:"):
                    current_section = "components"
                elif line.startswith("Design Notes:"):
                    current_section = "notes"
                elif line.startswith("- ") and current_section == "components":
                    ui_component_suggestions.append(line[2:].strip())
                elif current_section == "wireframe" and line and not line.startswith(("UI Component Suggestions:", "Design Notes:")):
                    if wireframe_description:
                        wireframe_description += " " + line
                    else:
                        wireframe_description = line
                elif current_section == "notes" and line and not line.startswith(("Wireframe Description:", "UI Component Suggestions:")):
                    if design_notes:
                        design_notes += " " + line
                    else:
                        design_notes = line
                        
            # Clean up
            wireframe_description = wireframe_description.strip()
            design_notes = design_notes.strip()
            
            # If we didn't parse correctly, fall back to mock
            if not wireframe_description and not ui_component_suggestions and not design_notes:
                return self._get_mock_design_suggestion(user_story)
                
            return {
                "wireframe_description": wireframe_description,
                "ui_component_suggestions": ui_component_suggestions,
                "design_notes": design_notes
            }
        except Exception as e:
            logger.error(f"Error generating design suggestion: {e}")
            return self._get_mock_design_suggestion(user_story)

    def _get_mock_design_suggestion(self, user_story: dict) -> dict:
        """Generate mock design suggestions when LLM is not available."""
        title = user_story.get('title', 'Feature')
        return {
            "wireframe_description": f"A clean, intuitive interface for {title} featuring a primary action button prominently displayed, with supporting information presented in a logical hierarchy. The design follows mobile-first principles with touch-friendly controls.",
            "ui_component_suggestions": [
                "Primary Button",
                "Form Input Fields",
                "Progress Indicator",
                "Notification Badge",
                "Filter/Sort Controls"
            ],
            "design_notes": f"Ensure adequate touch targets (minimum 48x48dp) for mobile usability. Use sufficient color contrast for accessibility. Consider progressive disclosure for advanced features to avoid overwhelming new users. The design should be responsive and work well on both mobile and desktop screens."
        }