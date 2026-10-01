import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

print("KEY FOUND:", bool(api_key))
print("KEY LENGTH:", len(api_key) if api_key else 0)
print("KEY PREFIX OK:", api_key.startswith("sk-or-v1-") if api_key else False)

if not api_key:
    raise SystemExit("OPENROUTER_API_KEY was not loaded.")

api_key = api_key.strip()

headers = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json",
}

print("AUTHORIZATION HEADER CREATED:", "Authorization" in headers)

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json={
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": "Say hello in one short sentence."
            }
        ],
        "max_tokens": 50
    },
    timeout=30
)

print("STATUS CODE:", response.status_code)
print("RESPONSE:")
print(response.text)