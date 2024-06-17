import pandas as pd
import requests
import json

cohorts = pd.read_csv('../../../data/expansion/cohorts.csv')
cohort_names = cohorts['cohort_name_lower'].to_list()

API_KEY = "AIzaSyBsUR5AP6bpWLrwwIPid3EXaITyeG8OHug"
SEARCH_ENGINE = "31a8c6002de144d1c"
URL = "https://www.googleapis.com/customsearch/v1"

params = {
    'q': 'the uk biobank',
    'key': API_KEY,
    'cx': SEARCH_ENGINE,
    'num': 10,
    'exactTerms': 'the uk biobank'
}

r = requests.get(URL, params=params)
data = r.json()