import os

import requests
from dotenv import load_dotenv

load_dotenv()




def get_ai_response(user_prompt: str, system_message: str = "You are NOTESHIP, a helpful study assistant."):
    """
    Base function to call Bytez API.
    """
    bytez_key = os.getenv("BYTEZ_API_KEY")
    if not bytez_key:
        return "API key not configured"

    model_id = os.getenv("MODEL_ID", "google/gemini-2.5-pro")
    bytez_endpoint = f"https://api.bytez.com/models/v2/{model_id}"

    headers = {
        "Authorization": bytez_key,
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "params": {
            "temperature": 0.7,
            "max_length": 1000
        }
    }

    try:
        response = requests.post(
            bytez_endpoint,
            headers=headers,
            json=payload,
            timeout=60
        )

        if not response.ok:
            return f"Model API error {response.status_code}: {response.text}"

        data = response.json()

        if "output" in data and data["output"] and "content" in data["output"]:
            return data["output"]["content"]

        if "error" in data and data["error"]:
            return f"Bytez Error: {data['error']}"

        return "No output returned by Bytez"

    except Exception as e:
        return f"Request Failed: {str(e)}"
