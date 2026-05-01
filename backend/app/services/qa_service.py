"""
QA service for test case generation and other QA activities
"""
import logging
from app.services.llm_provider import get_llm_provider

logger = logging.getLogger(__name__)

class QAService:
    def __init__(self):
        self.llm_provider = get_llm_provider()
        if not self.llm_provider.is_available():
            logger.warning("LLM provider is not available. Using mock responses.")

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

    def suggest_test_data(self, user_story: dict) -> dict:
        """
        Suggest test data for a user story.
        """
        # This is a placeholder for future enhancement
        return {
            "valid_inputs": ["example1", "example2"],
            "invalid_inputs": ["", "invalid", "too_long_string"],
            "boundary_values": [0, 1, 100, 101]  # example for numeric fields
        }