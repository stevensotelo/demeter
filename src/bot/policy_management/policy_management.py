import pandas as pd
from nlu.enums import Geographic, Cultivars, Forecast, Historical, Error
from policy_management.catalog import Catalog
from policy_management.forecast import ForecastData
from policy_management.historical import HistoricalData
from policy_management.ner import NER

class PolicyManagement:

    def __init__(self, url):
        self.url_base = url        
        self.headers = {'Content-Type': 'application/json'}
        self.catalog = Catalog(url, self.headers)
        self.forecast_data = ForecastData(url, self.headers)
        self.historical_data = HistoricalData(url, self.headers)

    # Method that search geographic places
    # (dataframe) entities: List of entities found in the message user
    def geographic(self, entities):
        answer = []
        data = self.catalog.get_Geographic()   
        # Entities weren't found
        if (len(entities) == 0):
            answer.append(NER(Geographic.STATE, data.loc[:,"state_name"].unique()))
        else:            
            # This section adds the list of localities  
            for l in entities["locality"] :
                e_data = data[(data["state_name"].str.lower().contains(l.lower())), ]
                # Check if the message has state name in order to send the municipalities
                if(e_data.shape[0] > 0):
                    answer.append(NER(Geographic.MUNICIPALITIES_STATE, e_data.loc[:,"municipality_name"].unique(), l))
                else:
                    e_data = data[(data["municipality_name"].str.lower().contains(l.lower())), ]
                    # Check if message has municipality name in order to send weather stations
                    if(e_data.shape[0] > 0):
                        answer.append(NER(Geographic.WS_MUNICIPALITY, e_data.loc[:,"ws_name"].unique(),l))
                    else:
                        e_data = data[(data["ws_name"].str.lower().contains(l.lower())), ]
                        # Check if message has weather station name in order to send the ws found
                        if(e_data.shape[0] > 0):
                            answer.append(NER(Geographic.WEATHER_STATION, e_data.loc[:,"ws_name"].unique(),l))
        return answer
    
    # Method that search cultivars available
    # (dataframe) entities: List of entities found in the message user
    def cultivars(self, entities):
        answer = []
        data = self.catalog.get_Agronomic()
        # Entities weren't found
        if (len(entities) == 0):
            answer.append(NER(Cultivars.CROP_MULTIPLE, data.loc[:,"cp_name"].unique()))
        # Entities were found
        else:
            # This section adds the list of cultivars for each crop required
            if (len(entities["crop"]) > 0):
                for c in entities["crop"] :
                    e_data = data[(data["cp_name"].str.lower() == c.lower()), ]
                    answer.append(NER(Cultivars.CROP_CULTIVAR, e_data.loc[:,"cu_name"].unique(), c))
            else:
                # This section searches the cultivars required
                if (len(entities["cultivar"]) > 0):
                    for c in entities["cultivar"] :
                        e_data = data[(data["cu_name"].str.lower().contains(c.lower())), ]
                        answer.append(NER(Cultivars.CULTIVARS_MULTIPLE, e_data.loc[:,"cu_name"].unique()))
                else:
                    answer.append(NER(Cultivars.CROP_MULTIPLE, data.loc[:,"cp_name"].unique()))
        return answer
    
    # Method that search climatology
    # (dataframe) entities: List of entities found in the message user
    def historical_climatology(self, entities):
        answer = []        
        # Entities were found
        if (len(entities) > 0):
            # Get the localities
            geographic = self.catalog.get_Geographic()            
            # Try to search if locality was reconigzed
            if(len(entities["locality"]) > 0):
                # This loop figure out all localtities through: states, municipalities and ws, which are into the message
                for l in entities["locality"] :
                    ws_data = self.get_ws(l, geographic)
                    # Check if the ws were found
                    if(ws_data.shape[0] > 0):
                        ws_id = ws_data["ws_id"].unique()
                        ws = ','.join(ws_id)
                        # Ask for the historical data
                        climatology = self.historical_data.get_Climatology(ws)
                        df = pd.merge(climatology, geographic, on='ws_id', how='inner')
                        # Filter by measure
                        if len(entities["measure"]) > 0:                            
                            dft = pd.DataFrame()
                            for m in entities["measure"] :
                                dft = dft.append(df.loc[df["measure"] == self.get_measure_from_entities(m),:], ignore_index=True)
                            if(dft.shape[0] > 0):
                                df = dft
                        # Filter by months
                        if len(entities["date"]) > 0:                            
                            for m in entities["date"] :
                                m_n = self.get_month_from_entities(m)
                                if(m_n >= 0):
                                    m_n = m_n + 1
                                    df = df.loc[df["month"] == str(m_n),:]
                        # Add all answers
                        answer.append(NER(Historical.CLIMATOLOGY, df))
                    else:
                        answer.append(NER(Error.LOCALITY_NOT_FOUND,None,getattr(l, "value")))  
            else:
                answer.append(NER(Error.MISSING_GEOGRAPHIC))
        else:
            answer.append(NER(Error.MISSING_ENTITIES))
        return answer
    
    # Method that search climate forecast
    # (dataframe) entities: List of entities found in the message user
    def forecast_climate(self, entities):
        answer = []        
        # Entities were found
        if (len(entities) > 0):
            # Get the localities
            geographic = self.catalog.get_Geographic()
            # Try to search if locality was reconigzed
            if(len(entities["locality"]) > 0):                
                # This loop figure out all localtities through: states, municipalities and ws, which are into the message
                for l in entities["locality"] :
                    ws_data = self.get_ws(l, geographic)
                    # Check if the ws were found
                    if(ws_data.shape[0] > 0):
                        ws_id = ws_data["ws_id"].unique()
                        ws = ','.join(ws_id)
                        # Ask for the forecast data
                        forecast = self.forecast.get_Climate(ws)
                        df = pd.merge(forecast, geographic, on='ws_id', how='inner')
                        answer.append(NER(Forecast.CLIMATE, df))
                    else:
                        answer.append(NER(Error.LOCALITY_NOT_FOUND,None,l))        
            else:
                answer.append(NER(Error.MISSING_GEOGRAPHIC))
        else:
            answer.append(NER(Error.MISSING_ENTITIES))
        return answer
    
    # Method that returns the measure according to aclimate platform depending of request
    # (string) value: Value to search
    def get_measure_from_entities(self, value):
        ms = 'prec'
        if('sol' in value.lower() or 'rad' in value.lower()):
            ms = 'sol_rad'
        elif ('temp' in value.lower() or 'tmp' in value.lower()):
            if('mín' in value.lower() or 'min' in value.lower()):
                ms = 't_min'
            else:
                ms = 't_max'
        return ms
    
    # Method that return the index of a month
    # (string) value: Name of month
    def get_month_from_entities(self, value):
        mo = -1
        months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        mo = [i for i, e in months if  e in value.lower()]
        return mo
    
    # Method that search ws names and ids into geographic data
    # (string) name: Name of the weather station
    # (dataframe) geographic: List of all geographic
    def get_ws(self, name, geographic):        
        # Search by weather station, muncipality and state names
        ws_data = geographic[(geographic["ws_name"].str.lower().contains(name) | geographic["state_name"].str.lower().contains(name) |geographic["municipality_name"].str.lower().contains(name)), ["ws_id","ws_name"]]
        return ws_data


