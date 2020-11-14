import pandas as pd
import requests
import json

class ForecastData:

    def __init__(self, url, headers):
        self.url_base = url
        self.headers = headers
    
    # Method that search climate forecast
    # return: None if couldn't connect with the service, Otherwise a DataFrame with the data 
    def get_Climate(self, ws):
        # Set the url for getting data        
        api_url = self.url_base + 'Forecast/Climate/' + ws + '/true/json'
        # Send the request to the web api
        response = requests.get(api_url, headers=self.headers)        
        if response.status_code == 200: 
            # Load all states with their information
            json_data = json.loads(response.content.decode('utf-8'))
            df = pd.DataFrame()
            # Build a dataframe just with probabilities data
            for w in json_data['climate']:
                for m in w['data']:
                    for d in m['probabilities']:
                        df = df.append(pd.Series(w['weather_station'], m['year'], m['month'], d['measure'], d['lower'], d['normal'], d['upper']));
            df.columns = ["ws_id", "year", "month", "measure", "lower", "normal", "upper"]
        return df