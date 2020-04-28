import os
import json
import requests
import pandas as pd
import csv

csv_filepath = os.path.join(os.path.dirname(__file__), '..', "data", "stocklist.csv")
allstock = pd.read_csv(csv_filepath)

profile = input("Are you a retiree, young investor, or an adult?")


try:
    counter = 0
    listofstocks = pd.DataFrame()
    while counter < 2500:
        symbol = allstock['Ticker Symbol'][counter]
        request_url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}"
        response = requests.get(request_url)
        raw_response_text = (json.loads(response.text))
        response_text = pd.DataFrame(raw_response_text)
        listofstocks = listofstocks.append(response_text) 
        counter = counter + 1
    listofstocks = listofstocks[['symbol', 'price', 'change', 'eps', 'pe' ]]        
except Exception:
    pass



if profile == "young":
    listofstocks = listofstocks[(listofstocks['pe'] > 20)]
    listofstocks = listofstocks[['symbol', 'price', 'change', 'eps', 'pe' ]]
    print(listofstocks)

if profile == "adult":
    listofstocks == listofstocks[(listofstocks['pe']< 20)]
    listofstocks = listofstocks[['symbol', 'price', 'change', 'eps', 'pe' ]]
    print(listofstocks)

if profile == "retiree":
    listofstocks == listofstocks[(listofstocks['pe']< 12)]
    listofstocks = listofstocks[['symbol', 'price', 'change', 'eps', 'pe' ]]
    print(listofstocks)

