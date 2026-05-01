"""
Requirement processing service using LLM
"""
import logging
from app.services.llm_provider import get_llm_provider

logger = logging.getLogger(__name__)

class RequirementService:
    def __init__(self):
        self.llm_provider = get_llm_provider()
        if not self.llm_provider.is_available():
            logger.warning("LLM provider is not available. Using mock responses.")

    def refine_requirement(self, raw_text: str) -> dict:
        """
        Refine a raw requirement using LLM.
        Returns refined text and clarification questions.
        """
        prompt = f"""
You are an expert business analyst. Refine the following raw requirement to make it clear, concise, and actionable.
Identify any ambiguities or missing information and generate clarification questions.

Raw Requirement:
{raw_text}

Please provide:
1. Refined requirement (clear, concise, actionable)
2. List of clarification questions (if any ambiguities or missing information)

Format your response as:
Refined Requirement:
[Your refined requirement here]

Clarification Questions:
[Each question on a new line, or "None" if no questions]
"""
        try:
            response = self.llm_provider.generate(prompt, max_tokens=800, temperature=0.3)
            
            # Parse the response
            refined_text = ""
            clarification_questions = ""
            
            if "Refined Requirement:" in response and "Clarification Questions:" in response:
                parts = response.split("Clarification Questions:")
                refined_part = parts[0].replace("Refined Requirement:", "").strip()
                clarification_part = parts[1].strip() if len(parts) > 1 else ""
                
                refined_text = refined_part
                clarification_questions = clarification_part if clarification_part.strip().lower() != "none" else ""
            else:
                # Fallback if format is not followed exactly
                refined_text = response.strip()
                clarification_questions = ""
                
            return {
                "refined_text": refined_text,
                "clarification_questions": clarification_questions
            }
        except Exception as e:
            logger.error(f"Error refining requirement: {e}")
            # Return mock response on error
            return {
                "refined_text": f"Refined requirement based on: {raw_text[:100]}...",
                "clarification_questions": "What is the target audience for this feature? What are the key success metrics?"
            }

    def generate_clarification_questions(self, raw_text: str) -> list:
        """
        Generate clarification questions for a raw requirement.
        """
        result = self.refine_requirement(raw_text)
        questions_text = result.get("clarification_questions", "")
        
        # Split into individual questions
        questions = [q.strip() for q in questions_text.split('\n') if q.strip() and not q.strip().startswith('#')]
        return questions