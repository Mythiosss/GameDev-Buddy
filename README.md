# GameDev Buddy

GameDev Buddy is a small AI-powered planning assistant for beginner game developers. It turns a game idea, chosen engine, experience level, and main blocker into a concise MVP development plan.

## What It Does

Provide game idea, engine, experience level, and biggest problem. GameDev Buddy generates goal, core gameplay loop, recommended systems, development order, and next step.

## Why Open-Source AI

GameDev Buddy sends prompts to open-weight Gemma 3 4B through Ollama HTTP API. Inference can run locally and no external AI API key is required. `backend/ollama.py` owns Ollama communication; planning and FastAPI request handling remain separate.

## Tech Stack

- Python
- FastAPI
- Ollama
- Gemma 3 4B
- Vanilla HTML, CSS, and JavaScript

## Architecture

```text
Browser
  |
FastAPI
  |
Ollama
  |
Gemma 3 4B
  |
Structured JSON
  |
Browser
```

## Local Development

Requires Python 3.10+ and Ollama.

```powershell
git clone <repository-url>
cd gamedev-buddy
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama serve
```

In another terminal:

```powershell
ollama pull gemma3:4b
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Base URL for reachable Ollama service |
| `OLLAMA_MODEL` | `gemma3:4b` | Ollama model used for plan generation |
| `PORT` | `8000` | FastAPI HTTP port |

`OLLAMA_HOST` must be an `http` or `https` base URL without a path.

## Docker

The Docker image starts Ollama privately on `127.0.0.1:11434`, pulls `OLLAMA_MODEL` if needed, then starts FastAPI on `0.0.0.0:$PORT`. Port `11434` is not exposed.

Build and run with locally reachable Ollama outside container:

```powershell
docker build -t gamedev-buddy .
docker run --rm -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 -e OLLAMA_MODEL=gemma3:4b gamedev-buddy
```

## Render Demo Deployment

Use a Render **Web Service** with Docker runtime and `Dockerfile` at repository root. Do not set a custom Docker command; image entrypoint starts both services.

Set:

```text
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=gemma3:4b
```

Do not set `PORT`; Render injects it. Set health-check path to `/health`. Ollama remains private inside container; only FastAPI listens on Render public port.

Model is pulled at container startup, not Docker build. This keeps image smaller and lets `OLLAMA_MODEL` stay runtime-configurable. First boot downloads model; without persistent disk, restarts download it again. Attach Render persistent disk mounted at `/root/.ollama` to retain model data between restarts.

This project does not claim public deployment is live. Render must provide enough RAM, disk, and CPU for Gemma 3 4B before service creation.

## API

### `GET /health`

```json
{
  "status": "ok"
}
```

### `POST /api/generate-plan`

Request:

```json
{
  "game_idea": "A small game about dodging falling rocks.",
  "engine": "Godot",
  "experience_level": "Beginner",
  "biggest_problem": "I do not know what to build first."
}
```

Response:

```json
{
  "goal": "Make a playable rock-dodging game.",
  "core_loop": "Move, avoid rocks, and survive.",
  "recommended_systems": ["Player movement", "Rock spawner", "Collision detection"],
  "development_order": ["Create player movement", "Add falling rocks", "Detect collisions"],
  "next_step": "Create a player scene that moves left and right."
}
```

All request fields are required non-empty strings. Limits: game idea 2,000 characters, engine and experience level 100 each, biggest problem 1,000. Invalid requests return HTTP `422`; Ollama failures return `503`; invalid model output returns `502`.

## Testing

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s backend -p "test_*.py" -v
node --check frontend\app.js
```

## Project Structure

```text
frontend/
  index.html
  styles.css
  app.js
backend/
  main.py
  ollama.py
  plans.py
  test_plans.py
  test_ollama.py
Dockerfile
start.sh
requirements.txt
README.md
```

## Limitations

- Output quality depends on configured model.
- Scope reduction is not always aggressive enough.
- This is an MVP, not a full game project management system.
- A self-hosted Gemma 3 4B demo needs substantial model storage and runtime memory.

## Hacktoberfest 2026

Built for Hacktoberfest 2026 weekend challenge, “Build for a Friend.”
