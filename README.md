# AI SDLC Orchestrator

An AI-powered Software Development Lifecycle platform that assists development teams throughout the entire software development process.

## ✨ Features

### Core SDLC Features
- **Requirements Management**: AI-powered requirement refinement and clarification with gap detection
- **User Stories**: Automatic generation from requirements with acceptance criteria
- **Estimation**: Effort estimation (rule-based + ML) with story points and confidence levels
- **Design Suggestion**: Wireframe descriptions and UI component recommendations
- **Resource Gap Analysis**: Detect missing components across all layers of the stack
- **Test Case Generation**: Automated test case creation with functional, edge, performance, and security coverage
- **Code Review Assistance**: AI-powered review suggestions and improvement notes
- **Real-time Collaboration**: WebSocket-based team updates and notifications

### Advanced Features
- Analytics dashboard with burndown charts and velocity tracking
- Role-based access control and audit logging
- LLM-agnostic design (pluggable providers: mock, OpenAI, HuggingFace)
- Complete API documentation
- Docker Compose for quick deployment
- RESTful API with JWT authentication

## 🛠️ Tech Stack

- **Backend**: Python/FastAPI
- **Frontend**: React/TypeScript + Material-UI (MUI)
- **Database**: PostgreSQL  
- **Cache**: Redis
- **Containerization**: Docker/Kubernetes
- **AI Integration**: LLM abstraction layer with mock support

## 📦 Development Phases Completed

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | MVP Backend API structure, models, services | ✅ Complete |
| Phase 2 | Design and QA integration services | ✅ Complete |
| Phase 3 | Authentication and security (JWT, RBAC) | ✅ Complete |
| Phase 4 | Real-time collaboration via WebSockets | ✅ Complete |
| Phase 5 | Analytics and reporting with Recharts | ✅ Complete |
| Phase 6.2 | LLM provider & documentation setup | ✅ Complete |
| Phase 6.5 | Test suite & API service layer | ✅ Complete |
| **Phase 7** | **Complete working React frontend** | ✅ **COMPLETED** |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local backend dev)
- Node.js 18+ (for local frontend dev)

### Using Docker (Recommended)

```bash
# Build and run all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

### Local Development

#### Backend

```bash
cd backend
pip install -r requirements.txt

# Create .env file with database and AI provider settings
# See .env.example for template

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install

# Start development server
npm run dev

# Visit http://localhost:3000
```

## 📊 API Endpoints

The backend exposes a complete REST API at `/api/v1`:

- **Authentication**: `/auth/register`, `/auth/login`, `/auth/logout`
- **Requirements**: CRUD operations with AI refinement
- **User Stories**: Generate from requirements, estimate effort
- **Test Cases**: Generate test suites automatically
- **Design Suggestions**: Wireframe and UI recommendations
- **Resource Gaps**: Gap detection across all project layers
- **Analytics**: Burndown charts, velocity metrics

See `backend/app/api/v1/endpoints/` for API routes.

## 🤖 AI Integration

The platform uses an LLM abstraction layer that supports:

- **Mock Mode**: No AI required (use for development)
- **OpenAI**: For production with OpenAI models
- **HuggingFace**: For open-source model integration
- **Custom Providers**: Easy plugin architecture

Configure via `backend/app/core/llm_provider.py`

## 📁 Project Structure

```
ai-sdlc-orchestrator/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/endpoints/  # API routes
│   │   ├── services/          # Business logic & AI integration
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── core/              # Config, security, LLM provider
│   │   └── db/                # Database session & base class
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # React frontend
│   ├── src/
│   │   ├── pages/               # All SDLC module pages
│   │   ├── components/          # Reusable UI components (optional)
│   │   ├── services/            # API client & auth
│   │   └── App.jsx              # Main application shell
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # All-in-one deployment
├── README.md
└── .hermes/                # Hermes project metadata (optional)
```

## 🔐 Security Features

- JWT-based authentication with secure token handling
- Password hashing using bcrypt
- CORS configuration for API access control
- Role-based access control (admin/user roles)
- Secure headers and HTTPS ready

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest tests/

# Run frontend tests (when added)
npm test
```

## 📈 Analytics Dashboard

The platform includes real-time analytics:

- **Burndown Charts**: Track sprint progress vs estimates
- **Velocity Tracking**: Measure team performance over time
- **Completion Metrics**: Real-time project health indicators
- **Resource Utilization**: AI-powered gap detection suggestions

Visualized with Recharts for responsive, beautiful charts.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - See LICENSE file for details

## 🔗 GitHub Repository

🌐 [govindtank/ai-sdlc-orchestrator](https://github.com/govindtank/ai-sdlc-orchestrator)

---

**Status: Phase 7 Complete - Full-stack AI SDLC Orchestrator ready for deployment!** 🎉
