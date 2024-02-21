import requests
import json

def api_request(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data
