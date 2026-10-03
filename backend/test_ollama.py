import os
import unittest
from unittest.mock import MagicMock, patch

from backend.ollama import DEFAULT_OLLAMA_HOST, generate, get_ollama_api_url


class OllamaTests(unittest.TestCase):
    def test_default_host(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_ollama_api_url(), f"{DEFAULT_OLLAMA_HOST}/api/generate")

    def test_host_trailing_slash(self):
        with patch.dict(os.environ, {"OLLAMA_HOST": "http://ollama:11434/"}):
            self.assertEqual(get_ollama_api_url(), "http://ollama:11434/api/generate")

    def test_generate_uses_configured_host(self):
        with patch.dict(os.environ, {"OLLAMA_HOST": "http://ollama:11434"}):
            with patch("backend.ollama.urlopen") as mock_urlopen:
                mock_response = MagicMock()
                mock_response.__enter__.return_value = mock_response
                mock_urlopen.return_value = mock_response

                with patch("backend.ollama.json.load", return_value={"response": "Plan"}):
                    self.assertEqual(generate("Test prompt"), "Plan")

        self.assertEqual(mock_urlopen.call_args.args[0].full_url, "http://ollama:11434/api/generate")


if __name__ == "__main__":
    unittest.main()
