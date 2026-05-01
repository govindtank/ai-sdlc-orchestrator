"""
Effort estimation service using LLM and heuristics
"""
import logging
from app.services.llm_provider import get_llm_provider

logger = logging.getLogger(__name__)

class EstimateService:
    def __init__(self):
        self.llm_provider = get_llm_provider()
        if not self.llm_provider.is_available():
            logger.warning("LLM provider is not available. Using mock responses.")

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

    def generate_test_cases(self, user_story: dict) -> list:
        """
        Generate test cases from a user story using LLM.
        """
        prompt = f"""
You are an expert QA engineer. Generate test cases for the following user story.
Include functional tests, edge cases, and negative tests where applicable.

User Story:
Title: {user_story.get('title', '')}
Description: {user_story.get('description', '')}
Acceptance Criteria: {chr(10).join(['- ' + ac for ac in user_story.get('acceptance_criteria', [])])}

Please provide test cases in the following format:
Test Case 1:
Title: [Test case title]
Description: [What this test verifies]
Type: [functional, edge_case, performance, security, ui]
Steps:
1. [Step 1]
2. [Step 2]
Expected Result: [Expected outcome]

Test Case 2:
[Same format as above]
"""
        try:
            response = self.llm_provider.generate(prompt, max_tokens=1000, temperature=0.3)
            
            # Parse test cases from response
            test_cases = []
            current_tc = {}
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith("Test Case") and ":" in line:
                    # Save previous test case if exists
                    if current_tc and "title" in current_tc:
                        test_cases.append(current_tc)
                    current_tc = {}
                elif line.startswith("Title:") and current_tc:
                    current_tc["title"] = line.replace("Title:", "").strip()
                elif line.startswith("Description:") and current_tc:
                    current_tc["description"] = line.replace("Description:", "").strip()
                elif line.startswith("Type:") and current_tc:
                    current_tc["test_type"] = line.replace("Type:", "").strip().lower()
                elif line.startswith("Steps:") and current_tc:
                    current_tc["steps_raw"] = []
                elif line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")) and current_tc and "steps_raw" in current_tc:
                    current_tc["steps_raw"].append(line)
                elif line.startswith("Expected Result:") and current_tc:
                    current_tc["expected_result"] = line.replace("Expected Result:", "").strip()
                    
            # Process steps_raw into steps string
            for tc in test_cases:
                if "steps_raw" in tc:
                    tc["steps"] = "\n".join(tc["steps_raw"])
                    del tc["steps_raw"]
                # Ensure required fields exist
                tc.setdefault("title", "Generated Test Case")
                tc.setdefault("description", "Test case generated from user story")
                tc.setdefault("test_type", "functional")
                tc.setdefault("steps", "1. Execute test\n2. Verify results")
                tc.setdefault("expected_result", "Test passes successfully")
                
            # Save last test case
            if current_tc and "title" in current_tc:
                if "steps_raw" in current_tc:
                    current_tc["steps"] = "\n".join(current_tc["steps_raw"])
                    del current_tc["steps_raw"]
                current_tc.setdefault("title", "Generated Test Case")
                current_tc.setdefault("description", "Test case generated from user story")
                current_tc.setdefault("test_type", "functional")
                current_tc.setdefault("steps", "1. Execute test\n2. Verify results")
                current_tc.setdefault("expected_result", "Test passes successfully")
                test_cases.append(current_tc)
                
            return test_cases if test_cases else self._get_mock_test_cases(user_story)
        except Exception as e:
            logger.error(f"Error generating test cases: {e}")
            return self._get_mock_test_cases(user_story)

    def _get_mock_test_cases(self, user_story: dict) -> list:
        """Generate mock test cases when LLM is not available."""
        return [
            {
                "title": f"Verify {user_story.get('title', 'feature')} works as expected",
                "description": "Test that the core functionality works correctly",
                "test_type": "functional",
                "steps": "1. Navigate to the feature\n2. Perform the main action\n3. Verify the outcome",
                "expected_result": "The feature works as described in the user story"
            },
            {
                "title": f"Test edge cases for {user_story.get('title', 'feature')}",
                "description": "Test boundary conditions and unusual inputs",
                "test_type": "edge_case",
                "steps": "1. Test with minimum values\n2. Test with maximum values\n3. Test with invalid inputs",
                "expected_result": "The system handles edge cases gracefully"
            }
        ]