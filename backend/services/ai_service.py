import asyncio
import os
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

# Explicitly load .env from the backend directory (parent of services)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)


async def get_ai_response(user_prompt: str, system_message: str = "You are NOTESHIP, a helpful study assistant."):
    """
    Base function to call Bytez API (Async).
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
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(bytez_endpoint, headers=headers, json=payload) as response:
                
                if not response.ok:
                    text = await response.text()
                    return f"Model API error {response.status}: {text}"

                data = await response.json()

                if "output" in data and data["output"] and "content" in data["output"]:
                    return data["output"]["content"]

                if "error" in data and data["error"]:
                    return f"Bytez Error: {data['error']}"

                return "No output returned by Bytez"

    except asyncio.TimeoutError:
        return "Request timed out (5s limit)"
    except Exception as e:
        return f"Request Failed: {str(e)}"
