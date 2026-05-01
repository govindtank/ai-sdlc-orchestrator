"""
User story generation service using LLM
"""
import logging
from app.services.llm_provider import get_llm_provider

logger = logging.getLogger(__name__)

class StoryService:
    def __init__(self):
        self.llm_provider = get_llm_provider()
        if not self.llm_provider.is_available():
            logger.warning("LLM provider is not available. Using mock responses.")

    def generate_user_story(self, refined_requirement: str) -> dict:
        """
        Generate a user story from a refined requirement using LLM.
        Returns title, description, and acceptance criteria.
        """
        prompt = f"""
You are an expert product manager. Convert the following refined requirement into a well-formed user story with acceptance criteria.
Follow the format: "As a [type of user], I want [some goal] so that [some reason]."

Refined Requirement:
{refined_requirement}

Please provide:
1. User story title (concise)
2. User story description (in the standard format)
3. Acceptance criteria (as a list of testable conditions)

Format your response as:
Title:
[Your user story title here]

Description:
[Your user story description here]

Acceptance Criteria:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]
"""
        try:
            response = self.llm_provider.generate(prompt, max_tokens=800, temperature=0.3)
            
            # Parse the response
            title = ""
            description = ""
            acceptance_criteria = []
            
            lines = response.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith("Title:"):
                    current_section = "title"
                    title = line.replace("Title:", "").strip()
                elif line.startswith("Description:"):
                    current_section = "description"
                    description = line.replace("Description:", "").strip()
                elif line.startswith("Acceptance Criteria:"):
                    current_section = "acceptance"
                elif line.startswith("- ") and current_section == "acceptance":
                    acceptance_criteria.append(line[2:].strip())
                elif current_section == "title" and line and not line.startswith(("Description:", "Acceptance Criteria:")):
                    title += " " + line
                elif current_section == "description" and line and not line.startswith(("Title:", "Acceptance Criteria:")):
                    if description:
                        description += " " + line
                    else:
                        description = line
                        
            # Clean up
            title = title.strip()
            description = description.strip()
            
            return {
                "title": title,
                "description": description,
                "acceptance_criteria": acceptance_criteria
            }
        except Exception as e:
            logger.error(f"Error generating user story: {e}")
            # Return mock response on error
            return {
                "title": "User Story from Requirement",
                "description": "As a user, I want to achieve the goal described in the requirement so that I can benefit from the solution.",
                "acceptance_criteria": [
                    "The system should fulfill the core requirement",
                    "The system should be usable by the target audience",
                    "The system should meet performance expectations"
                ]
            }

    def estimate_effort(self, user_story: dict) -> dict:
        """
        Estimate effort for a user story using heuristics and LLM if available.
        Returns story points and confidence level.
        """
        # Simple heuristic based on description length and acceptance criteria count
        desc_len = len(user_story.get("description", ""))
        ac_count = len(user_story.get("acceptance_criteria", []))
        
        # Base points calculation
        base_points = 3  # Start with medium complexity
        
        # Adjust based on description length
        if desc_len > 200:
            base_points += 2
        elif desc_len > 100:
            base_points += 1
            
        # Adjust based on acceptance criteria
        if ac_count > 5:
            base_points += 2
        elif ac_count > 2:
            base_points += 1
            
        # Cap at 13 (Fibonacci-like scale)
        story_points = min(max(base_points, 1), 13)
        
        # Try to get LLM-based estimate if available
        llm_estimate = None
        try:
            if self.llm_provider.is_available():
                prompt = f"""
Estimate the effort in story points for implementing the following user story.
Use the Fibonacci scale (1, 2, 3, 5, 8, 13) where 1 is trivial and 13 is very complex.
Consider the scope, technical complexity, and uncertainty.

User Story:
Title: {user_story.get('title', '')}
Description: {user_story.get('description', '')}
Acceptance Criteria: {chr(10).join(['- ' + ac for ac in user_story.get('acceptance_criteria', [])])}

Provide only the number representing the story points.
"""
                response = self.llm_provider.generate(prompt, max_tokens=50, temperature=0.1)
                # Extract number from response
                import re
                numbers = re.findall(r'\b\d+\b', response)
                if numbers:
                    llm_estimate = int(numbers[0])
                    # Validate it's in our range
                    if 1 <= llm_estimate <= 13:
                        story_points = llm_estimate
        except Exception as e:
            logger.debug(f"LLM estimation failed, using heuristic: {e}")
            
        # Calculate confidence based on whether we used LLM
        confidence = "high" if llm_estimate is not None else "medium"
        
        return {
            "story_points": story_points,
            "confidence": confidence,
            "method": "llm" if llm_estimate is not None else "heuristic"
        }