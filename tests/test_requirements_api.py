"""
Tests for Requirements API Endpoint
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestRequirementsEndpoint:
    """Test Requirements CRUD operations."""
    
    def test_create_requirement(self, client):
        """Should create new requirement successfully."""
        response = client.post(
            "/api/v1/requirements",
            json={
                "title": "Test Requirement",
                "description": "A sample requirement for testing",
                "priority": "high",
                "status": "draft"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Requirement"
    
    def test_get_all_requirements(self, client):
        """Should list all requirements."""
        # Create a requirement first
        client.post(
            "/api/v1/requirements",
            json={
                "title": "First Requirement",
                "description": "Description 1",
                "priority": "medium"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        response = client.get(
            "/api/v1/requirements",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_get_requirement_by_id(self, client):
        """Should get specific requirement by ID."""
        # Create first
        create_response = client.post(
            "/api/v1/requirements",
            json={
                "title": "Specific Requirement",
                "description": "Test description"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        req_id = create_response.json()["id"]
        
        response = client.get(
            f"/api/v1/requirements/{req_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Specific Requirement"
    
    def test_update_requirement(self, client):
        """Should update existing requirement."""
        # Create first
        create_response = client.post(
            "/api/v1/requirements",
            json={
                "title": "To Update",
                "description": "Original description"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        req_id = create_response.json()["id"]
        
        # Update
        update_response = client.put(
            f"/api/v1/requirements/{req_id}",
            json={
                "title": "Updated Title",
                "description": "Updated description"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["title"] == "Updated Title"
    
    def test_delete_requirement(self, client):
        """Should delete requirement."""
        # Create first
        create_response = client.post(
            "/api/v1/requirements",
            json={
                "title": "To Delete",
                "description": "Will be deleted"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        req_id = create_response.json()["id"]
        
        delete_response = client.delete(
            f"/api/v1/requirements/{req_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert delete_response.status_code == 204
        
        # Verify deleted
        get_response = client.get(
            f"/api/v1/requirements/{req_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert get_response.status_code == 404
    
    def test_create_missing_fields(self, client):
        """Should reject requirement missing required fields."""
        response = client.post(
            "/api/v1/requirements",
            json={
                "title": ""  # Empty title
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main(["-v", "-s"])
