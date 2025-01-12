import time
from fastapi import FastAPI
from pydantic import BaseModel

class Base(BaseModel):
    length: int

class JobHandler:
    def __init__(self):
        self.jobs = []
        self.current_job = None
    
    def create_job(self, length=10):
        newJob = Job(length)
        self.jobs.append(newJob)
        return "New " + str(length) + "s Job has been created"
    
    def start_job(self):
        if (not self.current_job or self.current_job.status() == "completed"):
            if (len(self.jobs) > 0):
               self.current_job = self.jobs.pop(0)
               self.current_job.start_job()
               return "New Job has started"
            else:
                return "Error: no jobs in queue"
        else:
            return "Error: another job is currently running"
    
    def get_current_status(self):
        try:
            return self.current_job.status()
        except: 
            return "error"
        
class Job:
    def __init__(self, length=25):
        self.start = 0
        self.job_length = length 
    
    def start_job(self):
        self.start = time.time()

    def status(self):
        try:
            if self.start == 0:
                return "pending"
            elapsed_time = time.time() - self.start
            if elapsed_time >= self.job_length:
                return "completed"
            return "pending"
        except:
            return "error"

server = FastAPI()
handler = JobHandler()

@server.get("/status")
async def get_current_status():
    return {"result": handler.get_current_status()}

@server.get("/start")
async def start_job():
    return {"result": handler.start_job()}

@server.post("/create")
async def create_job(length: Base):
    return {"result": handler.create_job(length.length)}

