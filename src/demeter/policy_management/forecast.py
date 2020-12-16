import pandas as pd
import requests
import json

class ForecastData:

    def __init__(self, url, headers):
        self.url_base = url
        self.headers = headers
    
    # Method that search climate forecast
    # return: Dataframe empty if couldn't connect with the service, Otherwise a DataFrame with the data 
    def get_Climate(self, ws):
        # Set the url for getting data        
        api_url = self.url_base + 'Forecast/Climate/' + ws + '/true/json'                
        # Send the request to the web api        
        response = requests.get(api_url, headers=self.headers, verify=False)        
        if response.status_code == 200: 
            # Load all states with their information
            df = pd.DataFrame()
            json_data = json.loads(response.content.decode('utf-8'))            
            # Build a dataframe just with probabilities data
            for w in json_data['climate']:
                for m in w['data']:
                    for d in m['probabilities']:
                        df = df.append(pd.Series([w['weather_station'], m['year'], m['month'], d['measure'], d['lower'], d['normal'], d['upper']]), ignore_index=True)
            if df.shape[0] > 0:
                df.columns = ["ws_id", "year", "month", "measure", "lower", "normal", "upper"]
                return df
            else:
                return None
        else:
            return None
        
    
    # Method that search yield forecast
    # return: None if couldn't connect with the service, Otherwise a DataFrame with the data 
    def get_Yield(self, ws):
        # Set the url for getting data        
        api_url = self.url_base + 'Forecast/Yield/' + ws + '/json'                
        # Send the request to the web api
        response = requests.get(api_url, headers=self.headers, verify=False)        
        if response.status_code == 200: 
            # Load all states with their information
            df = pd.DataFrame()
            json_data = json.loads(response.content.decode('utf-8'))            
            # Build a dataframe just with probabilities data
            for w in json_data['yield']:
                for y in w['yield']:
                    for d in y['data']:
                        df = df.append(pd.Series([w['weather_station'], y['cultivar'], y['soil'], y['start'], y['end'], d['measure'], d['avg'], d['min'], d['max'],d['sd'],d['conf_lower'],d['conf_upper']]), ignore_index=True)
            if df.shape[0] > 0:
                df.columns = ["ws_id", "cu_id", "so_id", "start", "end", "measure", "avg", "min", "max", "sd", "conf_lower","conf_upper"]
                return df
            else:
                return None
        else:
            return None