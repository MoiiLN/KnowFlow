import requests
import json

res = requests.post('http://localhost:8000/api/login/', json={"username": "moi", "password": "123"})
print(res.status_code)
print(res.text)
