import pandas as pd


fo = pd.read_csv('../../data/foundation/uk_biobank.csv')

fo[fo['doi'] == '10.1371/journal.pmed.1001779']