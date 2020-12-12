import pandas as pd
import requests
import json

class HistoricalData:

    def __init__(self, url, headers):
        self.url_base = url
        self.headers = headers
    
    # Method that search climate forecast
    # return: None if couldn't connect with the service, Otherwise a DataFrame with the data 
    def get_Climatology(self, ws):
        # Set the url for getting data        
        api_url = self.url_base + 'Historical/Climatology/' + ws + '/json'
        # Send the request to the web api
        response = requests.get(api_url, headers=self.headers, verify=False)        
        if response.status_code == 200: 
            # Load all states with their information
            json_data = json.loads(response.content.decode('utf-8'))
            df = pd.DataFrame()
            # Build a dataframe just with climatology data
            for w in json_data:
                for m in w['monthly_data']:
                    for d in m['data']:
                        df = df.append(pd.Series([w['weather_station'], m['month'], d['measure'], d['value']]), ignore_index=True);
            df.columns = ["ws_id", "month", "measure", "value"]
            return df
        else:
            return None