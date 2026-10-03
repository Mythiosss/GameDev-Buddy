# GameDev Buddy

GameDev Buddy is a small AI-powered planning assistant for beginner game developers. Describe a game idea, current skill level, and main blocker; it turns that brief into a concise, practical MVP development plan using local Ollama inference.

## What It Does

Provide:

- Game idea
- Engine
- Experience level
- Biggest problem

GameDev Buddy generates:

- Goal
- Core gameplay loop
- Recommended systems
- Development order
- Next step

Plans prioritize small playable MVPs, practical implementation, and dependency-aware build order.

## Why Open-Source AI

GameDev Buddy sends prompts to open-weight Gemma 3 4B through local Ollama HTTP API. Inference can run locally and no external AI API key is required. Set `OLLAMA_MODEL` to choose installed model.

`backend/ollama.py` owns Ollama communication; planning and FastAPI request handling remain separate. Open models make local experimentation and modification more accessible.

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

## Running Locally

Requires Python 3.10+ and Ollama.

1. Clone repository:

   ```powershell
   git clone <repository-url>
   cd gamedev-buddy
   ```

2. Create virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install Python requirements:

   ```powershell
   pip install -r requirements.txt
   ```

5. Make sure Ollama is installed and running. Start it if needed:

   ```powershell
   ollama serve
   ```

6. Pull default configured model:

   ```powershell
   ollama pull gemma3:4b
   ```

7. Start FastAPI:

   ```powershell
   uvicorn backend.main:app --reload
   ```

8. Open `http://127.0.0.1:8000`.

No frontend build step is required.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_MODEL` | `gemma3:4b` | Ollama model used for generation |

Set another installed model for current PowerShell session:

```powershell
$env:OLLAMA_MODEL = "gemma3:4b"
uvicorn backend.main:app --reload
```

Ollama API address is fixed in application code at `http://127.0.0.1:11434/api/generate`.

## API

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
  "recommended_systems": [
    "Player movement",
    "Rock spawner",
    "Collision detection"
  ],
  "development_order": [
    "Create player movement",
    "Add falling rocks",
    "Detect collisions"
  ],
  "next_step": "Create a player scene that moves left and right."
}
```

All request fields are required non-empty strings; extra fields return HTTP `422`. Ollama failures return HTTP `503`. Invalid model output returns HTTP `502`.

## Testing

Run automated backend tests from repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s backend -p "test_*.py" -v
```

Current automated suite has 5 passing tests covering valid input/output, missing input, malformed model output, and Ollama unavailability.

Real-world validation ran five game-development scenarios through local Ollama/Gemma: beginner platformer, arena roguelike, overscoped RPG, combat-improvement problem, and Unreal horror game. All returned valid structured responses. Invalid requests correctly returned HTTP `422`. Live browser flow was verified: frontend → FastAPI → Ollama → Gemma → UI.

Scope reduction was only partially successful in overscoped RPG scenario; model still retained some extra systems.

## Project Structure

```text
frontend/
  index.html       Single-page interface
  styles.css       Responsive UI styles
  app.js           Form submission and plan rendering
backend/
  main.py          FastAPI app and API routes
  ollama.py        Local Ollama HTTP service
  plans.py         Plan models, prompt, and response parsing
  test_plans.py    Plan tests
  test_ollama.py   Ollama service check
requirements.txt   Python dependencies
README.md          Project documentation
```

## Limitations

- Output quality depends on local model.
- Scope reduction is not always aggressive enough.
- This is an MVP, not a full game project management system.

## Hacktoberfest 2026

Built for Hacktoberfest 2026 weekend challenge, “Build for a Friend.”
