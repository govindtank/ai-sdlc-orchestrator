# AI SDLC Orchestrator

An AI-powered Software Development Lifecycle platform that assists development teams throughout the entire software development process.

## Features
- AI-powered requirement refinement and clarification
- User story generation from requirements  
- Effort estimation (rule-based + ML)
- AI-assisted code review suggestions
- Automated test case generation
- Real-time team collaboration via WebSockets
- Analytics dashboard with burndown charts
- Role-based access control and audit logging
- Plugin architecture for Jira/GitHub/Slack integration
- AI-powered documentation generator
- LLM-agnostic design (start with open-source, configure any provider)

## Tech Stack
- Backend: Python/FastAPI
- Frontend: React/TypeScript
- Database: PostgreSQL
- Cache: Redis
- Containerization: Docker/Kubernetes
- AI: LLM abstraction layer (open-source first, configurable to any provider)

## Development Phases
See .hermes/plans/ for detailed phase-by-phase implementation plan.

## Setup
1. Clone repository
2. Copy .env.example to .env and configure
3. Run `docker-compose up -d` for development services
4. Install dependencies: `pip install -r backend/requirements.txt` and `npm install` in frontend
5. Start development servers

## License
MIT