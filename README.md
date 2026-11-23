# Docker + LangGraph: one-agent university helpdesk

A beginner-class project with **one LangGraph agent**, two tools, FastAPI, Groq GPT-OSS 120B, and SQLite. **The PDF companion teaches Docker, images, containers, ports, volumes, Compose, and every file.**

## Quick start

1. Install and launch Docker Desktop (or Docker Engine with Compose).
2. Copy `.env.example` to `.env`.
3. Put your real Groq API key into `.env`.
4. From this folder, run `docker compose up --build`.
5. Open http://127.0.0.1:8000 and ask a question.

## Three routes to test

- `GET http://127.0.0.1:8000/health` - health check
- `POST http://127.0.0.1:8000/chat` - AI messages
- `GET http://127.0.0.1:8000/tickets` - SQLite tickets
- `GET /` is a small browser UI; `GET /docs` is FastAPI's automatic API explorer.

Example chat JSON:

```json
{"session_id":"student-1", "message":"What is the attendance policy?"}
```

Next ask: `Create a complaint: the Wi-Fi is broken in Lab 4.`

## Docker commands

```bash
docker compose up --build
docker compose ps
docker compose logs -f
docker compose down
```

The Docker named volume keeps SQLite tickets even after `docker compose down`; `docker compose down -v` removes the named volume and data. **LangGraph uses `InMemorySaver` for chat context, so conversation memory is lost when the application restarts.** Reuse the same `session_id` while running to test memory.

## Important

- Groq runs remotely via its API: Docker packages **your Python application**, not the 120B model.
- This is a **local classroom demo**, not production software. No login or user authorization is implemented.
- `.env` is excluded from Git and Docker build context; never upload keys to GitHub.
- Image build and Python syntax can be checked without Groq; actual AI calls need a valid key and network access.
