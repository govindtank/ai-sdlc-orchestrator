"""
LLM Provider Abstraction Layer
Supports multiple backends: OpenAI, HuggingFace TGI/vLLM, and mock for development.
"""
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured."""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                logger.warning("OpenAI package not installed. Install with: pip install openai")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Check API key.")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 500),
                temperature=kwargs.get("temperature", 0.7),
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def is_available(self) -> bool:
        return self.client is not None

class HuggingFaceProvider(LLMProvider):
    """HuggingFace TGI or vLLM provider."""

    def __init__(self, endpoint_url: Optional[str] = None, api_key: Optional[str] = None):
        self.endpoint_url = endpoint_url or os.getenv("HF_ENDPOINT_URL")
        self.api_key = api_key or os.getenv("HF_API_KEY")
        self.headers = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.endpoint_url:
            raise RuntimeError("HuggingFace endpoint URL not configured.")
        try:
            import requests
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": kwargs.get("max_tokens", 500),
                    "temperature": kwargs.get("temperature", 0.7),
                    "return_full_text": False,
                },
            }
            response = requests.post(
                self.endpoint_url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            elif isinstance(result, dict):
                return result.get("generated_text", "")
            else:
                return str(result)
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            raise

    def is_available(self) -> bool:
        return bool(self.endpoint_url)

class MockProvider(LLMProvider):
    """Mock provider for development and testing."""

    def generate(self, prompt: str, **kwargs) -> str:
        # Simple mock responses based on prompt content
        if "refine" in prompt.lower() or "requirement" in prompt.lower():
            return """Refined Requirement:
The user needs a system that allows them to track their daily water intake and receive reminders to drink water throughout the day. The system should provide a simple interface to log water consumption and visualize progress toward daily goals.

Clarification Questions:
1. What is the target daily water intake goal (in ounces or liters)?
2. Should the reminders be customizable in frequency and timing?
3. Is integration with wearable devices (like Fitbit or Apple Watch) desired?"""
        elif "user story" in prompt.lower():
            return """User Story:
As a health-conscious individual, I want to easily log my water intake so that I can track my hydration levels throughout the day.

Acceptance Criteria:
- User can add a water intake entry with a single tap
- User can view daily, weekly, and monthly hydration trends
- User receives reminders at configurable intervals
- Data is stored locally and can be exported"""
        elif "test" in prompt.lower():
            return """Test Cases:
1. Functional Test: Verify that tapping the 'Add Water' button increases the daily total by the selected amount.
2. Edge Case Test: Verify that the system handles extremely large input values (e.g., 1000 liters) gracefully.
3. UI Test: Verify that the hydration progress bar updates correctly after each entry.
4. Performance Test: Verify that logging 100 entries in succession does not cause UI lag."""
        elif "code review" in prompt.lower():
            return """Code Review Suggestions:
1. Consider adding input validation for water intake amounts to prevent negative values.
2. The reminder system could benefit from using a background service instead of timers.
3. Add unit tests for the water intake calculation logic.
4. Consider using a state management library for better scalability."""
        else:
            return f"Mock AI response for: {prompt[:100]}..."

    def is_available(self) -> bool:
        return True

def get_llm_provider() -> LLMProvider:
    """Factory function to get the configured LLM provider."""
    provider_type = os.getenv("LLM_PROVIDER", "mock").lower()
    
    if provider_type == "openai":
        return OpenAIProvider()
    elif provider_type == "huggingface":
        return HuggingFaceProvider()
    else:
        # Default to mock for development
        return MockProvider()