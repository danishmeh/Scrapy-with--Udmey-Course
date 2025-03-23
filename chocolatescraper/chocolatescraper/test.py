import requests
from urllib.parse import urlencode

API_KEY = '90d87a96-d350-4abf-8f89-8377c44bf9a7'
target_url = 'https://www.chocolate.co.uk/collections/all'
proxy_url = f'https://proxy.scrapeops.io/v1/?{urlencode({"api_key": API_KEY, "url": target_url})}'

response = requests.get(proxy_url)
print(f"Status Code: {response.status_code}")
print(response.text[:500])  # Print snippet of response
