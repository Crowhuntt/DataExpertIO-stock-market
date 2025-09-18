import time
import requests
import os
import csv
from dotenv import load_dotenv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
tickers = []

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

# Call the API and get a response
response = requests.get(url)
# Parse the JSON response
data = response.json()
print(data)
# Extract tickers from the response
for ticker in data['results']:
    tickers.append(ticker)

# Handle pagination
# JSON last element is 'next_url' which contains the URL for the next page of results, if it exists
while 'next_url' in data and data['next_url']:
    print("Requesting next page...")
    # Polygon’s RESTful APIs free tier subscriptions come with a limit of 5 API requests per minute, so we pause for 12 seconds before making the next request.
    time.sleep(12)
    # Make a request to the next_url
    next_url = data['next_url'] + f"&apiKey={POLYGON_API_KEY}"
    response = requests.get(next_url)
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)

# Print the total number of tickers retrieved
print(len(tickers))

# Set ticker schema to output to CSV file
ticker_schema = ['ticker', 'name', 'market', 'locale', 'primary_exchange', 'type', 'active', 'currency_name', 'cik', 'composite_figi', 'share_class_figi', 'last_updated_utc']

# Export tickers to CSV
with open('tickers.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=ticker_schema)
    writer.writeheader()
    for ticker in tickers:
        # Only write fields present in schema
        row = {key: ticker.get(key, '') for key in ticker_schema}
        writer.writerow(row)

