# Groq Code Diagnostic Engine

A high-performance FastAPI application that diagnoses code using Groq's Llama 3.1 models.

## Features

- **FastAPI**: Modern, fast web framework
- **Groq Integration**: Powered by Llama 3.1 models for rapid code analysis
- **Docker Ready**: Containerized for easy deployment
- **CI/CD**: Automated testing and deployment pipeline
- **Production Ready**: Resource limits, health checks, logging

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Groq API Key ([Get one here](https://console.groq.com))

## Local Development

### Using Docker Compose (Recommended)

1. Clone the repository
2. Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```
3. Start the application:
   ```bash
   docker compose up --build
   ```
4. Access the API at `http://localhost:8000`
5. Interactive API docs at `http://localhost:8000/docs`

### Using Make Commands

```bash
make up          # Start services
make down        # Stop services
make logs        # View logs
make test        # Run tests
make clean       # Clean up containers and volumes
```

## API

### Health Check

`GET /health`

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Diagnose Code

`POST /diagnose`

Analyzes code for potential issues.

Request body:

```json
{
  "language": "python",
  "code": "print('hello')",
  "context": "Optional context about the code"
}
```

Supported languages: `python`, `javascript`, `typescript`, `java`, `c++`, `go`, `rust`, `ruby`, `php`, `swift`.

Response:

```json
{
  "result": "[CLEAN]",
  "model_used": "llama-3.1-8b-instant"
}
```

## Testing

Run tests with:

```bash
pytest
```

With coverage:

```bash
pytest --cov=. --cov-report=html
```

## Production Deployment

The application is configured for production with:

- Resource limits (CPU and memory)
- Health checks
- Structured logging
- Graceful shutdown support

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Your Groq API key |
| `APP_ENV` | No | Application environment (default: development) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

## Project Structure

```text
groq-diagnostic-engine/
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── test_main.py
├── .github/workflows/ci.yml
├── .env.example
├── .gitignore
├── Makefile
├── README.md
└── LICENSE
```

## License

MIT
