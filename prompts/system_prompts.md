# System Prompts Library for AI SDLC Orchestrator

## Overview
This directory contains AI prompts used throughout the application for generating requirements, user stories, design suggestions, test cases, and estimates. Each prompt is designed to work with LLM models like GPT-3.5, GPT-4, Claude, or open-source alternatives.

---

## 1. Requirement Refinement Prompts

### 1.1 Initial Clarification
```
You are an expert requirements engineer. Analyze the following rough requirement and help clarify it:

**User Input:** {requirement_text}

Please ask targeted questions to understand:
1. The primary goal/objective
2. Key stakeholders/users affected
3. Functional vs non-functional requirements
4. Constraints (budget, timeline, technical)
5. Success metrics/KPIs

Wait for user responses before providing refined requirement.

If information seems sufficient, provide a summary of questions answered and any assumptions made.
```

### 1.2 Requirement Specification Generation
```
Based on the following clarified requirements:

**Context:** {context}
**Goals:** {goals}
**Stakeholders:** {stakeholders}

Generate a comprehensive technical requirement specification including:
- Functional Requirements (FR-001, FR-002, etc.)
- Non-Functional Requirements (NFR-001, NFR-002, etc.)
- Use Case Descriptions
- Acceptance Criteria
- Assumptions and Constraints

Format as a structured document with clear sections.
```

---

## 2. User Story Generation Prompts

### 2.1 Story Creation
```
Convert the following technical requirement into user stories:

**Requirement:** {requirement}
**Features identified:** {features}

For each feature, create:
- User Story: "As a [user role], I want to [action] so that [benefit]"
- Acceptance Criteria (Given-When-Then format)
- Priority (Must Have / Should Have / Nice to Have)
- Effort Estimate (Story points: 1, 2, 3, 5, 8, 13)

Output format: JSON array of story objects with fields: id, title, user_story, acceptance_criteria, priority, story_points
```

### 2.2 Epics and Milestones
```
Group related user stories into epics based on common themes and dependencies:

**Stories:** {stories_list}

Create epics with:
- Epic Name
- Description
- Estimated Stories count
- Suggested order for implementation
- Dependencies (if any)
```

---

## 3. Design Suggestion Prompts

### 3.1 Architecture Pattern Recommendation
```
Analyze this application requirement and recommend the appropriate architecture pattern:

**Application Type:** {app_type}
**Scale Requirements:** {scale_info}
**Performance Needs:** {performance_requirements}

Recommend one of:
- MVC (Model-View-Controller)
- MVP (Model-View-Presenter)
- MVVM (Model-View-ViewModel)
- CQRS (Command Query Responsibility Segregation)
- Event-Driven Architecture

Provide:
1. Recommended pattern with justification
2. Key components and their responsibilities
3. Data flow diagram description
4. Technology recommendations for implementation
5. Pros and cons of the recommendation
```

### 3.2 Database Schema Design
```
Design a relational database schema for this application feature:

**Feature Description:** {feature}
**Key Entities:** {entities}
**Relationships:** {relationships}

Generate ERD-style description including:
1. Tables with columns, data types, constraints
2. Primary and Foreign keys
3. Index recommendations
4. Relationship types (one-to-one, one-to-many, many-to-many)
5. Normalization considerations
```

---

## 4. Test Case Generation Prompts

### 4.1 Unit Test Cases
```
Generate unit test cases for the following functionality:

**Function to Test:** {function_description}
**Input Parameters:** {inputs}
**Expected Behavior:** {expected_behavior}
**Edge Cases:** {edge_cases}

For each test case, provide:
- Test ID
- Test Name/Description
- Input Data (JSON format)
- Expected Output
- Test Steps
- Pre-conditions
- Post-conditions

Also include negative test cases for error handling.
```

### 4.2 Integration Test Scenarios
```
Create integration test scenarios for the following API endpoint:

**Endpoint:** {endpoint}
**Method:** {method} (GET/POST/PUT/DELETE)
**Business Logic:** {business_logic}

For each scenario, provide:
- Scenario Name
- Request payload (if applicable)
- Expected response structure
- Status codes to handle
- Error conditions to test
- Data cleanup steps
```

---

## 5. Effort Estimation Prompts

### 5.1 Story Point Estimation
```
Estimate effort for these user stories using Fibonacci sequence (1, 2, 3, 5, 8, 13, 21):

**Stories:** {stories_with_complexity}
**Team Composition:** {team_info}

For each story, provide:
- Complexity factors (technical difficulty, uncertainty, dependencies)
- Risk level (low/medium/high)
- Initial estimate
- Recommended estimate after considering risks

Justify estimates with specific reasoning.
```

### 5.2 Sprint Planning Estimation
```
Group stories into sprints based on capacity and dependencies:

**Stories:** {stories_list}
**Sprint Capacity:** {capacity_hours}
**Team Velocity (previous sprints):** {velocity_history}

Recommend:
1. Number of sprints required
2. Stories per sprint
3. Critical path for implementation order
4. Potential risks to timeline
```

---

## 6. Code Review Suggestion Prompts

### 6.1 Security Audit
```
Review this code snippet for security vulnerabilities:

**Code:** {code_snippet}
**Context:** {code_context}

Check for:
- SQL injection vulnerabilities
- XSS risks
- Authentication/authorization issues
- Input validation gaps
- Data exposure (sensitive info)
- Dependency vulnerabilities

Flag each issue with severity (Critical, High, Medium, Low) and remediation steps.
```

### 6.2 Code Quality Review
```
Review this code for quality improvements:

**Code:** {code_snippet}
**Standards:** {coding_standards}

Evaluate:
- Readability
- Maintainability
- Performance optimization opportunities
- Best practices adherence
- Documentation completeness
- Error handling adequacy

Provide specific refactoring suggestions with before/after examples.
```

---

## 7. Documentation Generation Prompts

### 7.1 API Documentation
```
Generate API documentation for this endpoint:

**Endpoint:** {endpoint}
**Request Schema:** {request_schema}
**Response Schema:** {response_schema}

Create:
- Endpoint summary
- HTTP method and path
- Request parameters (path, query, body) with descriptions
- Response structure with examples
- Error codes and messages
- Authentication requirements
- Rate limits if applicable

Format suitable for Swagger/OpenAPI spec.
```

### 7.2 README/Getting Started Guide
```
Create a getting started guide for this application:

**Application:** {app_name}
**Purpose:** {purpose}
**Key Features:** {features}
**Tech Stack:** {technology_stack}
**Setup Requirements:** {setup_info}

Generate:
1. Project overview and value proposition
2. Prerequisites and installation steps
3. Configuration guide (environment variables)
4. Basic usage examples
5. Common commands (start, stop, rebuild)
6. Troubleshooting tips
7. Next steps for production deployment

Format as comprehensive README.md content.
```

---

## Usage Notes

1. **Prompt Selection:** Use appropriate prompts based on the AI service being called:
   - `app/services/llm_router.py` routes to correct provider
   - Prompts are stored here for reference and debugging

2. **Temperature Settings:** 
   - Creative tasks (design, documentation): 0.7-1.0
   - Technical tasks (code review, requirements): 0.3-0.5
   - Estimation: 0.1-0.3 (more deterministic)

3. **Context Window Management:** Keep prompts concise and include only relevant context in {placeholders}

4. **Prompt Chaining:** Complex tasks may require multiple prompt calls in sequence

5. **Version Control:** Update prompts as models evolve - version each major change
