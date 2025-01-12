import asyncio
import uvicorn
import threading
from server import server
from client import Client
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_server():
    uvicorn.run(server, host="127.0.0.1", port=8000, log_level="critical")

async def integration_test():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    await asyncio.sleep(1) 

    try:
        client = Client("http://localhost:8000")

        # Run and monitor 5 10s jobs
        for i in range(5):        
            response = client.create_job().json()
            print(response['result'])
            
            response = client.start_job().json()
            print(response['result'])
            
            start_time = time.time()
            client.monitor_job()
            delay = time.time() - start_time - 10
            print("Delay: " + str(delay))
            print("-----------------")

        # Run and monitor 5 20s jobs
        for i in range(5):        
            response = client.create_job(20).json()
            print(response['result'])
            
            response = client.start_job().json()
            print(response['result'])
            
            start_time = time.time()
            client.monitor_job()
            delay = time.time() - start_time - 20
            print("Delay: " + str(delay))
            print("-----------------")
        
        # Run and monitor 5 30s jobs
        for i in range(5):        
            response = client.create_job(30).json()
            print(response['result'])
            
            response = client.start_job().json()
            print(response['result'])
            
            start_time = time.time()
            client.monitor_job()
            delay = time.time() - start_time - 30
            print("Delay: " + str(delay))
            print("-----------------")
        

    except Exception as e:
        logger.error(f"Error during test: {e}")

if __name__ == "__main__":
    asyncio.run(integration_test())