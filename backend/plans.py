import json

from pydantic import BaseModel, ConfigDict, Field, ValidationError

SYSTEM_PROMPT = """You are GameDev Buddy, a practical planning assistant for beginner game developers.
Create a small playable MVP plan from user details. Favor implementation over brainstorming. Avoid unnecessary features and complex architecture. Respect engine and experience level. Address biggest problem directly. Put systems in dependency order. Give one immediate concrete next action.
Return only valid JSON with exactly this structure:
{
  "goal": "string",
  "core_loop": "string",
  "recommended_systems": ["string"],
  "development_order": ["string"],
  "next_step": "string"
}
Keep every value concise. Do not use markdown or add any other keys."""


class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    game_idea: str = Field(min_length=1, max_length=2000)
    engine: str = Field(min_length=1, max_length=100)
    experience_level: str = Field(min_length=1, max_length=100)
    biggest_problem: str = Field(min_length=1, max_length=1000)


class DevelopmentPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    goal: str = Field(min_length=1)
    core_loop: str = Field(min_length=1)
    recommended_systems: list[str] = Field(min_length=1)
    development_order: list[str] = Field(min_length=1)
    next_step: str = Field(min_length=1)


def build_prompt(request: PlanRequest) -> str:
    return (
        f"Game idea: {request.game_idea}\n"
        f"Engine: {request.engine}\n"
        f"Experience level: {request.experience_level}\n"
        f"Biggest problem: {request.biggest_problem}"
    )


def parse_plan(response: str) -> DevelopmentPlan:
    try:
        return DevelopmentPlan.model_validate(json.loads(response))
    except (json.JSONDecodeError, ValidationError) as error:
        raise ValueError("Ollama returned an invalid plan") from error
