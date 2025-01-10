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
    # Utilizing oscillating exponential backoff
    def monitor_job(self, min_delay=0.5, max_delay=8, backoff_factor=2): 
        start_time = time.time()
        curr_job_status = "N/A"
        curr_delay = min_delay
        num_calls = 0
        while curr_job_status != "completed" and curr_job_status != "error":
            response = self.request_status().json()
            
            num_calls += 1
            if response["result"] != curr_job_status:
                print("Job Status is now \"" + str(response["result"]) + "\"")
                curr_job_status = response["result"]
                print("Elapsed Time: " + str(time.time() - start_time))
            time.sleep(min(curr_delay, max_delay))
            print(curr_delay)
            if curr_delay >= max_delay:
                curr_delay = max_delay / backoff_factor
            else:
                curr_delay *= backoff_factor
        print("Number of Calls: " + str(num_calls))
                

        
if __name__ == "__main__":
    client = Client("http://localhost:8000")
    
    response = client.create_job().json()
    print(response["result"])
    
    response = client.start_job().json()
    print(response["result"])
    
    client.monitor_job()
