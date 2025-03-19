from Template.Base.base_template import BaseTemplate
from Service.ETC.csv_reader import CSVReader
import pandas as pd
import requests
import os

class CarCsvRead(BaseTemplate):
    def __init__(self, name = "CarCsvRead"):
        super().__init__(name)

def DataLoad(self, **kwargs):
        
        print("Load Call")

