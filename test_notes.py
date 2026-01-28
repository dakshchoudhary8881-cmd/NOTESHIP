import requests


def test_notes():
    try:
        response = requests.post("http://127.0.0.1:5000/notes", json={"topic": "Carbon and its Compounds"}, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
             print("Response snippet:", response.json().get("reply", "")[:100])
             print("Notes Test: PASS")
        else:
             print("Notes Test: FAIL")
             print(response.text)
    except Exception as e:
        print(f"Notes Test: ERROR - {e}")

if __name__ == "__main__":
    test_notes()
