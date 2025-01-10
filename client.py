import urllib3
import time

class Client:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.http = urllib3.PoolManager()

    # Request the status of the current job
    def request_status(self):
        response = self.http.request("GET", self.server_url + "/status")
        return response
    
    # Create a new job and add it to the job queue
    def create_job(self):
        response = self.http.request("GET", self.server_url + "/create")
        return response
    
    # Start the next job in the queue
    def start_job(self):
        response = self.http.request("GET", self.server_url + "/start")
        return response
    
    # Continuously get the status of the job until it is completed
    def monitor_job(self): 
        curr_job_status = "N/A"
        while curr_job_status != "completed" and curr_job_status != "error":
            response = self.request_status().json()
            if response["result"] != curr_job_status:
                print("Job Status is now \"" + str(response["result"]) + "\"")
                curr_job_status = response["result"]

        
if __name__ == "__main__":
    client = Client("http://localhost:8000")
    
    client.monitor_job()
    
    response = client.create_job().json()
    print(response["result"])
    
    response = client.start_job().json()
    print(response["result"])
    
    client.monitor_job()
