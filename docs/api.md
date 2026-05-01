# AI SDLC Orchestrator - API Documentation

## Overview

AI-powered Software Development Lifecycle platform that assists development teams throughout the entire software development process.

**Base URL:** `http://localhost:8000` (Development)  
**Version:** 1.0.0  
**Auth:** JWT Bearer Token

---

## Authentication

All API endpoints require authentication except:
- POST `/api/v1/auth/login`
- POST `/api/v1/auth/register`
- GET `/health`

### Obtaining Access Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_id": "user_001"
}
```

**Include in headers for authenticated requests:**
```
Authorization: Bearer {access_token}
```

---

## Endpoints Overview

### Requirements Management
- POST `/api/v1/requirements` - Create new requirement
- GET `/api/v1/requirements` - List all requirements
- GET `/api/v1/requirements/{id}` - Get specific requirement
- PUT `/api/v1/requirements/{id}` - Update requirement
- DELETE `/api/v1/requirements/{id}` - Delete requirement

### User Stories
- POST `/api/v1/stories` - Generate user stories from requirements
- GET `/api/v1/stories` - List all stories
- PUT `/api/v1/stories/{id}` - Update story
- DELETE `/api/v1/stories/{id}` - Delete story

### Effort Estimation
- POST `/api/v1/estimates` - Generate estimates for stories/epics
- GET `/api/v1/estimates` - List all estimates
- GET `/api/v1/estimates/{id}` - Get specific estimate

### Test Cases
- POST `/api/v1/test-cases` - Generate test cases
- GET `/api/v1/test-cases` - List all test cases
- PUT `/api/v1/test-cases/{id}` - Update test case
- DELETE `/api/v1/test-cases/{id}` - Delete test case

### Design Suggestions
- POST `/api/v1/design-suggestions` - Generate architecture/design suggestions
- GET `/api/v1/design-suggestions` - List all suggestions

### Resource Gaps
- POST `/api/v1/resource-gaps` - Detect resource gaps for upcoming sprints
- GET `/api/v1/resource-gaps` - List all resource gap reports

### Analytics Dashboard
- GET `/api/v1/analytics/burndown` - Burndown chart data
- GET `/api/v1/analytics/velocity` - Team velocity metrics
- GET `/api/v1/analytics/completion` - Sprint completion tracking

### Real-time Collaboration
- WS `/api/v1/ws/connect` - WebSocket connection for live updates

---

## Request/Response Examples

### Create Requirement

**POST** `/api/v1/requirements`

**Headers:**
```json
{
  "Authorization": "Bearer {token}",
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "title": "User Authentication",
  "description": "Implement secure user authentication system",
  "priority": "high",
  "status": "draft",
  "category": "security",
  "estimated_points": null,
  "created_by": "user_001"
}
```

**Response (201 Created):**
```json
{
  "id": "req_001",
  "title": "User Authentication",
  "description": "Implement secure user authentication system",
  "priority": "high",
  "status": "draft",
  "category": "security",
  "ai_enhanced_summary": "This requirement focuses on implementing a comprehensive authentication system that includes...",
  "created_at": "2026-05-01T18:30:00Z",
  "updated_at": "2026-05-01T18:30:00Z"
}
```

### Generate User Stories from Requirement

**POST** `/api/v1/stories`

**Request Body:**
```json
{
  "requirement_id": "req_001",
  "title": "User Authentication",
  "features": ["login", "registration", "password_reset"],
  "target_audience": "all_users"
}
```

**Response (200 OK):**
```json
[
  {
    "id": "story_001",
    "title": "User Registration",
    "user_story": "As a new user, I want to register with email and password so that I can access the platform",
    "acceptance_criteria": [
      "Given I am not logged in, When I click register, Then I should see registration form",
      "Given I enter valid credentials, When I submit form, Then I should be redirected to dashboard"
    ],
    "priority": "must_have",
    "story_points": 5,
    "epic_id": "auth_epic_001"
  },
  {
    "id": "story_002",
    "title": "User Login",
    "user_story": "As an existing user, I want to log in with email and password so that I can access my account",
    "acceptance_criteria": [
      "Given I have a valid account, When I enter correct credentials, Then I should be authenticated"
    ],
    "priority": "must_have",
    "story_points": 3,
    "epic_id": "auth_epic_001"
  }
]
```

### Generate Test Cases for Functionality

**POST** `/api/v1/test-cases`

**Request Body:**
```json
{
  "function_name": "user_login",
  "description": "Test user login functionality",
  "input_schema": {
    "type": "object",
    "properties": {
      "email": {"type": "string"},
      "password": {"type": "string"}
    },
    "required": ["email", "password"]
  }
}
```

**Response (200 OK):**
```json
[
  {
    "id": "tc_001",
    "test_name": "Valid Login Credentials",
    "description": "User can login with correct email and password",
    "type": "positive",
    "steps": [
      "Navigate to login page",
      "Enter valid email address",
      "Enter valid password",
      "Click 'Login' button"
    ],
    "expected_result": "User is redirected to dashboard",
    "pre_conditions": ["User account exists and is active"],
    "test_id": "TC-001",
    "status": "not_run"
  },
  {
    "id": "tc_002",
    "test_name": "Invalid Login Credentials",
    "description": "User cannot login with incorrect password",
    "type": "negative",
    "steps": [
      "Navigate to login page",
      "Enter valid email address",
      "Enter incorrect password",
      "Click 'Login' button"
    ],
    "expected_result": "Error message displayed: 'Invalid credentials'",
    "pre_conditions": ["User account exists"],
    "test_id": "TC-002",
    "status": "not_run"
  }
]
```

### Get Analytics Dashboard Data

**GET** `/api/v1/analytics/burndown`

**Headers:** `Authorization: Bearer {token}`

**Response (200 OK):**
```json
{
  "sprint": 3,
  "start_date": "2026-04-15",
  "end_date": "2026-05-08",
  "total_story_points_planned": 42,
  "total_story_points_completed": 28,
  "remaining_points": 14,
  "burn_rate": 0.93,
  "trend": "on_track",
  "data_points": [
    {"day": 0, "points_remaining": 42},
    {"day": 1, "points_remaining": 41},
    {"day": 2, "points_remaining": 40},
    ...
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data",
  "type": "value_error"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions for this action"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error. Please try again later."
}
```

---

## Rate Limiting

- **Limit:** 100 requests per minute per IP
- **Header:** `X-Rate-Limit: 100`
- **Header:** `X-Rate-Limit-Remaining: 95`

### Handling Rate Limits (429)

```json
{
  "detail": "Rate limit exceeded",
  "type": "rate_limit_exceeded",
  "headers": {
    "Retry-After": "60"
  }
}
```

---

## WebSocket Real-time Updates

Connect to the WebSocket endpoint for real-time collaboration features:

**Endpoint:** `ws://localhost:8000/api/v1/ws/connect`

**Authentication:** Include JWT token in handshake (implementation-specific)

### Events

- `requirement.created` - New requirement added
- `requirement.updated` - Requirement modified
- `story.completed` - Story marked as done
- `estimate.generated` - New estimate generated
- `design.published` - Design suggestion released
- `alert.resource_gap` - Resource gap detected

### Example Subscription

```json
{
  "type": "subscribe",
  "topics": ["requirement.created", "story.completed"]
}
```

**Response:**
```json
{
  "type": "subscribed",
  "topics": ["requirement.created", "story.completed"],
  "client_id": "client_123"
}
```

---

## Environment Variables Configuration

### Required for Production

```bash
DATABASE_URL=postgresql://user:password@localhost/ai_sdlc
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
LLM_PROVIDER=openai  # or 'mock', 'huggingface'
OPENAI_API_KEY=sk-xxx
```

### Development (Mock LLM)

Set `LLM_PROVIDER=mock` to use simulated AI responses without API calls.

---

## Next Steps

1. **Configure LLM Provider:** Edit `.env` file and set desired provider
2. **Run Migrations:** Initialize database schema
3. **Start Services:** `docker-compose up -d`
4. **Access Dashboard:** Open browser and navigate to frontend (port 3000)
5. **Authentication:** Register/login via `/api/v1/auth/register`

---

*For full interactive API documentation, visit: http://localhost:8000/docs*
