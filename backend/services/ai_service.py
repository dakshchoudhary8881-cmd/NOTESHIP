import os
import requests
from dotenv import load_dotenv

load_dotenv()

BYTEZ_KEY = os.getenv("BYTEZ_API_KEY")
MODEL_ID = os.getenv("MODEL_ID", "google/gemini-2.5-pro")

BYTEZ_ENDPOINT = f"https://api.bytez.com/models/v2/{MODEL_ID}"


def get_ai_response(prompt: str):
    if not BYTEZ_KEY:
        return "Bytez API key missing. Add it in .env"

    headers = {
        "Authorization": BYTEZ_KEY,  # Bytez uses raw key, not Bearer
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are NOTESHIP, a helpful study assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "params": {
            "temperature": 0.7,
            "max_length": 200
        }
    }

    try:
        response = requests.post(
            BYTEZ_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=60
        )

        try:
            data = response.json()
        except:
            return f"Bytez returned invalid JSON: {response.text}"

        # Correct Bytez chat response structure
        if "output" in data and data["output"] and "content" in data["output"]:
            return data["output"]["content"]

        if "error" in data and data["error"]:
            return f"Bytez Error: {data['error']}"

        return "No output returned by Bytez"

    except Exception as e:
        return f"Request Failed: {str(e)}"
