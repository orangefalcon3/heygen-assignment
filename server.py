import time
from fastapi import FastAPI
from pydantic import BaseModel

# Model for post request
class Base(BaseModel):
    length: int

# Class to represent job handler
class JobHandler:

    # Initialize job handler
    def __init__(self):
        self.jobs = []
        self.current_job = None
    
    # Create a new job
    def create_job(self, length=10):
        
        # Create job
        newJob = Job(length)

        # Add job to queue
        self.jobs.append(newJob)

        # Return update message
        return "New " + str(length) + "s Job has been created"
    
    # Start a new job
    def start_job(self):

        # Check if current job is running 
        if (not self.current_job or self.current_job.status() == "completed"):

            # Check if there is a job in the queue
            if (len(self.jobs) > 0):
               
               # Get the next job in the queue
               self.current_job = self.jobs.pop(0)

               # Start the job
               self.current_job.start_job()

               # Return update message
               return "New Job has started"
            
            # Handle error of no jobs in queue
            else:
                return "Error: no jobs in queue"
        
        # Handle error of job currently running
        else:
            return "Error: another job is currently running"
    
    # Get status of current job
    def get_current_status(self):
        try:

            # Get status from job
            return self.current_job.status()
        
        # Handle error
        except: 
            return "error"

# Class to represent a job        
class Job:

    # Initialize the job
    def __init__(self, length=25):
        self.start = 0
        self.job_length = length 
    
    # Start the job
    def start_job(self):
        self.start = time.time()

    # Get the status
    def status(self):
        try:

            # Check if job has been started
            if self.start == 0:
                return "pending"
            
            # Find how long job has been running
            elapsed_time = time.time() - self.start
            
            # Check if job is completed
            if elapsed_time >= self.job_length:
                return "completed"
            return "pending"
        
        # Handle errors
        except:
            return "error"

# Initialize server and job handler
server = FastAPI()
handler = JobHandler()

# Endpoint to get status
@server.get("/status")
async def get_current_status():
    return {"result": handler.get_current_status()}

# Endpoint for job starting
@server.get("/start")
async def start_job():
    return {"result": handler.start_job()}

# Endpoint for job creation
@server.post("/create")
async def create_job(length: Base):
    return {"result": handler.create_job(length.length)}

