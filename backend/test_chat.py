import requests

res = requests.post(
    "http://127.0.0.1:5000/chat",
    json={"message": "Hello from NOTESHIP backend"}
)

print(res.json())
