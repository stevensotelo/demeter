import requests
from flask import Flask, request
app = Flask(__name__)

FILE_TOKEN = "/home/hsotelo/token.txt"
token = ""

# Adds support for GET requests to our webhook
@app.route('/webhook',methods=['GET'])
def webhook():
    verify_token = request.args.get("hub.verify_token")    
    # Check if sent token is correct
    if verify_token == token:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorise.'

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
                'recipient': {
                    'id': sender_id
                },
                'message': {"text":"Hola mundo"}
            }
        response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+token,json=request_body).json()
        return response
    return 'ok'

if __name__ == "__main__":
    # Read file
    f = open(FILE_TOKEN, "r")
    token = f.read()
    app.run(threaded=True, port=5000)