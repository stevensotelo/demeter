import flask
from flask import request, jsonify
from nlu.enums import Intent, Geographic, Cultivars
from policy_management.policy_management import PolicyManagement
from nlg.generator import Generator




app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Demeter Bot</h1>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/request/query', methods=['GET'])
def api_query():
    
    policy = PolicyManagement("https://pronosticosapi.aclimatecolombia.org/api/")
    answer = []

    intent = Intent.LIST_CULTIVARS
    type = Cultivars.CULTIVARS
    entities = None
    
    if(intent == Intent.LIST_PLACES):
        answer = policy.geographic(type, entities)
    elif(intent == Intent.LIST_CULTIVARS):
        answer = policy.cultivars(type, value)
    elif(intent == Intent.HISTORICAL_CLIMATOLOGY):
        answer = policy.historical_climatology(type, value)
    elif(intent == Intent.FORECAST_CLIMATE):
        answer = policy.forecast_climate(type, value)
    
    return jsonify(Generator.print(answer))

app.run()