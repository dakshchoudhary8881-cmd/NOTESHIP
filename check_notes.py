import requests

try:
    response = requests.post("http://127.0.0.1:5000/notes", json={"topic": "Test"}, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(e)
