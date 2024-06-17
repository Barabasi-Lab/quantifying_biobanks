import pandas as pd
import json
import re
from tqdm import tqdm
from unidecode import unidecode
from glob import glob

# read json file from bquery data directory
with open('../../data/bquery/cohort_names_bq.json', 'r') as f:
    data = json.load(f)
# make a pandas dataframe
df = pd.DataFrame(data)
# set value to papers to int
df['papers'] = df['papers'].astype(int)
# convert everything to ascii
df['cohort_name'] = df['cohort_name'].apply(lambda x: x.encode('ascii', 'ignore').decode())
# unidecode every cohort name
df['cohort_name'] = df['cohort_name'].apply(lambda x: unidecode(x))
# replace every \n or \t or \s or double space with a single space
df['cohort_name'] = df['cohort_name'].apply(lambda x: re.sub(r'[\n\t\s]+', ' ', x))
# replace 'the' with 'The' in cohort names
df['cohort_name'] = df['cohort_name'].apply(lambda x: re.sub(r'^the', 'The', x))
# sort by papers descending
df = df.sort_values('papers', ascending=False)
# groupby cohort_name and kind and sum papers
df = df.groupby(['cohort_name', 'kind']).sum().reset_index()
# groupby cohort_name, get the first kind and papers
df = df.groupby('cohort_name').agg({'kind': 'first', 'papers': 'max'}).reset_index()
# sort by papers descending
df = df.sort_values('papers', ascending=False)
# remove cohort names with less than 5 papers
df = df[df['papers'] >= 5]
# remove cohorts with two 'the' in their name or one 'and'
df = df[~df['cohort_name'].str.contains('the the', case=False)]
# remove cohorts with word "and" and less than 2 papers
df = df[~((df['cohort_name'].str.contains(' and ', case=False)) & (df['papers'] < 2))]
# save in data/cohorts directory
df.to_csv('../../data/cohorts/bq_cohorts.csv', index=False)

# read cohort_names.csv from train directory
df_train = pd.read_csv('../../data/train/cohort_names.csv')
df_clean = pd.read_csv('../../data/train/clean_cohort_names.csv')
# add the word 'The' to all cohort names in df_train and df_clean if they don't start with 'The'
df_train['cohort_name'] = df_train['cohort_name'].apply(lambda x: 'The ' + x if not x.lower().startswith('the') else x)
df_clean['cohort_name'] = df_clean['cohort_name'].apply(lambda x: 'The ' + x if not x.lower().startswith('the') else x)
# list of cohort names in df
df_names = set(df['cohort_name'].str.lower().tolist())
# list of cohort names in df_train
train_names = set(df_train['cohort_name'].str.lower().tolist())
# list of cohort names in df_clean
clean_names = set(df_clean['cohort_name'].str.lower().tolist())
# list of all cohort names
df_and_train = set(df_names & train_names)
df_and_clean = set(df_names & clean_names)
all_names = df_names | train_names | clean_names
# make a dataframe with all cohort names with the union of dataframes df, df_train and df_clean
df_all = pd.concat([df, df_train, df_clean]).drop_duplicates().reset_index(drop=True)
# make column with lower case cohort names
df_all['cohort_name_lower'] = df_all['cohort_name'].str.lower()
# keep only cohort_name column
df_all = df_all[['cohort_name']]
# save in data/train directory
# remove starting the from df_all ignorecase
df_all['cohort_name'] = df_all['cohort_name'].apply(lambda x: re.sub(r'^the ', '', x, flags=re.IGNORECASE))
# remove '"' and ',' from cohort_name
df_all['cohort_name'] = df_all['cohort_name'].apply(lambda x: re.sub(r'["\,]', '', x))
# sort values
df_all = df_all.sort_values('cohort_name')
# remove names starting with single letter word
df_all = df_all[~df_all['cohort_name'].str.contains(r'^[a-zA-Z\d]\s')]
# remove cohorts with a single word
df_all = df_all[~df_all['cohort_name'].str.contains(r'^\w+$')]
# unidecode cohort names
df_all['cohort_name'] = df_all['cohort_name'].apply(lambda x: unidecode(x))
# remove trailing and double spaces
df_all['cohort_name'] = df_all['cohort_name'].apply(lambda x: ' '.join(x.split()))
# drop duplicates
df_all = df_all.drop_duplicates()
df_all.to_csv('../../data/train/cohort_names_all.csv', index=False)