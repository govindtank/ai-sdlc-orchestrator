"""
LLM Service - Factory and Router for Multiple LLM Providers
Provides a unified interface for switching between mock, OpenAI, and HuggingFace providers
"""
import logging
from typing import Optional, Dict, Any, Literal
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseLLMService:
    """Base class for LLM services that wraps provider logic."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
    
    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text completion from a prompt."""
        pass
    
    @abstractmethod
    def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Chat completion with conversation history."""
        pass


class MockLLMService(BaseLLMService):
    """Mock LLM service for development/testing without API calls."""
    
    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        logger.debug(f"[MOCK] Generating response for: {prompt[:50]}...")
        
        # Simulate AI response based on context
        responses = {
            "requirement refinement": f"Refined requirement: {prompt}\n\nThe requirement has been clarified to include:\n- Clear acceptance criteria\n- Measurable success metrics\n- Dependencies and constraints",
            "user story": f"User Story from:\n\nAs a {self._extract_user_type(prompt)}, I want to {self._extract_action(prompt)} so that {self._extract_value(prompt)}.",
            "design suggestion": f"Design Suggestion for:\n\n**Architecture Pattern:** MVC\n**Data Flow:** Request → Controller → Service → Repository → Response\n**Technology Stack:** Python/FastAPI + React/TypeScript",
            "test case": f"Test Case Generated for:\n\n**Test ID:** TC-{hash(prompt) % 10000}\n**Scenario:** {prompt}\n**Expected Output:** Successful completion with proper validation\n**Edge Cases:** Input validation, null handling, error recovery",
        }
        
        # Default generic response
        default_response = f"""{prompt}

**AI Response:**
Based on the analysis, here's a comprehensive response:

1. **Key Considerations:**
   - Ensure proper input validation
   - Handle edge cases gracefully
   - Maintain backward compatibility

2. **Implementation Notes:**
   - Use type hints for clarity
   - Add docstrings to functions
   - Include error handling

3. **Testing Strategy:**
   - Write unit tests for each component
   - Add integration tests for API endpoints
   - Include end-to-end scenarios"""
        
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": responses.get("default generic response", default_response) if "." in responses else default_response
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 50, "total_tokens": 60},
            "model": self.model_name
        }
    
    def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Handle multi-turn conversations."""
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant", 
                        "content": self._summarize_conversation(messages)
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {"prompt_tokens": 50, "completion_tokens": 100, "total_tokens": 150}
        }
    
    def _extract_user_type(self, prompt: str) -> str:
        """Extract user type from requirement text."""
        types = ["administrator", "manager", "user", "admin"]
        return types[hash(prompt) % len(types)]
    
    def _extract_action(self, prompt: str) -> str:
        """Extract action from requirement text."""
        actions = ["view reports", "generate analytics", "manage users"]
        return actions[hash(prompt) % len(actions)]
    
    def _extract_value(self, prompt: str) -> str:
        """Extract value proposition from requirement text."""
        values = ["better insights", "efficient workflow", "improved security"]
        return values[hash(prompt) % len(values)]
    
    def _summarize_conversation(self, messages: list) -> str:
        """Summarize conversation history."""
        return "Based on our discussion, I can help you with further analysis and implementation details. Please let me know what aspect you'd like to focus on."


class OpenAIService(BaseLLMService):
    """OpenAI API LLM service."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        super().__init__(model_name)
        self.api_key = api_key or ""
        self.client = None
        
        if api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=api_key)
            except ImportError:
                logger.warning("OpenAI package not installed. Install with: pip install openai")
    
    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Set OPENAI_API_KEY in environment.")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 500),
                temperature=kwargs.get("temperature", 0.7)
            )
            
            logger.debug(f"[OPENAI] Response received: {len(response.choices[0].message.content)} tokens")
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": response.choices[0].message.content
                        },
                        "finish_reason": response.choices[0].finish_reason
                    }
                ],
                "usage": response.usage.dict() if response.usage else {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"[OPENAI] API Error: {e}")
            raise
    
    def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        if not self.client:
            raise RuntimeError("OpenAI client not initialized.")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", 500),
                temperature=kwargs.get("temperature", 0.7)
            )
            
            return {
                "choices": [
                    {
                        "message": {
                            "role": response.choices[0].message.role,
                            "content": response.choices[0].message.content
                        },
                        "finish_reason": response.choices[0].finish_reason
                    }
                ],
                "usage": response.usage.dict() if response.usage else {}
            }
        except Exception as e:
            logger.error(f"[OPENAI] API Error: {e}")
            raise


class HuggingFaceService(BaseLLMService):
    """HuggingFace TGI/vLLM LLM service."""
    
    def __init__(self, endpoint_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__()
        self.endpoint_url = endpoint_url or ""
        self.api_key = api_key or ""
        
        if self.api_key:
            self.headers = {"Authorization": f"Bearer {self.api_key}"}
        else:
            self.headers = {}
    
    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        if not self.endpoint_url:
            raise RuntimeError("HuggingFace endpoint URL not configured. Set HF_ENDPOINT_URL in environment.")
        
        try:
            import requests
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": kwargs.get("max_tokens", 500),
                    "temperature": kwargs.get("temperature", 0.7)
                }
            }
            
            response = requests.post(
                self.endpoint_url,
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("generated_text", "")
                
                return {
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": generated_text
                            },
                            "finish_reason": "stop"
                        }
                    ],
                    "usage": {"prompt_tokens": 0, "completion_tokens": len(generated_text), "total_tokens": len(generated_text)},
                    "model": self.endpoint_url.split("/")[-1]
                }
            else:
                logger.error(f"[HUGGINGFACE] API Error {response.status_code}: {response.text}")
                raise Exception(f"API Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"[HUGGINGFACE] Request Error: {e}")
            raise
    
    def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Chat with HuggingFace model (single-turn only for most TGI models)."""
        # Convert messages to prompt format
        system_msg = ""
        for msg in messages:
            if msg["role"] == "system":
                system_msg += f"System: {msg['content']}\n\n"
            elif msg["role"] == "user":
                system_msg += f"User: {msg['content']}"
            elif msg["role"] == "assistant":
                system_msg += f"\nAssistant: {msg['content']}"
        
        if system_msg and "User" in messages[-1]["role"]:
            system_msg += "\n\nAssistant:"
        
        return self.complete(system_msg, **kwargs)


class LLMRouter:
    """
    Router that selects the appropriate LLM service based on configuration.
    Supports fallback to mock if other providers fail or aren't configured.
    """
    
    def __init__(self, 
                 provider: Literal["mock", "openai", "huggingface"] = "mock",
                 model_name: str = "gpt-3.5-turbo"):
        
        self.provider = provider
        self.model_name = model_name
        
        # Initialize appropriate service
        if provider == "openai":
            import os
            api_key = os.getenv("OPENAI_API_KEY") or ""
            self.service = OpenAIService(model_name=model_name, api_key=api_key if api_key else None)
            logger.info(f"Initialized OpenAI LLM service with model: {model_name}")
        elif provider == "huggingface":
            import os
            endpoint = os.getenv("HF_ENDPOINT_URL", "")
            api_key = os.getenv("HF_API_KEY", "")
            self.service = HuggingFaceService(endpoint_url=endpoint, api_key=api_key if api_key else None)
            logger.info(f"Initialized HuggingFace LLM service with endpoint: {endpoint}")
        else:  # mock or default
            self.service = MockLLMService(model_name=model_name)
            logger.info(f"Using Mock LLM service (development mode)")
        
        self._initialized = True
    
    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate completion using current provider."""
        return self.service.complete(prompt, **kwargs)
    
    def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        """Handle chat conversation using current provider."""
        return self.service.chat(messages, **kwargs)
    
    @property
    def is_available(self) -> bool:
        """Check if the current service is available."""
        if isinstance(self.service, MockLLMService):
            return True
        elif isinstance(self.service, OpenAIService):
            return self.service.client is not None
        elif isinstance(self.service, HuggingFaceService):
            return bool(self.service.endpoint_url)
        return False
    
    def get_model_name(self) -> str:
        """Get the current model name."""
        if isinstance(self.service, MockLLMService):
            return self.model_name
        return "configured_model"


# Factory function for creating LLM router
def create_llm_router(provider: Literal["mock", "openai", "huggingface"] = "mock", 
                      model_name: str = "gpt-3.5-turbo") -> LLMRouter:
    """Factory function to create and return an LLMRouter instance."""
    return LLMRouter(provider=provider, model_name=model_name)
