import gspread
import fortunes
import datetime

from flask import Flask, request
from random import randint
from twilio.twiml.messaging_response import MessagingResponse
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Revolver Needs").sheet1

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

    return str(MessagingResponse().message(message))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
