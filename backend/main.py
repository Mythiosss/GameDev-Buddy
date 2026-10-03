import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.ollama import OllamaUnavailableError, generate
from backend.plans import SYSTEM_PROMPT, DevelopmentPlan, PlanRequest, build_prompt, parse_plan

app = FastAPI(title="GameDev Buddy")
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"


class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/test-ollama")
def test_ollama(request: PromptRequest) -> dict[str, str]:
    try:
        return {"response": generate(request.prompt)}
    except OllamaUnavailableError as error:
        raise HTTPException(status_code=503, detail="Ollama is unavailable") from error


@app.post("/api/generate-plan", response_model=DevelopmentPlan)
def generate_plan(request: PlanRequest) -> DevelopmentPlan:
    try:
        response = generate(
            build_prompt(request), system=SYSTEM_PROMPT, response_format="json"
        )
    except OllamaUnavailableError as error:
        raise HTTPException(status_code=503, detail="Ollama is unavailable") from error

    try:
        return parse_plan(response)
    except ValueError as error:
        raise HTTPException(status_code=502, detail="Ollama returned an invalid plan") from error


app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
