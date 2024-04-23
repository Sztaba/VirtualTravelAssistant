from DataAgregator import DataAgregator, DataSource
from abc import *
import pandas as pd

class Form(DataSource):
    def get_data(self):
        pass

class FormCSV(Form):
    def __init__(self, file_path_or_url:str, url: bool = False):
        self.file_path_or_url = file_path_or_url
        self.url = url
        self.data = pd.read_csv(self.file_path_or_url)
    def get_data(self):
        return self.data
    
class FormApi(Form):
    def __init__(self, api_key:str, url:str):
        self.url = url
    def get_data(self):
        # TODO: Implement API call
        return 'Data from paid... API'


class FormDataAgregator(DataAgregator):
    def __init__(self, form:Form):
        self.form = form
        self.data = self.process_data()

    def get_data(self):
        return self.form.get_data()
    
    def process_data(self):
        data = self.get_data()
        # drop timestamp and reindex with Name column
        data = data.drop(columns=['Sygnatura czasowa'])
        # rename columns fo lowwer case 
        data.columns = data.columns.str.lower()
        # rename columns 
        # Types of attractions you like best? -> places
        # What length of trips do you prefer?  -> trip_length
        # Do you enjoy spending time actively or passively? -> active
        mapp = {
            "types of attractions you like best?": "places",
            "what length of trips do you prefer? ": "trip_length",
            "do you enjoy spending time actively": "active"
            }
        data = data.rename(columns=mapp)
        
        # set index to email
        data = data.set_index('email')

        return data
    
    # email and places only
    def get_random_single_row(self):
        return self.data[['places']].sample().to_dict()
        
