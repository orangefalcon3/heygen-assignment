import urllib3
import time

class Client:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.http = urllib3.PoolManager()
        self.min_delay = 0.5
        self.max_delay = 4
        self.backoff_factor = 2
        self.last_five = []

    # Request the status of the current job
    def request_status(self):
        response = self.http.request("GET", self.server_url + "/status")
        return response
    
    # Create a new 10s job and add it to the job queue
    def create_job_10(self):
        response = self.http.request("GET", self.server_url + "/create_10")
        return response
    
    # Create a new 25s job and add it to the job queue
    def create_job_25(self):
        response = self.http.request("GET", self.server_url + "/create_25")
        return response
    
    # Start the next job in the queue
    def start_job(self):
        response = self.http.request("GET", self.server_url + "/start")
        return response
    
    # Method to automatically calibrate exponential backoff to handle changes in job delays
    # Utilizes recent job history to try to take advantage of pattern matching
    def calibrate(self, elapsed_time):
        if len(self.last_five) != 0:
            et_average = sum(self.last_five) / len(self.last_five)
            et_improvement = (et_average - elapsed_time) / et_average   

            if et_improvement > 0.10:
                self.max_delay = max(self.max_delay * (0.95 - et_improvement), self.min_delay)
                self.min_delay = max(self.min_delay * (0.95 - et_improvement), 0.05)
            else:
                self.min_delay *= (1.05 - et_improvement)
                self.max_delay = min(self.max_delay * (1.05 - et_improvement), elapsed_time / 4)
        
        self.last_five.append(elapsed_time)
        if len(self.last_five) > 5:
            self.last_five.pop(0)


    # Continuously get the status of the job until it is completed
    # Utilizing oscillating exponential backoff
    def monitor_job(
            self, 
            min_delay=0.5, 
            max_delay=4, 
            backoff_factor=2, 
            oscillation=True,
            automatic=True
        ): 
        if (not automatic):
            self.min_delay = min_delay
            self.max_delay = max_delay
            self.backoff_factor = backoff_factor
        
        print("Max Delay " + str(self.max_delay))
        print("Last Five ET " + str(self.last_five))
        
        curr_job_status = "N/A"
        curr_delay = self.min_delay
        
        start_time = time.time()
        num_calls = 0
        
        while curr_job_status != "completed" and curr_job_status != "error":
            response = self.request_status().json()
            num_calls += 1
            
            if response["result"] != curr_job_status:
                print("Job Status is now \"" + str(response["result"]) + "\"")
                curr_job_status = response["result"]
                elapsed_time = time.time() - start_time
                print("Elapsed Time: " + str(elapsed_time))
            
            if curr_job_status != "completed" and curr_job_status != "error":
                time.sleep(min(curr_delay, self.max_delay))
                if oscillation and curr_delay >= self.max_delay:
                    curr_delay = self.max_delay / self.backoff_factor
                else:
                    curr_delay *= self.backoff_factor
        
        if curr_job_status == "completed":
            calls_per_sec = num_calls / elapsed_time
            self.calibrate(elapsed_time)
                
        print("Number of Calls: " + str(num_calls))
                

        
if __name__ == "__main__":
    client = Client("http://localhost:8000")

    for i in range(5):        
        response = client.create_job_10().json()
        print(response["result"])
        
        response = client.start_job().json()
        print(response["result"])
        
        client.monitor_job()
    
    for i in range(5):        
        response = client.create_job_25().json()
        print(response["result"])
        
        response = client.start_job().json()
        print(response["result"])
        
        client.monitor_job()
