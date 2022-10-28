import pandas as pd
import gspread
#from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class AgriLac:

    # Method Construct
    # (string) key: Path where the key is located
    # (string) file: Id file in google sheets
    # (string) sheet: Sheet's name in the google sheets file
    # (string[]) scopes: Url of the websites where the system should sign in
    def __init__(self, key, file, sheet, scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']):
        self.key = key
        self.file = file
        self.sheet = sheet
        self.scopes = scopes
        self.gs = None
    
    # Method that sign in the system with Google
    def sign(self):
        credentials = Credentials.from_service_account_file(self.key, scopes=self.scopes)
        gc = gspread.authorize(credentials)
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)
        # open a google sheet
        self.gs = gc.open_by_key(self.file)

    # Method that save information into sheet in google
    # (dataframe) text: Text that should be saved in the document
    def dato_preliminar(self, text):
        data = text.splitlines()
        df = pd.DataFrame(data)
        answer = "ok"
        try:
            self.sign()
            self.gs.values_append(self.sheet, {'valueInputOption': 'RAW'}, {'values': df.values.tolist()})
        except Exception as err:
            answer = "error"
            print(f"Unexpected {err=}, {type(err)=}")
        return answer
        
