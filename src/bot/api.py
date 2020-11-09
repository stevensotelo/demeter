import flask
from flask import request, jsonify
from nlu.enums import Intent, Geographic, Cultivars
from policy_management.policy_management import PolicyManagement




app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Demeter Bot</h1>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/request/query', methods=['GET'])
def api_query():
    
    policy = PolicyManagement("https://pronosticosapi.aclimatecolombia.org/api/")
    answer = ""

    intent = Intent.LIST_CULTIVARS
    type = Cultivars.CULTIVARS
    value = None

    if(intent == Intent.LIST_PLACES):
        localities = policy.geographic(type, value)
        for l in localities:
            answer = answer + l + ", "
        answer = "Los sitios disponibles son: " + answer[:-3]
    elif(intent == Intent.LIST_CULTIVARS):
        cultivar = policy.cultivars(type, value)
        if(type == Cultivars.CROP):
            for cu in cultivar:
                answer = answer + cu + ", "            
        elif(type == Cultivars.CROP):
            for cp in cultivar.loc[:,["cp_name"]].unique():
                answer = answer + c + ": "        
                for cu in cultivar.loc[cultivar["cp_name"] == cp,["cu_name"]].unique():
                    answer = answer + cu + ", "
        
        answer = "Los cultivares disponibles son: " + answer[:-3]

    return jsonify(answer)

app.run()