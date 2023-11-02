import requests

r = requests.Session()

response = requests.get("http://127.0.0.2:8080", headers={"x-personal-header": "some-fake-data"})
print(response.text, response.status_code, response.headers)
