import urllib3
import time
import json

class Client:

    # Initialize the client
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
    
    # Create a new job and add it to the job queue
    def create_job(self, length=10):
        post_body = json.dumps({
            "length": length,
        })
        response = self.http.request('POST', self.server_url + '/create',
                 headers={'Content-Type': 'application/json'},
                 body=post_body)
        return response
    
    
    # Start the next job in the queue
    def start_job(self):
        response = self.http.request("GET", self.server_url + "/start")
        return response
    
    # Method to automatically calibrate exponential backoff to handle changes in job delays
    # Utilizes recent job history to try to take advantage of pattern matching
    def calibrate(self, elapsed_time):

        # Check if there is any existing history
        if len(self.last_five) != 0:

            # Find average elapsed time in history
            et_average = sum(self.last_five) / len(self.last_five)

            # Find improvement when compared to average
            et_improvement = (et_average - elapsed_time) / et_average   
            
            if et_improvement > 0.10:
                # Decrease delay parameters if the execution time is lowered
                self.max_delay = max(self.max_delay * (0.95 - et_improvement), max(self.min_delay, elapsed_time / 10))
                self.min_delay = max(self.min_delay * (0.95 - et_improvement), 0.05)
            else:
                # Increase delay parameters if the execution time is increased
                self.min_delay *= (1.05 - et_improvement)
                self.max_delay = min(self.max_delay * (1.05 - et_improvement), elapsed_time / 4)
        
        # Update history
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

        # Set parameters manually if no auto-calibration
        if (not automatic):
            self.min_delay = min_delay
            self.max_delay = max_delay
            self.backoff_factor = backoff_factor
        
        curr_job_status = "N/A"

        # Set spacing between calls
        curr_delay = self.min_delay
        
        # Initialize metrics
        start_time = time.time()
        num_calls = 0
        
        while curr_job_status != "completed" and curr_job_status != "error":

            # Request status
            response = self.request_status().json()
            num_calls += 1
            
            # Check if there is a status change
            if response["result"] != curr_job_status:

                # Print status update
                print("Job Status is now \"" + str(response["result"]) + "\"")

                # Update status
                curr_job_status = response["result"]

                # Find elapsed time
                elapsed_time = time.time() - start_time
            
            # Check if job is still running
            if curr_job_status != "completed" and curr_job_status != "error":

                # Wait until next call
                time.sleep(min(curr_delay, self.max_delay))

                # Update spacing
                if oscillation and curr_delay >= self.max_delay:
                    curr_delay = self.max_delay / self.backoff_factor
                else:
                    curr_delay *= self.backoff_factor
        
        # Auto-calibrate if needed
        if automatic and curr_job_status == "completed":
            self.calibrate(elapsed_time)
        
        # Print Error Message
        if curr_job_status == "error":
            print("An error has occurred in this job")
                
        # Print Metric
        print("Number of Calls: " + str(num_calls))
