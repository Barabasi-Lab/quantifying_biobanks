import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# set a seaborn style for a research paper
sns.set_style('whitegrid')
sns.set_context('paper')
sns.set(font_scale=1.5)

COLLECTIONS = '../../data/raw_cohorts/eu_bbmri_eric_collections_2023-10-06_04_09_28.csv'
BIOBANKS = '../../data/raw_cohorts/eu_bbmri_eric_biobanks_2023-09-27_18_23_17.csv'

data = pd.read_csv(COLLECTIONS)
bb = pd.read_csv(BIOBANKS)

biobanks = data.dropna(subset=['Categories']).groupby('Biobank label')['Categories'].unique().to_frame()
cancer_biobanks = biobanks[biobanks['Categories'].apply(lambda x: 'Cancer' in x)]