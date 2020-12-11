#import urllib3
#from urllib3 import request

#import certifi
#import json
#import pandas as pd
#import requests

#from io import StringIO
#import csv

#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

#url = 'https://pronosticosapi.aclimatecolombia.org/api/Geographic/csv'
#url = 'https://pronosticosapi.aclimatecolombia.org/api/Geographic/json'
#r = http.request('GET', url)
#print(r.status)
#d = StringIO(r.data.decode('ISO-8859-1'))
#d = StringIO(r.data.decode('latin-1'))
#print(r.data)
#df = pd.read_csv(d, sep="\s*[,]\s*",engine="python")
#df = df.replace({"^\s*|\s*$":""}, regex=True)
#print(df)

#response = requests.get(url)
#print(json.loads(response.content.decode('utf-8')))
#print(response.text )

#print(pd.read_csv("https://pronosticosapi.aclimatecolombia.org/api/Geographic/csv"))

#file1 = open('G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\bot\\vocab\\intents.txt', 'r') 
#Lines = file1.readlines()
#print(Lines) 

#from nlu.enums import Intent, Slot
#print(Intent.list())
#print(Intent(2).value == 2)

from nlu.enums import Intent, Geographic, Cultivars
from nlu.nlu_tasks import NLUTasks

nlu_o  = NLUTasks(model_path = "G:\\Me\\Code\\UOC\\TFM\\demeter\\model\\demeter_model", params_path = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\bot\\vocab")    
message = "Cuando se puede sembrar en cali papa y yuca en ibague"
utterance = nlu_o.nlu(message)
print(utterance)

# import os

# params_path = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\bot\\vocab"

# #file_params = open(os.path.join(params_path,"intents.txt") , 'r')
# with open(os.path.join(params_path,"intents.txt")) as file_params:
#     intent_names = file_params.read().split("\n")
# print(intent_names)

# # Load Slots
# file_params = open(os.path.join(params_path,"slots.txt") , 'r')
# slot_names = file_params.readlines()
# slot_map = {}
# for label in slot_names:
#     slot_map[label] = len(slot_map)
# print(slot_map)

# from mongoengine import *
# from orm.orm_demeter import *
# import datetime

# connect('dialog')
# melisa = Melisa.objects.get(name="facebook")
# print(melisa.token)

# user_id = "564546"
# user = None
# if not User.objects(user_id=user_id):
#     user = User(melisa = melisa, user_id = user_id)
#     user.save()
#     print("new user")
# else:
#     user = User.objects.get(user_id=user_id)
#     print("User" + user.user_id)

# chat = Chat(user = user, text = message, date = datetime.datetime.now())
# chat.save()

# # Update chat
# chat.intent_id = utterance["intent"]
# chat.intent_name = utterance["name"]
# chat.slots = utterance["slots"]
# chat.save() 
# print(chat)