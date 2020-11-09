import pandas as pd
from nlu.enums import Geographic, Cultivars
from policy_management.catalog import Catalog

class PolicyManagement:

    def __init__(self, url):
        self.url_base = url        
        self.headers = {'Content-Type': 'application/json'} # 'application/json'
        self.catalog = Catalog(url, self.headers)

    # Method that search geographic places
    # (enum) type: Type of search
    # (string) value: Value to search. By default it is None 
    def geographic(self, type, value = None):
        localities = []
        data = self.catalog.get_Geographic()        
        if(type == Geographic.STATE):            
            # List all states
            if(value == None):
                localities = data.loc[:,"state_name"].unique()
            # Filter municipalities by state
            else:
                localities = data.loc[data["state_name"] == value,"municipality_name"].unique()
        elif(type == Geographic.MUNICIPALITY):            
            # List all municipalities
            if(value == None):
                localities = data.loc[:,"municipality_name"].unique()
            # Filter ws by municipalities
            else:
                localities = data.loc[places["municipality_name"] == value,"weather_stations"].unique()
            
        return localities
    
    # Method that search cultivars available
    # (enum) type: Type of search. By deafult it is Cultivars.CROP
    # (string) value: Value to search. By default it is None 
    def cultivars(self, type = Cultivars.CROP, value = None):
        cu = []
        data = self.catalog.get_Agronomic()                
        if(type == Cultivars.CROP):
            # List all crops
            if(value == None):                
                cu = data.loc[:,"cp_name"].unique()
            # Filter crops
            else:
                cu = data.loc[data["cp_name"] == value,"cu_name"].unique()
        elif(type == Cultivars.CULTIVARS):            
            # List all cultivars
            if(value == None):                
                cu = data.loc[:,["cp_name","cu_name"]]
            # Filter ws by municipalities
            else:
                cu = data.loc[(data["cp_name"] == value | data["cu_name"] == value) ,"cu_name"].unique()
            cu.drop_duplicates()
        return cu

