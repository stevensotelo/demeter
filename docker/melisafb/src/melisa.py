import requests
import datetime
from flask import Flask, request
app = Flask(__name__)

FOLDER_APP = "/home/hsotelo/"
#FOLDER_APP = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\facebook_client\\"
#FOLDER_APP = "/app/"
FILE_TOKEN = FOLDER_APP + "token.txt"
TOKEN = ""

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Running MelisaBot for Facebook</h1>'''

'''
# Adds support for GET requests to our webhook
@app.route('/webhook',methods=['GET'])
def webhook():
    verify_token = request.args.get("hub.verify_token")    
    print("token: " + TOKEN)
    #print("verify: " + verify_token)
    # Check if sent token is correct
    if verify_token == TOKEN:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorise.'
'''
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
        response = requests.post('https://graph.facebook.com/v9.0/me/messages?access_token='+TOKEN,json=request_body).json()
        return response
    return 'ok'


if __name__ == "__main__":
    # Read file
    f = open(FILE_TOKEN, "r")
    TOKEN = f.read()
    f.close()
    #app.run(host="0.0.0.0", threaded=True, port=443)
    #app.run(threaded=True, port=443)
    #app.run(host="0.0.0.0", threaded=True, port=80)
    app.run(host='0.0.0.0', port=80)

# Run in background
# nohup python3.8 melisa.py > melisa.log 2>&1 &