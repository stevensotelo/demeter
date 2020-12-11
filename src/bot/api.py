import flask
from flask import request, jsonify
import requests

from nlu.enums import Intent, Geographic, Cultivars
from nlu.nlu_tasks import NLUTasks

from policy_management.policy_management import PolicyManagement

from nlg.generator import Generator

import pandas as pd

from mongoengine import *
from orm.orm_demeter import *
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True

nlu_o = None
aclimate = "https://pronosticosapi.aclimatecolombia.org/api/"

# Home page
@app.route('/', methods=['GET'])
def home():
    return "<h1>Demeter Bot</h1>"

# Register melisa
@app.route('/api/v1/melisa/', methods=['GET'])
def register_melisa():
    name = request.args.get("name")    
    if not Melisa.objects(name=name) :
        melisa = Melisa(name = name, url_post = request.args.get("url_post"), token = request.args.get("token"))
        melisa.save()
        return "OK"
    else:
        return "ERROR"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/query/', methods=['GET'])
def api_query():
    
    # Validate autentication of melisa
    if not Melisa.objects(name=request.args.get("melisa")):
        return "ERROR 1"
    else:
        melisa = Melisa.objects.get(name=request.args.get("melisa"))

        if(melisa.token == request.args.get("token")):
            policy = PolicyManagement(aclimate)
            user = None
            user_id = request.args.get("user")
            message = request.args.get("message")
            chat_id = ""
            if request.args.get("chat_id"):
                chat_id = request.args.get("chat_id")
            # Check if user exists, otherwise it will create
            if not User.objects(user_id=user_id):
                user = User(melisa = melisa, user_id = user_id)
                user.save()
                request_body = {"user": user_id, "token": melisa.token, "chat_id":chat_id, "text": "Hola, soy Melisa, un bot que provee información agroclimática."}
                response = requests.post(melisa.url_post,json=request_body).json()
            else:
                user = User.objects.get(user_id=user_id)

            # Create chat
            chat = Chat(user = user, text = message, date = datetime.datetime.now(), ext_id = chat_id)
            chat.save()

            # Decoded message
            utterance = nlu_o.nlu(message)

            # Update chat
            chat.intent_id = utterance["intent"]
            chat.intent_name = utterance["name"]
            chat.slots = utterance["slots"]
            chat.save()            

            intent = Intent(utterance["intent"])    
            entities = utterance["slots"]
            
            if(intent == Intent.PLACES):
                answer = policy.geographic(entities)
            elif(intent == Intent.CULTIVARS):
                answer = policy.cultivars(entities)
            elif(intent == Intent.CLIMATOLOGY):
                answer = policy.historical_climatology(entities)
            elif(intent == Intent.FORECAST_PRECIPITATION):
                answer = policy.forecast_climate(entities)
            
            answers = Generator.print(answer)
            request_body = {"user": user_id, "token": melisa.token, "chat_id":chat_id, "text": answers}
            response = requests.post(melisa.url_post,json=request_body).json()
            return 'ok'
        else:
            return "ERROR 2"

if __name__ == "__main__":
    #     
    nlu_o  = NLUTasks(model_path = "G:\\Me\\Code\\UOC\\TFM\\demeter\\model\\demeter_model", params_path = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\bot\\vocab")    
    # Connect with database
    #connect('mongodb://dialog:56456@localhost:27017/dialog')
    connect('dialog')
    
    app.run(threaded=True, port=5000)
    #app.run(host='0.0.0.0', port=80)