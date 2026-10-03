from unittest.mock import MagicMock, patch

from backend.ollama import generate


with patch("backend.ollama.urlopen") as mock_urlopen:
    mock_response = MagicMock()
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    with patch("backend.ollama.json.load", return_value={"response": "Plan"}):
        assert generate("Test prompt") == "Plan"
