import os
import json
import requests
import time
import datetime
import stat
import pandas as pd
import csv
import base64
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from time import strptime

def mkt_cap_format(x):
    return "${:.1f}M".format(x/1000000)

def vol_format(x):
    return "{:.1f}M".format(x/1000000)

def send_email():
    load_dotenv()
    date = datetime.date.today()
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
    MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
    SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
    file_path = os.path.join(os.path.dirname(__file__), '..', "data", "final_list.csv")
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('text/csv')
    attachment.file_name = FileName('final_list.csv')
    attachment.disposition = Disposition('attachment')
    template_data = {"human_friendly_timestamp": date.strftime("%B %d, %Y")}
    client = SendGridAPIClient(SENDGRID_API_KEY) 
    message = Mail(from_email=MY_EMAIL_ADDRESS, to_emails=MY_EMAIL_ADDRESS)
    message.template_id = SENDGRID_TEMPLATE_ID 
    message.dynamic_template_data = template_data
    message.attachment = attachment
    try:
        client.send(message)
    except Exception as e:
        print("Oops, Sendgrid is down. Our bad.", e)

def convert_modtime_to_date(path):
    fileStatsObj = os.stat(path)
    modificationTime = time.ctime(fileStatsObj[stat.ST_MTIME])
    return datetime.datetime.strptime(modificationTime,'%a %b %d %H:%M:%S %Y').strftime('%m/%d/%y')


if __name__=="__main__":
    csv_filepath = os.path.join(os.path.dirname(__file__), '..', "data", "full_list.csv")
    allstock = pd.read_csv(csv_filepath)

    profile = input("Are you a retiree, young investor, or an adult? ")

    while True:
        wtp = input("What is the maximum you are willing to pay for a share of stock? ")
        if wtp.isnumeric() == False:
            print("Invalid number. Try again.")
            exit
        else:
            break

    while True:
        liquidity = input("Do you care about liquidity in the stock (volume >1m)? Reply yes or no. ")
        if liquidity in ("yes", "Yes", "YES"):
            liquidity = True
            break
        else:
            liquidity = False
            break   
    update_time = convert_modtime_to_date('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.pkl')
    update = input("Do you want to update the stock info? It was last updated on" + " " + update_time + "." + " ")

    while True:
        if update in ("yes", "Yes", "YES"):
            try:
                counter = 0
                listofstocks = pd.DataFrame()
                while counter < 2352:
                    symbol = allstock['Ticker Symbol'][counter]
                    request_url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}"
                    response = requests.get(request_url)
                    raw_response_text = (json.loads(response.text))
                    response_text = pd.DataFrame(raw_response_text)
                    listofstocks = listofstocks.append(response_text)
                    counter = counter + 1
                listofstocks.to_pickle('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.pkl')
                break
            except Exception:
                continue
            break
        if update in ("no", "No", "NO"):
            break

    if profile in ("young", "young investor"):
        listofstocks = pd.read_pickle('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.pkl')
        listofstocks2 = listofstocks[(listofstocks['pe'] > 20)]
        listofstocks2 = listofstocks2[(listofstocks2['price'])<float(wtp)]
        if liquidity == True:
            listofstocks2 = listofstocks2[(listofstocks2['avgVolume'])>1000000]
        elif liquidity == False:
            pass
        listofstocks2.loc[:, 'marketCap'] = listofstocks2.loc[:, 'marketCap'].apply(mkt_cap_format)
        listofstocks2.loc[:, 'avgVolume'] = listofstocks2.loc[:, 'avgVolume'].apply(vol_format)
        listofstocks3 = listofstocks2[['symbol', 'price', 'yearHigh', 'yearLow', 'eps', 'pe','marketCap', 'avgVolume']]
        print(listofstocks3)
    if profile == "adult":
        listofstocks = pd.read_pickle('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.pkl')
        listofstocks2 = listofstocks[(listofstocks['pe']< 20)]
        listofstocks2 = listofstocks2[(listofstocks2['price'])<float(wtp)]
        if liquidity == True:
            listofstocks2 = listofstocks2[(listofstocks2['avgVolume'])>1000000]
        else:
            pass
        listofstocks2.loc[:, 'marketCap'] = listofstocks2.loc[:, 'marketCap'].apply(mkt_cap_format)
        listofstocks2.loc[:, 'avgVolume'] = listofstocks2.loc[:, 'avgVolume'].apply(vol_format)
        listofstocks3 = listofstocks2[['symbol', 'price', 'yearHigh', 'yearLow', 'eps', 'pe','marketCap', 'volume']]
        print(listofstocks3)
    if profile == "retiree":
        listofstocks = pd.read_pickle('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.pkl')
        listofstocks2 = listofstocks[(listofstocks['pe']< 12)]
        listofstocks2 = listofstocks2[(listofstocks2['price'])<float(wtp)]
        if liquidity == True:
            listofstocks2 = listofstocks2[(listofstocks2['avgVolume'])>1000000]
        else:
            pass    
        listofstocks2.loc[:, 'marketCap'] = listofstocks2.loc[:, 'marketCap'].apply(mkt_cap_format)
        listofstocks2.loc[:, 'avgVolume'] = listofstocks2.loc[:, 'avgVolume'].apply(vol_format)
        listofstocks3 = listofstocks2[['symbol', 'price', 'yearHigh', 'yearLow', 'eps', 'pe','marketCap', 'avgVolume']]
        print(listofstocks3)
    spread = input("Do you want to export this output to a spreadsheet sent to your email? If you do, enter yes.")
    while True:
        if spread == "yes":
            print("Ok, processing now. Thanks!")
            listofstocks3.to_csv('/Users/kunaalsingh/Desktop/screen-project/data/final_list.csv')
            send_email()
            break
        elif spread == "no":
            print("Ok, sounds good. Thanks for using our service.")
            break
        else:
            print("Sorry, didn't get that, please reply either yes or no.")



