import time
from fastapi import FastAPI

class Job:
    def __init__(self):
        self.start = time.time()
        self.job_length = 50 #Temporary Placeholder, should be configurable?
    
    def status(self):
        elapsed_time = time.time() - self.start
        if elapsed_time >= self.job_length:
            return "completed"
        return "pending"

server = FastAPI()
job = Job()

@server.get("/status")
async def get_status():
    return {"result": job.status()}