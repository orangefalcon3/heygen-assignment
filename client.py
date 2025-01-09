import urllib3
import time

class Client:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.http = urllib3.PoolManager()

    def request_status(self):
        response = self.http.request("GET", self.server_url + "/status")
        return response
    
    def create_job(self):
        response = self.http.request("GET", self.server_url + "/create")
        return response
    
    def start_job(self):
        response = self.http.request("GET", self.server_url + "/start")
        return response
        
if __name__ == "__main__":
    client = Client("http://localhost:8000")
    curr_job_status = "N/A"
    while True:
        response = client.request_status().json()
        if response["result"] != curr_job_status:
            print("Job Status has been changed to " + str(response["result"]))
            curr_job_status = response["result"]
        if response["result"] == "completed":
            break
        time.sleep(1)
    curr_job_status = "N/A"
    response = client.create_job().json()
    print(response["result"])
    response = client.start_job().json()
    print(response["result"])
    while True:
        response = client.request_status().json()
        if response["result"] != curr_job_status:
            print("Job Status has been changed to " + str(response["result"]))
            curr_job_status = response["result"]
        if response["result"] == "completed":
            break
        time.sleep(1)
