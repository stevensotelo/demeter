import requests
import datetime
from flask import Flask, request
app = Flask(__name__)

FOLDER_APP = "/home/hsotelo/melisa/facebook/"
#FOLDER_APP = "D:\\Me\\Code\\UOC\\TFM\\demeter\\src\\melisafb\\"
#FOLDER_APP = "/app/"
FILE_TOKEN = FOLDER_APP + "token.txt"
FILE_TOKEN_DEMETER = FOLDER_APP + "token_demeter.txt"
TOKEN = ""
MELISA_NAME = "facebook"
TOKEN_DEMETER = ""
DEMETER_URL = "https://demeter.aclimate.org/api/v1/query"

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Running MelisaBot for Facebook</h1>'''

# Adds support for GET requests to our webhook
@app.route('/webhook',methods=['GET','POST'])
def webhook():    
    if request.method == 'GET':
        verify_token = request.args.get("hub.verify_token") 
        challenge = request.args.get('hub.challenge')
        mode = request.args.get('hub.mode')
        print(verify_token," ",challenge," ",mode)
        if mode and verify_token:
            if mode == 'subscribe' and verify_token == TOKEN:
                print("WEBHOOK_VERIFIED")
                return challenge
        else:
            # Responds with the challenge token from the request
            return request.args.get("hub.challenge")
        return 'Unable to authorise.'
    else:
        data = request.get_json()        
        try:
            for entry in data['entry']:
                for message in entry['messaging']:
                    if message.get('message'):
                        sender_id = message['sender']['id']
                        if message['message'].get('text'):
                            text = message['message'].get('text')
                            url = DEMETER_URL + "?melisa=" + MELISA_NAME + "&token=" + TOKEN_DEMETER + "&user=" + sender_id + "&message=" + text
                            print(url)
                            request_body = {
                                    'recipient': {
                                        'id': sender_id
                                    },
                                    'message': {"text":"Hola, en breve te enviaremos una respuesta"}
                                }
                            requests.post('https://graph.facebook.com/v9.0/me/messages?access_token='+TOKEN,json=request_body)
                            requests.get(url, timeout=1)
                        else:
                            request_body = {
                                    'recipient': {
                                        'id': sender_id
                                    },
                                    'message': {"text":"Hola, lo sentimos no podemos procesar tu mensaje. Intenta solamente con texto"}
                                }
                            requests.post('https://graph.facebook.com/v9.0/me/messages?access_token='+TOKEN,json=request_body)
        except Exception:
            return 'ok'
    return 'ok'

"""
@app.route('/webhook',methods=['GET','POST'])
def webhook():
    # Parse the query params
    mode = request.values['hub.mode']
    token = request.values['hub.verify_token']
    challenge = request.values['hub.challenge']
    print(request.values['hub.mode'])
    if mode and token:
        if mode == 'subscribe' and token == TOKEN:
            print("WEBHOOK_VERIFIED")
            return challenge
        else:
            return 'Unable to authorise.'
    return 'Unable to authorise.'
"""


@app.route("/receptor", methods=['POST'])
def receptor():
    data = request.get_json()    
    token = data['token']
    messages = data['text']
    sender_id = data['user_id']
    if token == TOKEN_DEMETER:
        for m in messages:
            request_body = {
                    'recipient': {
                        'id': sender_id
                    },
                    'message': {"text":m}
                }
            requests.post('https://graph.facebook.com/v9.0/me/messages?access_token='+TOKEN,json=request_body)
    return 'ok'

if __name__ == "__main__":
    # Read file
    with open(FILE_TOKEN, "r") as f:
        TOKEN = f.read()
    with open(FILE_TOKEN_DEMETER, "r") as f:
        TOKEN_DEMETER = f.read()
    
    app.run(host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0', port=8080)
    print("Start server on PORT 5000")

# Run in background
# nohup python3.8 melisa.py > melisa.log 2>&1 &
# nohup python melisa.py > melisa.log 2>&1 &