import os
import json
import requests
import datetime
import pandas as pd
import csv
import base64
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)


#next step: give user choice whether to update stock info then or use the current information as of a certain date.

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


csv_filepath = os.path.join(os.path.dirname(__file__), '..', "data", "stocklist.csv")
allstock = pd.read_csv(csv_filepath)

profile = input("Are you a retiree, young investor, or an adult?")

update = input("Do you want to update the stock info? It was last updated on date.")

if update == "yes":
    try:
        counter = 0
        listofstocks = pd.DataFrame()
        while counter < 2254:
            symbol = allstock['Ticker Symbol'][counter]
            request_url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}"
            response = requests.get(request_url)
            raw_response_text = (json.loads(response.text))
            response_text = pd.DataFrame(raw_response_text)
            listofstocks = listofstocks.append(response_text) 
            counter = counter + 1
        listofstocks = listofstocks[['symbol', 'price', 'change', 'eps', 'pe' ]]
        listofstocks.to_csv('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.csv')
    except Exception:
        pass

if update == "no":
    pass



if profile == "young":
    listofstocks = pd.read_csv('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.csv')
    listofstocks2 = listofstocks[(listofstocks['pe'] > 20)]
    listofstocks3 = listofstocks2[['symbol', 'price', 'change', 'eps', 'pe' ]]
    print(listofstocks3)

if profile == "adult":
    listofstocks = pd.read_csv('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.csv')
    listofstocks2 = listofstocks[(listofstocks['pe']< 20)]
    listofstocks3 = listofstocks2[['symbol', 'price', 'change', 'eps', 'pe' ]]
    print(listofstocks3)

if profile == "retiree":
    listofstocks = pd.read_csv('/Users/kunaalsingh/Desktop/screen-project/data/updated_stocklist.csv')
    listofstocks2 = listofstocks[(listofstocks['pe']< 12)]
    listofstocks3 = listofstocks2[['symbol', 'price', 'change', 'eps', 'pe' ]]
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





