import time

import requests

BASE_URL = "http://127.0.0.1:5000"

def test_root():
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"GET /: {resp.status_code}")
        print(resp.json())
    except Exception as e:
        print(f"GET / failed: {e}")

def test_chat():
    try:
        start = time.time()
        payload = {"message": "Explain photosynthesis in 3 lines"}
        resp = requests.post(f"{BASE_URL}/chat", json=payload)
        duration = time.time() - start
        print(f"POST /chat: {resp.status_code} ({duration:.2f}s)")
        print(resp.json())
    except Exception as e:
        print(f"POST /chat failed: {e}")

def test_notes():
    try:
        payload = {"topic": "Chemical Reactions and Equations"}
        resp = requests.post(f"{BASE_URL}/notes", json=payload)
        print(f"POST /notes: {resp.status_code}")
        # Print first 100 chars
        print(resp.text[:100])
    except Exception as e:
        print(f"POST /notes failed: {e}")
        
def stability_test():
    print("Running Stability Test (10 messages)...")
    success = 0
    for i in range(10):
        try:
            resp = requests.post(f"{BASE_URL}/chat", json={"message": f"ping {i}"})
            if resp.status_code == 200:
                success += 1
        except Exception:  # noqa: E722
            pass
    print(f"Stability: {success}/10 passed")

if __name__ == "__main__":
    test_root()
    test_chat()
    test_notes()
    stability_test()
