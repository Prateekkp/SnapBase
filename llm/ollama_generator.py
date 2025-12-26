import requests
from typing import Optional


OLLAMA_URL = "http://localhost:11434/api/generate"

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        # Try to get a simple response from Ollama
        payload = {
            "model": "llama2",  # Default model for testing
            "prompt": "Say OK",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 10
            }
        }
        r = requests.post(OLLAMA_URL, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
        return False


def generate_sql_with_ollama(prompt: str, model: str = "llama2") -> Optional[str]:
    """Generate SQL using Ollama"""
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 512
            }
        }

        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()

        response_data = r.json()
        content = response_data.get("response", "").strip()
        return content if content else None

    except requests.exceptions.Timeout:
        print("❌ Ollama error: Request timeout (Ollama is taking too long)")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Ollama error: Connection failed (check if Ollama is running on localhost:11434)")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ Ollama error: HTTP {e.response.status_code}")
        return None
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return None