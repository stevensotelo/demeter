import urllib3
from urllib3 import request

import certifi
import json
import pandas as pd
import requests

from io import StringIO
import csv

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

from nlu.enums import Intent, Slot
print(Intent.list())
print(Intent(2).value == 2)