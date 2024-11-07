import requests

url = "http://127.0.0.1:5000/process_audio"
data = {"target_lang": "sw"}

response = requests.post(url, json=data)
print(response.json())
