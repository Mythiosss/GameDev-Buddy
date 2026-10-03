import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

DEFAULT_OLLAMA_HOST = "http://127.0.0.1:11434"
DEFAULT_MODEL = "gemma3:4b"


class OllamaUnavailableError(RuntimeError):
    pass


def get_ollama_api_url() -> str:
    host = os.getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST).strip().rstrip("/")
    parsed_host = urlsplit(host)
    if (
        parsed_host.scheme not in {"http", "https"}
        or not parsed_host.netloc
        or parsed_host.path not in {"", "/"}
        or parsed_host.query
        or parsed_host.fragment
    ):
        raise OllamaUnavailableError("OLLAMA_HOST must be an HTTP URL without a path")
    return f"{host}/api/generate"


def generate(
    prompt: str,
    system: str | None = None,
    response_format: str | dict[str, object] | None = None,
) -> str:
    request_body = {
        "model": os.getenv("OLLAMA_MODEL", DEFAULT_MODEL),
        "prompt": prompt,
        "stream": False,
    }
    if system is not None:
        request_body["system"] = system
    if response_format is not None:
        request_body["format"] = response_format

    payload = json.dumps(request_body).encode("utf-8")
    request = Request(
        get_ollama_api_url(),
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise OllamaUnavailableError("Ollama request failed") from error

    generated_text = result.get("response")
    if not isinstance(generated_text, str):
        raise OllamaUnavailableError("Ollama returned an invalid response")

    return generated_text
