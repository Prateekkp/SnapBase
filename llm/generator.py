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

def generate_sql(prompt, api_key, retry_count=0):
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
        elif e.response.status_code == 403:
            print("❌ LLM error: Access forbidden (403)")
            print("   Possible reasons:")
            print("   • API key doesn't have access to this model")
            print("   • NVIDIA API quota or rate limit exceeded")
            print("   • Request may be too large")
            print("   💡 TIP: Try using direct SQL commands instead")
            print("      Example: SHOW TABLES; or SELECT * FROM table_name;")
        elif e.response.status_code == 429:
            print("❌ LLM error: Rate limit exceeded (429)")
            print("   💡 Please wait a moment and try again")
            print("   💡 Or use direct SQL: SHOW TABLES;")
        else:
            print(f"❌ LLM error: HTTP {e.response.status_code}")
            try:
                error_detail = e.response.json()
                if "detail" in error_detail:
                    print(f"   Detail: {error_detail['detail']}")
                elif "error" in error_detail:
                    print(f"   Error: {error_detail['error']}")
            except:
                pass
        return None
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return None
