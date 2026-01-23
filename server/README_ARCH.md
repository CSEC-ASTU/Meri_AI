# ASTU Route AI - Backend Server

AI-powered campus navigation and university knowledge system for Adama Science and Technology University (ASTU).

## Architecture

**Clean, decoupled architecture** with clear separation of concerns:

```
main.py (FastAPI app, lifespan, middleware, routes)
    ↓
app/
    ├── core/
    │   ├── container.py         (Dependency Injection)
    │   ├── exceptions.py        (Custom Exceptions)
    │   └── logging_config.py    (Logging Setup)
    ├── services/
    │   ├── interfaces.py        (Abstract Service Contracts)
    │   ├── ai_service.py        (Gemini Integration)
    │   ├── vector_service.py    (Semantic Search)
    │   ├── routing_service.py   (Navigation Logic)
    │   ├── rag_service.py       (Knowledge Q&A)
    │   └── cache_service.py     (Redis/Memory Cache)
    └── routers/
        ├── health.py            (Health checks)
        ├── query.py             (Q&A endpoints)
        ├── route.py             (Route endpoints)
        ├── nearby.py            (Services endpoints)
        └── schemas.py           (Request/Response models)

database.py  (Postgres/Supabase with pgvector)
config.py    (Settings & Environment)
models.py    (Data Models)
```

### Key Design Principles

1. **Dependency Injection** - All services injected via container, no hard coupling
2. **Interface-Based** - Services implement abstract interfaces (IDatabase, IAIService, etc.)
3. **Single Responsibility** - Each service handles one domain (AI, Routing, Caching, etc.)
4. **Error Handling** - Custom exceptions with specific codes for API responses
5. **Logging** - Structured logging per module for debugging

## Setup

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key from Supabase dashboard
- `DATABASE_URL` - Postgres connection string
- `AI_API_KEY` - Google Gemini API key

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python database.py
```

This will:
- Enable pgvector extension
- Create `pois` and `documents` tables
- Set up vector indexes

### 4. Run Server

```bash
python main.py
# or with auto-reload in development
uvicorn main:app --reload --host 0.0.0.0 --port 4000
```

Server runs at: `http://localhost:4000`

## API Endpoints

### Health Checks
```bash
GET  /health/          - Basic status
GET  /health/db        - Database check
GET  /health/ai        - AI service check
GET  /health/cache     - Cache service check
```

### Q&A (Phase 4)
```bash
POST /api/query        - Answer university questions
```

### Navigation (Phase 4)
```bash
GET/POST /api/route/stream    - Find route with streaming reasoning
```

### Nearby Services (Phase 4)
```bash
GET  /api/nearby       - Find nearby services (mosque, pharmacy, etc.)
```

## Development

### Checking Configuration

```bash
python diagnose.py
```

## Service Implementation Details

### AI Service (Gemini)
- Generates text embeddings
- Streams responses token-by-token (SSE ready)
- Handles retries and timeouts

### Vector Service
- Semantic search on documents using pgvector
- POI fuzzy matching for locations

### Routing Service
- Haversine distance calculation
- Walking time estimation
- Support for urgency modes (normal, exam, accessibility)

### RAG Service
- Retrieves relevant documents
- Builds context for Gemini
- Generates knowledge-based answers

### Cache Service
- Redis caching with TTL
- Falls back to in-memory cache if Redis unavailable
- Reduces API calls and response latency

## Troubleshooting

**Database connection fails:**
- Check internet connection
- Verify DATABASE_URL in .env
- Run `python diagnose.py`

**AI service errors:**
- Verify AI_API_KEY is valid
- Check API quota in Google Cloud

## Next Steps

1. **Phase 3**: Integrate OpenStreetMap (OSM) for full routing
2. **Phase 4**: Implement API endpoints with streaming responses
3. **Phase 5**: Add authentication, rate limiting, monitoring

## License

MIT - CSEC Hackathon 2026
