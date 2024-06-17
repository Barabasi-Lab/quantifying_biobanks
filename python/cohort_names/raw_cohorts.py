"""
clean raw cohort files
Author: Rodrigo Dorantes-Gilardi
email: r.dorantesgilardi[at]northeastern[dot]edu
"""

import re
import pandas as pd
import numpy as np
from glob import glob
import html


def remove_parenthesis(cohort):
    pattern = re.compile('\(.*\)')
    if pattern.search(cohort):
        match = pattern.search(cohort)
        start = match.start()
        end = match.end()
        return cohort[:start].strip() + cohort[end:]
    else:
        return cohort


# 1 EU BBMRI
EU_BBMRI = '../../data/raw_cohorts/eu_bbmri_eric_collections_2023-10-06_04_09_28.csv'
eu_bbmri = pd.read_csv(EU_BBMRI)
# remove parenthesis from Biobank label column
eu_bbmri['Biobank label'] = eu_bbmri['Biobank label'].apply(remove_parenthesis)
eu_bbmri['Biobank label'].value_counts()
# remove everything after colon
eu_bbmri['Biobank label'] = eu_bbmri['Biobank label'].str.split(':').str[0]
# get number of words in Biobank label column
eu_bbmri['Label_words'] = eu_bbmri['Biobank label'].str.split().str.len()
eu_bbmri[eu_bbmri['Label_words'] == 3]['Biobank label'].value_counts()
# 1 if biobank in label, 0 otherwise
keywords = r"bio|ban[kc]|repo|colle|study|cohort|project|survey|program|registry|database|initiative|consortium|network"
eu_bbmri['biobank'] = eu_bbmri['Biobank label'].str.contains(
    keywords, case=False).astype(int)
eu_bbmri[eu_bbmri['biobank'] == 1]['Biobank label'].value_counts()
# 1 if starts with "the", 0 otherwise
eu_bbmri['the'] = eu_bbmri['Biobank label'].str.startswith(r'The').astype(int)
eu_bbmri[eu_bbmri['the'] == 1]['Biobank label'].value_counts()
eu_bbmri = eu_bbmri[(eu_bbmri['biobank'] == 1) | (
    eu_bbmri['the'] == 1) | (eu_bbmri['Label_words'] == 1)]
eu_names = pd.read_csv('../../data/cohorts/eu_bbmri_cohorts.csv')
eu_names = eu_names[eu_names['cohort_name'].isin(eu_bbmri['Biobank label'])]
eu_names.to_csv('../../data/cohorts/eu_bbmri_cohorts.csv', index=False)

# 2 Scicrunch cohorts
scicrunch = pd.read_csv('../../data/raw_cohorts/scicrunch_cohorts.csv')
# remove parenthesis from Resource Name column
scicrunch['Resource Name'] = scicrunch['Resource Name'].apply(
    remove_parenthesis)
# remove everything after colon or dash
scicrunch['Resource Name'] = scicrunch['Resource Name'].str.split(':').str[0]
scicrunch['Resource Name'] = scicrunch['Resource Name'].str.split('-').str[0]
scicrunch = scicrunch.dropna(axis=1, how='all')
scicrunch['biobank'] = scicrunch['Resource Name'].str.contains(
    keywords, case=False).astype(int)
scicrunch = scicrunch[scicrunch['biobank'] == 1]
scicrunch['cohort_name'] = scicrunch['Resource Name']
scicrunch.to_csv('../../data/cohorts/scicrunch_cohorts.csv', index=False)

# 3 Molgenis cohorts
molgenis = pd.read_csv('../../data/raw_cohorts/molgenis_cohorts.csv')
# only column "type" in "Biobank", "Population cohort", "Birth cohort"
molgenis = molgenis[molgenis['type'].isin(
    ['Biobank', 'Population cohort', 'Birth cohort'])]
molgenis['biobank'] = molgenis['cohort_name'].str.contains(
    keywords, case=False).astype(int)
molgenis = molgenis[molgenis['biobank'] == 1]
molgenis.to_csv('../../data/cohorts/molgenis_cohorts.csv', index=False)

# 4 read cedcd_cohorts.csv from data/cohorts directory
cedcd = pd.read_csv('../../data/cohorts/cedcd_cohorts.csv')
# 5 read dceg_cohorts.csv from data/cohorts directory
dceg = pd.read_csv('../../data/cohorts/dceg_cohorts.csv')
# 6 read dpuk_cohorts.csv from data/cohorts directory
dpuk = pd.read_csv('../../data/cohorts/dpuk_cohorts.csv')
# 7 read epnd_cohorts.csv from data/cohorts directory
epnd = pd.read_csv('../../data/cohorts/epnd_cohorts.csv')
# 8 read iadrp_cohorts.csv from data/cohorts directory
iadrp = pd.read_csv('../../data/cohorts/iadrp_cohorts.csv')
# 9 read jpnd_cohorts.csv from data/cohorts directory
jpnd = pd.read_csv('../../data/cohorts/jpnd_cohorts.csv')
# 10 read maelstrom_cohorts.csv from data/cohorts directory
maelstrom = pd.read_csv('../../data/cohorts/maelstrom_cohorts.csv')
# 11 read pooling_cohorts.csv from data/cohorts directory
pooling = pd.read_csv('../../data/cohorts/pooling_cohorts.csv')
# 12 read ukri_cohorts.csv from data/cohorts directory
ukri = pd.read_csv('../../data/cohorts/ukri_cohorts.csv')
# make a list of all cohort names
cohorts = [cedcd, dceg, dpuk, epnd, iadrp, jpnd, maelstrom,
           pooling, ukri, eu_names, scicrunch, molgenis]
# merge all cohorts only using cohort_name column
all_cohorts = pd.concat(cohorts).reset_index(drop=True)
all_cohorts = all_cohorts[['cohort_name']]
all_cohorts = all_cohorts.drop_duplicates().reset_index(drop=True)
# apply html.unescape to cohort_name column
all_cohorts['cohort_name'] = all_cohorts['cohort_name'].apply(html.unescape)
# replace "’" with "'"
all_cohorts['cohort_name'] = all_cohorts['cohort_name'].str.replace('’', "'")
# replace " " with " "
all_cohorts['cohort_name'] = all_cohorts['cohort_name'].str.replace(' ', ' ')
# replace "–" with "-"
all_cohorts['cohort_name'] = all_cohorts['cohort_name'].str.replace('–', '-')
# replace " " with " "
all_cohorts['cohort_name'] = all_cohorts['cohort_name'].str.replace(' ', ' ')
# remove single word cohort names
all_cohorts = all_cohorts[~all_cohorts['cohort_name'].str.contains(r'^\w+$')]
# save in data/cohorts directory
all_cohorts.to_csv('../../data/cohorts/main_cohorts.csv', index=False)
# 13 read cohorts.txt from data/chat_gpt directory
gpt = pd.read_csv('../../data/chat_gpt/cohorts.txt', sep=' - ')
# concatenate with all_cohorts on cohort_name column
all_gpt = pd.concat([all_cohorts, gpt[["cohort_name"]]]).reset_index(drop=True)
# remove parenthesis from cohort_name column
all_gpt['cohort_name'] = all_gpt['cohort_name'].apply(remove_parenthesis)
# ignore cohorts with a parenthesis
all_gpt = all_gpt[~all_gpt['cohort_name'].str.contains(r'\(')]
all_gpt = all_gpt[~all_gpt['cohort_name'].str.contains(r'\)')]
# 14 read bq_cohorts.csv from data/cohorts directory
bq = pd.read_csv('../../data/cohorts/bq_cohorts.csv')
# concatenate with all_gpt on cohort_name column
all_gpt = pd.concat([all_gpt, bq[['cohort_name']]]).reset_index(drop=True)

# cohorts starting with "the" capitalize them
all_gpt['cohort_name'] = all_gpt['cohort_name'].apply(
    lambda x: re.sub(r'^the ', 'The ', x, flags=re.IGNORECASE))
# those that don't start with "the" add "The" at the beginning
all_gpt['cohort_name'] = all_gpt['cohort_name'].apply(
    lambda x: 'The ' + x if not x.lower().startswith('the') else x)
# strip of leading and trailing spaces
all_gpt['cohort_name'] = all_gpt['cohort_name'].str.strip()
# remove double spaces
all_gpt['cohort_name'] = all_gpt['cohort_name'].apply(
    lambda x: ' '.join(x.split()))
# drop duplicates
all_gpt = all_gpt.drop_duplicates().reset_index(drop=True)
all_gpt['lower'] = all_gpt['cohort_name'].str.lower()
# replace the first word "The" with "[Tt]he"
all_gpt['cohort_name'] = all_gpt['cohort_name'].apply(
    lambda x: re.sub(r'^The ', '[Tt]he ', x))
# save in data/cohorts directory
# remove names with length less than 10 in lower
all_gpt = all_gpt[all_gpt['lower'].str.len() >= 10]
# drop duplicates cohort_name column
all_gpt = all_gpt.drop_duplicates('cohort_name').reset_index(drop=True)
all_gpt.columns = ['cohort_name', 'cohort_name_lower']
all_gpt.to_csv('../../data/cohorts/final_cohorts.csv', index=False)
