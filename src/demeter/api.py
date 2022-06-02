import flask
from flask import request
import requests
from mongoengine import *
from orm.orm_demeter import *
import datetime

from nlu.enums import Intent, Commands
from nlu.nlu_tasks import NLUTasks
from policy_management.policy_management import PolicyManagement
from policy_management.ner import NER
from nlg.generator import Generator

from conf import config

app = flask.Flask(__name__)

nlu_o = None

# Home page
@app.route('/', methods=['GET'])
def home():
    return "<h1>Demeter Bot</h1>"

# Register melisa
@app.route('/api/v1/melisa/', methods=['GET'])
def register_melisa():
    if config['ENABLE_REGISTER_MELISA']:
        name = request.args.get("name")    
        if not Melisa.objects(name=name) :
            melisa = Melisa(name = name, url_post = request.args.get("url_post"), token = request.args.get("token"))
            melisa.save()
            return "OK"
        else:
            return "ERROR"
    else:
        return "Not enable"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/query/', methods=['GET'])
def api_query():
    # Validate if melisa exists into the database
    say_wait = True
    if not Melisa.objects(name=request.args.get("melisa")):
        return "ERROR 1"
    else:
        melisa = Melisa.objects.get(name=request.args.get("melisa"))
        # Validate authentication
        if(melisa.token == request.args.get("token")):
            policy = PolicyManagement(config["ACLIMATE_API"],config["COUNTRIES"])
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
                request_body = {"user_id": user_id, "token": melisa.token, "chat_id":chat_id, "text": ["Hola, soy Melisa, un bot que provee información agroclimática.","Si no sabes como iniciar y necesitas ayuda solo escribeme: ayuda"]}
                say_wait = False
                response = requests.post(melisa.url_post,json=request_body)
            else:
                user = User.objects.get(user_id=user_id)

            # Create chat
            chat = Chat(user = user, text = message, date = datetime.datetime.now(), ext_id = chat_id)
            chat.save()

            # message
            message = message.replace("_"," ")
            print(message)
            answer = []
            # Check some especial words
            if message.startswith(("hola", "hi", "Hola", "HOLA")) :
                answer.append(NER(Commands.HI))
                chat.intent_id = 6
                chat.intent_name = "hi"
                chat.slots = {}
                chat.save()
            elif message.startswith(("bye", "adios", "Bye", "BYE", "ADIOS", "chao")):
                answer.append(NER(Commands.BYE))
                chat.intent_id = 7
                chat.intent_name = "bye"
                chat.slots = {}
                chat.save()
            elif message.startswith(("help","ayuda","Help", "HELP", "Ayuda", "Ayuda")):
                answer.append(NER(Commands.HELP))
                chat.intent_id = 8
                chat.intent_name = "help"
                chat.slots = {}
                chat.save()
            elif "thanks" in message or "gracias" in message:
                answer.append(NER(Commands.THANKS))
                chat.intent_id = 9
                chat.intent_name = "thanks"
                chat.slots = {}
                chat.save()
            else:
                # Temporal message
                if say_wait:
                    rb_tmp = {"user_id": user_id, "token": melisa.token, "chat_id":chat_id, "text": ["Estoy procesando tu pregunta"]}
                    response = requests.post(melisa.url_post,json=rb_tmp)
                # Decoded message
                utterance = nlu_o.nlu(message)
                print(utterance)
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
                elif(intent == Intent.FORECAST_YIELD):
                    answer = policy.forecast_yield(entities)
                elif(intent == Intent.FORECAST_DATE):
                    answer = policy.forecast_yield(entities, best_date=True)

            answers = Generator.print(answer)
            #answers += ["En estos momentos estoy aprendiendo a responder a tus preguntas, por favor ayúdame a mejorar con esta encuesta: https://demeter.paperform.co/?4ctj8=" + str(chat.pk)]
            request_body = {"user_id": user_id, "token": melisa.token, "chat_id":chat_id, "text": answers}
            response = requests.post(melisa.url_post,json=request_body)
            print("User",user_id,"Message sent")
            return 'ok'
        else:
            return "ERROR 2"

if __name__ == "__main__":
    # Connect with database
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")

    # It starts the model for NLU
    nlu_o  = NLUTasks(model_path = config['MODEL_PATH'], params_path = config['PARAMS_PATH'])
    print("NLU loaded")

    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'], debug=config['DEBUG'])

# nohup python api.py > demeter.log 2>&1 &