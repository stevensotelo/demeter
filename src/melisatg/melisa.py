import re
from flask import Flask, request, Response
import requests
import telegram

app = Flask(__name__)

FOLDER_APP = "/home/hsotelo/melisa/telegram/"
#FOLDER_APP = "/home/hsotelo/melisatg/"
#FOLDER_APP = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\facebook_client\\"
#FOLDER_APP = "/app/"
FILE_TOKEN = FOLDER_APP + "token.txt"
FILE_TOKEN_DEMETER = FOLDER_APP + "token_demeter.txt"
TOKEN = ""
with open(FILE_TOKEN, "r") as f:
    TOKEN = f.read()
MELISA_NAME = "telegram"
TOKEN_DEMETER = ""
DEMETER_URL = "https://demeter.aclimate.org/api/v1/query/"

URL = "https://melisatg.aclimate.org/"
BOT_USER_NAME = "Melisa_chatbot"
bot = None

@app.route('/')
def index():
    return '<h1>Running MelisaBot for Telegram</h1>'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    sender_id = str(update.message.chat.id)
    ext_id = str(update.message.message_id)
    try:
        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8').decode()
        #text = update.message.text    
        text = re.sub(r"\W", "_", text)
        if text != "/start":
            json = {"melisa":MELISA_NAME,"token":TOKEN_DEMETER,"user":sender_id,"chat_id":ext_id,"message":text}
            r = requests.post(DEMETER_URL, json=json)
            #url = DEMETER_URL + "?melisa=" + MELISA_NAME + "&token=" + TOKEN_DEMETER + "&user=" + sender_id + "&chat_id=" + ext_id + "&message=" + text
            #requests.get(url, timeout=1)
        return Response('ok',200)
    except Exception:
        return Response('Bad request',400)

@app.route("/receptor", methods=['POST'])
def receptor():
    data = request.get_json()
    token = data['token']
    messages = data['text']
    sender_id = data['user_id']
    chat_id = data['chat_id'] if 'chat_id' in data is None else None
    first = True
    if token == TOKEN_DEMETER:
        for m in messages:
            if first and chat_id is not None:
                bot.sendMessage(chat_id=sender_id, text=m, reply_to_message_id=chat_id)
                first = False
            else:
                bot.sendMessage(chat_id=sender_id, text=m)
    return Response('ok',200)


if __name__ == '__main__':
    with open(FILE_TOKEN_DEMETER, "r") as f:
        TOKEN_DEMETER = f.read()
    bot = telegram.Bot(token=TOKEN)

    #app.run(threaded=True, port=5000)
    app.run(host='0.0.0.0', port=5001)
    print("Start server on PORT 5001")

# Run in background
# nohup python3 melisa.py > melisa.log 2>&1 &