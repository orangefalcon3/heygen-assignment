import time
from fastapi import FastAPI

class JobHandler:
    def __init__(self):
        self.jobs = []
        self.current_job = Job(10)
        self.current_job.start_job()
    
    def create_job(self, length=10):
        newJob = Job(length)
        self.jobs.append(newJob)
        return "New Job has been created"
    
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
        if (not self.current_job):
            return "error"
        return self.current_job.status()
        
class Job:
    def __init__(self, length=10):
        self.start = 0
        self.job_length = length 
    
    def start_job(self):
        self.start = time.time()

    def status(self):
        if self.start == 0:
            return "pending"
        elapsed_time = time.time() - self.start
        if elapsed_time >= self.job_length:
            return "completed"
        return "pending"

server = FastAPI()
handler = JobHandler()


@server.get("/status")
async def get_current_status():
    return {"result": handler.get_current_status()}

@server.get("/start")
async def start_job():
    return {"result": handler.start_job()}

@server.get("/create")
async def create_job():
    return {"result": handler.create_job()}

