import os
import json
import requests
import pandas

symbol = input("Please input a ticker: ")


request_url = f"https://financialmodelingprep.com/api/v3/company/profile/{symbol}"
response = requests.get(request_url)
raw_response_text = (json.loads(response.text))
print(raw_response_text['profile']['description'])
#weeklyresponse = requests.get(weekly_url)
#parsed_response = json.loads(response.text)
#parsed_weekly = json.loads(weeklyresponse.text)