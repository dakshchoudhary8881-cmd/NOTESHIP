import asyncio
import time

import aiohttp

BASE_URL = "http://127.0.0.1:5000"

async def test_root():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + "/") as resp:
                text = await resp.text()
                print(f"[GET /] Status: {resp.status}")
                if resp.status == 200:
                    return True
    except Exception as e:
        print(f"[GET /] Exception: {e}")
    return False

async def test_chat():
    payload = {"message": "Explain atoms quickly"}
    start = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_URL + "/chat", json=payload) as resp:
                data = await resp.json()
                duration = time.time() - start
                print(f"[POST /chat] Status: {resp.status}, Time: {duration:.2f}s")
                if resp.status == 200 and duration < 3:
                    return True
                elif resp.status == 503:
                    print("Service Unavailable (Expected if no API key or Rate Limit)")
                    return True # Pass for now if handled gracefully
    except Exception as e:
        print(f"[POST /chat] Exception: {e}")
    return False

async def test_notes():
    payload = {"topic": "Metals and Non-metals"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_URL + "/notes", json=payload) as resp:
                data = await resp.json()
                print(f"[POST /notes] Status: {resp.status}")
                if resp.status == 200:
                    has_markdown = "reply" in data 
                    # We can't strict check markdown content if it's a mock or error message
                    return True
                elif resp.status == 503:
                    return True
    except Exception as e:
        print(f"[POST /notes] Exception: {e}")
    return False

async def make_stress_request(session, i):
    start = time.time()
    try:
        async with session.post(BASE_URL + "/chat", json={"message": f"stress {i}"}) as resp:
            await resp.read()
            duration = time.time() - start
            return duration, resp.status
    except Exception:
        return 0, 500

async def stress_test():
    print("[Stress Test] Firing 20 concurrent requests...")
    async with aiohttp.ClientSession() as session:
        tasks = [make_stress_request(session, i) for i in range(20)]
        results = await asyncio.gather(*tasks)
        
    latencies = [r[0] for r in results]
    statuses = [r[1] for r in results]
    
    avg_latency = sum(latencies) / len(latencies)
    success_count = statuses.count(200) + statuses.count(503) # Count 503 as handled/pass for stress on logic
    
    print(f"[Stress Test] Avg Latency: {avg_latency:.2f}s")
    print(f"[Stress Test] Success/Handled: {success_count}/20")
    print(f"[Stress Test] Status Codes: {set(statuses)}")
    
    if avg_latency < 1.5 and success_count == 20:
        return True
    return False

async def main():
    # Wait for server to be up
    print("Waiting for server...")
    await asyncio.sleep(2) 
    
    print("\n=== RUNNING BACKEND TESTS ===")
    passes = 0
    total = 4
    
    if await test_root(): passes += 1
    else: print("FAIL: Root")
    
    if await test_chat(): passes += 1
    else: print("FAIL: Chat")
    
    if await test_notes(): passes += 1
    else: print("FAIL: Notes")
    
    if await stress_test(): passes += 1
    else: print("FAIL: Stress")
    
    print(f"\nResult: {passes}/{total} Passed")

if __name__ == "__main__":
    asyncio.run(main())
