import time
import requests
import os
from dotenv import load_dotenv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
tickers = []

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

response = requests.get(url)
data = response.json()
for ticker in data['results']:
    tickers.append(ticker)

print(len(tickers))

while 'next_url' in data and data['next_url']:
    time.sleep(12)  # To respect rate limits
    next_url = data['next_url'] + f"&apiKey={POLYGON_API_KEY}"
    response = requests.get(next_url)
    data = response.json()
    for ticker in data['results']:
        tickers.append(ticker)
    print(len(tickers))

print(len(tickers))
