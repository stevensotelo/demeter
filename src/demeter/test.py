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

#from nlu.enums import Intent, Geographic, Cultivars
#from nlu.nlu_tasks import NLUTasks

#nlu_o  = NLUTasks(model_path = "G:\\Me\\Code\\UOC\\TFM\\demeter\\model\\demeter_model", params_path = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\bot\\vocab")    
#message = "Cuando se puede sembrar en cali papa y yuca en ibague"
#utterance = nlu_o.nlu(message)
#print(utterance)

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

#from mongoengine import *
#from orm.orm_demeter import *
#import datetime

#connect('dialog')
#connect('dialog', host='192.168.199.74', port=27017)
#melisa = Melisa(name = "facebook", url_post = "https://melisafb.aclimatecolombia.org/receptor", token = "Melis@Fb2020")
#melisa.save()
#print(melisa.token)

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

from transformers import BertTokenizer
import tensorflow as tf
from tensorflow import keras
from nlu.nlu_tasks import NLUTasks
from nlu.enums import Intent, Geographic, Cultivars, Commands

"""
print("Loading tokenizer")
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
print("Loading model")
model2 = tf.saved_model.load("/home/hsotelo/demeter/demeter")


print("Loading preparing all")

intent_names = ['forecast_yield','forecast_precipitation', 'climatology', 'cultivars', 'places', 'forecast_date']
intent_map = dict((label, idx) for idx, label in enumerate(intent_names))
slot_names = ["[PAD]"]
slot_names += ["B-crop","B-cultivar","I-cultivar","B-locality","I-locality","B-measure","I-measure","B-date","I-date","B-unit","I-unit","O"]
slot_map = {}
for label in slot_names:
    slot_map[label] = len(slot_map)

def decode_predictions(text, tokenizer, intent_names, slot_names,intent_id, slot_ids):
    info = {"intent": intent_names[intent_id]}
    collected_slots = {}
    active_slot_words = []
    active_slot_name = None
    for word in text.split():
        tokens = tokenizer.tokenize(word)
        current_word_slot_ids = slot_ids[:len(tokens)]
        slot_ids = slot_ids[len(tokens):]
        current_word_slot_name = slot_names[current_word_slot_ids[0]]
        if current_word_slot_name == "O":
            if active_slot_name:
                collected_slots[active_slot_name] = " ".join(active_slot_words)
                active_slot_words = []
                active_slot_name = None
        else:
            # Naive BIO: handling: treat B- and I- the same...
            new_slot_name = current_word_slot_name[2:]
            if active_slot_name is None:
                active_slot_words.append(word)
                active_slot_name = new_slot_name
            elif new_slot_name == active_slot_name:
                active_slot_words.append(word)
            else:
                collected_slots[active_slot_name] = " ".join(active_slot_words)
                active_slot_words = [word]
                active_slot_name = new_slot_name
    if active_slot_name:
        collected_slots[active_slot_name] = " ".join(active_slot_words)
    info["slots"] = collected_slots
    return info

def nlu(text, tokenizer, my_model, intent_names, slot_names):
    inputs = tf.constant(tokenizer.encode(text))[None, :]  # batch_size = 1
    outputs = my_model(inputs)
    slot_logits, intent_logits = outputs
    #print(slot_logits.numpy())
    slot_ids = slot_logits.numpy().argmax(axis=-1)[0, 1:-1]
    #print(slot_ids)
    intent_id = intent_logits.numpy().argmax(axis=-1)[0]

    return decode_predictions(text, tokenizer, intent_names, slot_names,intent_id, slot_ids)
"""

print("Loading model")
nlu  = NLUTasks(model_path = "/home/hsotelo/demeter/demeter", params_path = "/home/hsotelo/demeter/service/vocab")    

oraciones = ["Cual es la mejor variedad para sembrar en Tolima", "climatologia en ibague", "lluvias en tolima", "mejor cultivar de arroz en Cerete"]
for o in oraciones:
    print(o)
    #print(model2.predict(o))    
    #print(nlu(o,tokenizer, model2, intent_names, slot_names))
    print(nlu.nlu(o))