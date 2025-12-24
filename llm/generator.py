import requests

NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def test_api_key(api_key):
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "meta/llama-4-maverick-17b-128e-instruct",
            "messages": [{"role": "user", "content": "Say OK"}],
            "max_tokens": 5
        }
        r = requests.post(NVIDIA_URL, headers=headers, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ API key validation error: {e}")
        return False

def generate_sql(prompt, api_key):
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }

        payload = {
            "model": "meta/llama-4-maverick-17b-128e-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.2
        }

        r = requests.post(NVIDIA_URL, headers=headers, json=payload, timeout=60)
        r.raise_for_status()

        content = r.json()["choices"][0]["message"]["content"].strip()
        return content if content else None

    except requests.exceptions.Timeout:
        print("❌ LLM error: Request timeout (API is taking too long)")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ LLM error: Connection failed (check internet connection)")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ LLM error: Invalid API key")
        else:
            print(f"❌ LLM error: HTTP {e.response.status_code}")
        return None
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return None
