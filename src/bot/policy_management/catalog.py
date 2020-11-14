import pandas as pd
import requests
import json

class Catalog:

    def __init__(self, url, headers):
        self.url_base = url
        self.headers = headers
    
    # Method that search all geographic locations in the aclimate platform
    # return: None if couldn't connect with the service, Otherwise a DataFrame with the data 
    def get_Geographic(self):
        # Set the url for getting data
        api_url = '{0}Geographic/json'.format(self.url_base)
        # Send the request to the web api
        response = requests.get(api_url, headers=self.headers)        
        if response.status_code == 200: 
            # Load all states with their information
            json_data = json.loads(response.content.decode('utf-8'))
            df = pd.DataFrame()
            # Build a dataframe just with geographic data
            for s in json_data:                
                for m in s['municipalities']:
                    for w in m['weather_stations']:
                        df = df.append(pd.Series([s['country'], s['id'], s['name'], m['id'], m['name'], w['id'], w['name'], w['origin']]), ignore_index=True)
            df.columns = ["country_name", "state_id", "state_name", "municipality_id", "municipality_name", "ws_id", "ws_name", "ws_origin"]
        return df
    
    # Method that search all cultivars available in the aclimate platform
    # return: None if couldn't connect with the service, Otherwise a DataFrame with the data 
    def get_Agronomic(self):
        # Set the url for getting data
        api_url = '{0}Agronomic/true/json'.format(self.url_base)
        # Send the request to the web api
        response = requests.get(api_url, headers=self.headers)        
        if response.status_code == 200: 
            # Load all states with their information
            json_data = json.loads(response.content.decode('utf-8'))
            df = pd.DataFrame()
            # Build a dataframe just with geographic data
            for cp in json_data:                
                for cu in cp['cultivars']:
                    df = df.append(pd.Series([cp['cp_id'], cp['cp_name'], cu['id'], cu['name'], cu['rainfed'], cu['national']]), ignore_index=True)
            df.columns = ["cp_id", "cp_name", "cu_id", "cu_name", "cu_rainfed", "cu_national"]
        return df