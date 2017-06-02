from flask import Flask, request
from twilio import twiml

app = Flask(__name__)

@app.route("/", methods=['POST'])
def add():
    number = request.form['From']
    message_body = request.form['Body']

    if number and message_body:
        res = twiml.Response()
        res.message("We've alerted the sheriff. Thanks.")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
