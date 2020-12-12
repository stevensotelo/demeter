import re
from flask import Flask, request
import requests
import telegram

app = Flask(__name__)

FOLDER_APP = "/home/hsotelo/melisatg/"
#FOLDER_APP = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\facebook_client\\"
#FOLDER_APP = "/app/"
FILE_TOKEN = FOLDER_APP + "token.txt"
FILE_TOKEN_DEMETER = FOLDER_APP + "token_demeter.txt"
TOKEN = ""
with open(FILE_TOKEN, "r") as f:
    TOKEN = f.read()
MELISA_NAME = "telegram"
TOKEN_DEMETER = ""
DEMETER_URL = "https://demeter.aclimatecolombia.org/api/v1/query"

URL = "https://melisatg.aclimatecolombia.org"
BOT_USER_NAME = "MelisaDAbot"
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

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    text = re.sub(r"\W", "_", text)
    if text != "/start":
        url = DEMETER_URL + "?melisa=" + MELISA_NAME + "&token=" + TOKEN_DEMETER + "&user=" + sender_id + "&chat_id=" + ext_id + "&message=" + text
        requests.get(url)

    return 'ok'

@app.route("/receptor", methods=['POST'])
def receptor():
    data = request.get_json()
    token = data['token']
    messages = data['text']
    sender_id = data['user_id']
    chat_id = data['chat_id']    
    if token == TOKEN_DEMETER:
        for m in messages:
            bot.sendMessage(chat_id=sender_id, text=m)
    return 'ok'


if __name__ == '__main__':
    with open(FILE_TOKEN_DEMETER, "r") as f:
        TOKEN_DEMETER = f.read()
    bot = telegram.Bot(token=TOKEN)

    #app.run(threaded=True, port=5000)
    app.run(host='0.0.0.0', port=81)

# Run in background
# nohup python3.8 melisa.py > melisa.log 2>&1 &