import requests
import json
import time

url = "http://127.0.0.1:8000/blogs"
headers = {"Content-Type": "application/json"}
data = {
    "topic": "Cricket",
    "language": "Bangla"
}

print(f"Sending POST request to {url} with data: {data}")
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
