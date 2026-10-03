import unittest
from unittest.mock import patch

from fastapi import HTTPException
from pydantic import ValidationError

from backend.main import generate_plan, health
from backend.ollama import OllamaUnavailableError
from backend.plans import PlanRequest, parse_plan

VALID_REQUEST = {
    "game_idea": "A small game about dodging falling rocks.",
    "engine": "Godot",
    "experience_level": "Beginner",
    "biggest_problem": "I do not know what to build first.",
}
VALID_PLAN = {
    "goal": "Make a playable rock-dodging game.",
    "core_loop": "Move, avoid rocks, and survive.",
    "recommended_systems": ["Player movement", "Rock spawner", "Collision detection"],
    "development_order": ["Create player movement", "Add falling rocks", "Detect collisions"],
    "next_step": "Create a player scene that moves left and right.",
}
VALID_RESPONSE = """{
  "goal": "Make a playable rock-dodging game.",
  "core_loop": "Move, avoid rocks, and survive.",
  "recommended_systems": ["Player movement", "Rock spawner", "Collision detection"],
  "development_order": ["Create player movement", "Add falling rocks", "Detect collisions"],
  "next_step": "Create a player scene that moves left and right."
}"""


class GeneratePlanTests(unittest.TestCase):
    def test_health(self):
        self.assertEqual(health(), {"status": "ok"})

    def test_input_too_long(self):
        request = VALID_REQUEST | {"game_idea": "x" * 2001}

        with self.assertRaises(ValidationError):
            PlanRequest.model_validate(request)

    def test_valid_request(self):
        request = PlanRequest.model_validate(VALID_REQUEST)

        with patch("backend.main.generate", return_value=VALID_RESPONSE):
            plan = generate_plan(request)

        self.assertEqual(plan.model_dump(), VALID_PLAN)

    def test_missing_required_input(self):
        request = VALID_REQUEST.copy()
        del request["engine"]

        with self.assertRaises(ValidationError):
            PlanRequest.model_validate(request)

    def test_valid_model_response(self):
        plan = parse_plan(VALID_RESPONSE)

        self.assertEqual(plan.model_dump(), VALID_PLAN)

    def test_malformed_model_response(self):
        request = PlanRequest.model_validate(VALID_REQUEST)

        with patch("backend.main.generate", return_value='{"goal": "Missing fields"}'):
            with self.assertRaises(HTTPException) as error:
                generate_plan(request)

        self.assertEqual(error.exception.status_code, 502)
        self.assertEqual(error.exception.detail, "Ollama returned an invalid plan")

    def test_ollama_unavailable(self):
        request = PlanRequest.model_validate(VALID_REQUEST)

        with patch("backend.main.generate", side_effect=OllamaUnavailableError):
            with self.assertRaises(HTTPException) as error:
                generate_plan(request)

        self.assertEqual(error.exception.status_code, 503)
        self.assertEqual(error.exception.detail, "Ollama is unavailable")


if __name__ == "__main__":
    unittest.main()
