from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "123456")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == 'POST':
        data = request.json
        if MAKE_WEBHOOK_URL:
            requests.post(MAKE_WEBHOOK_URL, json=data)
        return "OK", 200

@app.route('/')
def index():
    return '✅ Webhook Meta → Make opérationnel.'

if __name__ == '__main__':
    app.run(debug=True)
