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
        if (entities.shape[0] == 0):
            answer.append(NER(Geographic.STATE, data.loc[:,"state_name"].unique()))
        else:
            e_type = entities.loc[(entities["type"].str.isin(["b-locality"])), ]
            localities =  entities.loc[(entities["type"].str.isin(["b-locality"])), ]
            # This section adds the list of localities  
            for l in localities_s.itertuples(index=True, name='Pandas') :
                e_data = data[(data["state_name"].str.lower().contains(getattr(l, "value"))), ]
                # Check if the message has state name in order to send the municipalities
                if(e_data.shape[0] > 0):
                    answer.append(NER(Geographic.MUNICIPALITIES_STATE, e_data.loc[:,"municipality_name"].unique(), getattr(l, "value")))
                else:
                    e_data = data[(data["municipality_name"].str.lower().contains(getattr(l, "value"))), ]
                    # Check if message has municipality name in order to send weather stations
                    if(e_data.shape[0] > 0):
                        answer.append(NER(Geographic.WS_MUNICIPALITY, e_data.loc[:,"ws_name"].unique(),getattr(l, "value")))
                    else:
                        e_data = data[(data["ws_name"].str.lower().contains(getattr(l, "value"))), ]
                        # Check if message has weather station name in order to send the ws found
                        if(e_data.shape[0] > 0):
                            answer.append(NER(Geographic.WEATHER_STATION, e_data.loc[:,"ws_name"].unique(),getattr(l, "value")))
        return answer
    
    # Method that search cultivars available
    # (dataframe) entities: List of entities found in the message user
    def cultivars(self, entities):
        answer = []
        data = self.catalog.get_Agronomic()
        # Entities weren't found
        if (entities.shape[0] == 0):
            answer.append(NER(Cultivars.CROP_MULTIPLE, data.loc[:,"cp_name"].unique()))
        # Entities were found
        else:
            e_type = entities.loc[(entities["type"].str.isin(["b-crop"]) & entities["type"].str.isin(["b-cultivar"])), ]
            # Specific list of crops and cultivars
            if(e_type.shape[0] > 0):
                crops =  entities.loc[(entities["type"].str.isin(["b-crop"])), ]
                # This section adds the list of cultivars for each crop required
                if (crops.shape[0] > 0):
                    for c in crops.itertuples(index=True, name='Pandas') :
                        e_data = data[(data["cp_name"].str.lower() == getattr(c, "value")), ]
                        answer.append(NER(Cultivars.CROP_CULTIVAR, e_data.loc[:,"cu_name"].unique(), getattr(c, "value")))
                else:
                    # This section searches the cultivars required
                    cultivars =  entities.loc[(entities["type"].str.isin(["b-cultivar"])), ]
                    if (cultivars.shape[0] > 0):
                        for c in cultivars.itertuples(index=True, name='Pandas') :
                            e_data = data[(data["cu_name"].str.lower().contains(getattr(c, "value"))), ]
                            answer.append(NER(Cultivars.CULTIVARS_MULTIPLE, e_data.loc[:,"cu_name"].unique()))
        return answer
    
    # Method that search climatology
    # (dataframe) entities: List of entities found in the message user
    def historical_climatology(self, entities):
        answer = []        
        # Entities were found
        if (entities.shape[0] > 0):
            # Get the localities
            geographic = self.catalog.get_Geographic()
            e_type = entities.loc[(entities["type"].str.isin(["b-locality"])), ]
            # Try to search if locality was reconigzed
            if(e_type.shape[0] > 0):
                localities =  entities.loc[(entities["type"].str.isin(["b-locality"])), ]
                # This section check if a locality was found
                if (localities.shape[0] > 0):
                    # This loop figure out all localtities through: states, municipalities and ws, which are into the message
                    for l in localities.itertuples(index=True, name='Pandas') :
                        ws_data = self.get_ws(getattr(l, "value"), geographic)
                        # Check if the ws were found
                        if(ws_data.shape[0] > 0):
                            ws_id = ws_data["ws_id"].unique()
                            ws = ','.join(ws_id)
                            # Ask for the historical data
                            climatology = self.historical_data.get_Climatology(ws)
                            df = pd.merge(climatology, geographic, on='ws_id', how='inner')
                            # Filter by measure
                            measures = entities.loc[(entities["type"].str.isin(["b-measure"])), ]
                            if measures.shape[0] > 0:
                                me = measures.loc[:,"value"].unique()
                                for m in me :
                                    df = df.loc[df["measure"] == get_measure_from_entities(m),:]
                            # Filter by months
                            months = entities.loc[(entities["type"].str.isin(["b-date"])), ]
                            if months.shape[0] > 0:
                                mo = months.loc[:,"value"].unique()
                                for m in mo :
                                    m_n = get_month_from_entities(m)
                                    if(m_n >= 0):
                                        m_n = m_n + 1
                                        df = df.loc[df["month"] == str(m_n),:]
                            # Add all answers
                            answer.append(NER(Historical.CLIMATOLOGY, df))
                        else:
                            answer.append(NER(Error.LOCALITY_NOT_FOUND,None,getattr(l, "value")))        
                else:
                    answer.append(NER(Error.MISSING_GEOGRAPHIC))
        return answer
    
    # Method that search climate forecast
    # (dataframe) entities: List of entities found in the message user
    def forecast_climate(self, entities):
        answer = []        
        # Entities were found
        if (entities.shape[0] > 0):
            # Get the localities
            geographic = self.catalog.get_Geographic()
            e_type = entities.loc[(entities["type"].str.isin(["b-locality"])), ]
            # Try to search if locality was reconigzed
            if(e_type.shape[0] > 0):
                localities =  entities.loc[(entities["type"].str.isin(["b-locality"])), ]
                # This loop figure out all localtities through: states, municipalities and ws, which are into the message
                for l in localities.itertuples(index=True, name='Pandas') :
                    ws_data = self.get_ws(getattr(l, "value"), geographic)
                    # Check if the ws were found
                    if(ws_data.shape[0] > 0):
                        ws_id = ws_data["ws_id"].unique()
                        ws = ','.join(ws_id)
                        # Ask for the forecast data
                        forecast = self.forecast.get_Climate(ws)
                        df = pd.merge(forecast, geographic, on='ws_id', how='inner')
                        answer.append(NER(Forecast.CLIMATE, df))
                    else:
                        answer.append(NER(Error.LOCALITY_NOT_FOUND,None,getattr(l, "value")))        
            else:
                answer.append(NER(Error.MISSING_GEOGRAPHIC))

        return answer

    
    # Method that returns the measure according to aclimate platform depending of request
    # (string) value: Value to search
    def get_measure_from_entities(value):
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
    def get_month_from_entities(value):
        mo = -1
        months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        mo = [i for i, e in months if  e in value.lower()]
        return mo
    
    # Method that search ws names and ids into geographic data
    # (string) name: Name of the weather station
    # (dataframe) geographic: List of all geographic
    def get_ws(name, geographic):        
        # Search by weather station, muncipality and state names
        ws_data = geographic[(geographic["ws_name"].str.lower().contains(name) | geographic["state_name"].str.lower().contains(name) |geographic["municipality_name"].str.lower().contains(name)), ["ws_id","ws_name"]]
        return ws_data


