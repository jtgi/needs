import gspread
import fortunes
import datetime
import os

from flask import Flask, request
from random import randint
from twilio.twiml.messaging_response import MessagingResponse
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

app = Flask(__name__)

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
sheriff = "+16047209499"
#sheriff = "+12063932973"
inbound = "+16046702633"

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Revolver Needs").sheet1
twilio_client =  Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route("/", methods=['POST'])
def add():
    number = request.form['From']
    message_body = request.form['Body']
    message = "Something went wrong. Try again?"

    if number and message_body:
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        sheet.insert_row([time, number, message_body], 2)
        fort = fortunes.list[randint(0, len(fortunes.list))]
        message = "The sheriff has been alerted.\nYour fortune: {}.".format(fort)
	sheriff_msg = "New task:\n\n{}\nFrom: {}\n\nneeds.revolvercoffee.ca".format(message_body, number)
	twilio_client.messages.create(to=sheriff, from_=inbound, body=sheriff_msg)

    return str(MessagingResponse().message(message))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
