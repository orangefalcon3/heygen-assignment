import urllib3
import time

class Client:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.http = urllib3.PoolManager()

    def request_status(self):
        response = self.http.request("GET", self.server_url + "/status")
        return response
        
if __name__ == "__main__":
    client = Client("http://localhost:8000")
    while True:
        response = client.request_status().json()
        print(response["result"])
        if response["result"] == "completed":
            break
        time.sleep(1)