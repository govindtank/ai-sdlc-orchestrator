"""
Pytest configuration and shared fixtures for AI SDLC Orchestrator tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


# Create test client fixture that can be reused across test files
@pytest.fixture(scope="session")
def test_client():
    """Create a FastAPI test client for the application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def set_test_environment():
    """Set environment variables for testing."""
    import os
    
    # Ensure we're using test database
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("DEBUG", "True")
    os.environ.setdefault("LOG_LEVEL", "DEBUG")


# Shared fixtures can be added here as needed
