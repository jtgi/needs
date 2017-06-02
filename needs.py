from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=['POST'])
def add():
    number = request.form['From']
    message_body = request.form['Body']

    if number and message_body:
        res = MessagingResponse()
        res.message("We've alerted the sheriff. Thanks.")
        return str(res)

    return "something bad happened"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
