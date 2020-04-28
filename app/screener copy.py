import os
import json
import requests
import pandas

profile = input("Are you a retiree, young investor, or an adult?")


if profile == "young":
    print("ok")

if profile == "adult":
    print("ok")

if profile == "retiree":
    print("ok")



#symbol = input("Please input a ticker: ")
#
#
request_url = f"https://financialmodelingprep.com/api/v3/company/stock/list"
response = requests.get(request_url)
raw_response_text = (json.loads(response.text))
print(raw_response_text)
#weeklyresponse = requests.get(weekly_url)
#parsed_response = json.loads(response.text)
#parsed_weekly = json.loads(weeklyresponse.text)