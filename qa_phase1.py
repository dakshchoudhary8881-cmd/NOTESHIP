import sys
import time

import requests

BASE_URL = "http://127.0.0.1:5000"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def check_root():
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            log("Root endpoint reachable: 200 OK", "PASS")
            return True
        else:
            log(f"Root endpoint failed: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"Root endpoint exception: {e}", "FAIL")
        return False

def check_chat_503():
    try:
        payload = {"message": "hello"}
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
        # We expect 503 because Bytez API is expired.
        # But wait, looking at chat.py again:
        # It calls get_ai_response. If that raises Exception -> 503.
        # If it returns a reply starting with "Request Failed" -> 503.
        # So 503 is the expected correct behavior for "Expired" credits if the code handles it.
        # The prompt says: "Confirm /chat returns expected 503 gracefully"
        
        if response.status_code == 503:
            log("Chat endpoint returned 503 as expected", "PASS")
            try:
                data = response.json()
                if data.get("status") == "error":
                    log("Chat JSON structure correct", "PASS")
                else:
                    log(f"Chat JSON unexpected: {data}", "WARN")
            except:
                log("Chat response not valid JSON", "FAIL")
            return True
        else:
            log(f"Chat endpoint unexpected status: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"Chat endpoint exception: {e}", "FAIL")
        return False

def check_notes_503():
    try:
        payload = {"topic": "Photosynthesis"}
        response = requests.post(f"{BASE_URL}/notes", json=payload, timeout=10)
        
        if response.status_code == 503:
            log("Notes endpoint returned 503 as expected", "PASS")
            return True
        else:
            log(f"Notes endpoint unexpected status: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"Notes endpoint exception: {e}", "FAIL")
        return False

def check_performance():
    log("Running 5 sequential requests to /chat...")
    latencies = []
    for i in range(5):
        start = time.time()
        try:
            requests.post(f"{BASE_URL}/chat", json={"message": f"msg {i}"}, timeout=5)
            latencies.append(time.time() - start)
        except Exception as e:
            log(f"Request {i} failed: {e}", "FAIL")
    
    if latencies:
        avg = sum(latencies) / len(latencies)
        log(f"Average latency: {avg:.4f}s", "INFO")
        if max(latencies) < 5:
            log("No request exceeded 5s", "PASS")
        else:
            log(f"Some requests exceeded 5s: {max(latencies):.4f}s", "FAIL")
    else:
        log("All performance requests failed", "FAIL")

def main():
    log("Starting Phase 1 Server Validation")
    # Wait a moment for server to be fully ready
    time.sleep(2)
    
    if not check_root():
        sys.exit(1)
        
    check_chat_503()
    check_notes_503()
    check_performance()
    
    log("Phase 1 Complete")

if __name__ == "__main__":
    main()
