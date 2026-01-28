import concurrent.futures
import time

import requests

BASE_URL = "http://127.0.0.1:5000"
NUM_REQUESTS = 10
MAX_TIME = 3  # seconds (aggressive for 10 requests but let's try)

def send_chat_request(i):
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/chat", json={"message": f"Stress test message {i}"}, timeout=5)
        elapsed = time.time() - start
        return {
            "id": i,
            "status": response.status_code,
            "time": elapsed,
            "success": response.status_code == 200
        }
    except Exception as e:
        return {
            "id": i,
            "status": "ERROR",
            "time": time.time() - start,
            "success": False,
            "error": str(e)
        }

def run_stress_test():
    print(f"Starting Stress Test: {NUM_REQUESTS} requests...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(send_chat_request, range(NUM_REQUESTS)))
    
    total_time = time.time() - start_time
    success_count = sum(1 for r in results if r["success"])
    
    print("\n=== Stress Test Results ===")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Success Rate: {success_count}/{NUM_REQUESTS}")
    
    for r in results:
        status = r["status"]
        if r["status"] == 200:
            print(f"Req {r['id']}: {status} ({r['time']:.2f}s)")
        else:
            print(f"Req {r['id']}: {status} ({r['time']:.2f}s) - {r.get('error', '')}")

if __name__ == "__main__":
    run_stress_test()
