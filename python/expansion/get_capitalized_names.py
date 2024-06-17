import pandas as pd
from tqdm import tqdm
import numpy as np

papers = pd.read_json('../../data/database/mentions/papers.json', lines=True)
cohorts = pd.read_csv('../../data/database/cohorts.csv')

# search for each cohort_name_lower in the papers title column
names = cohorts['cohort_name_lower'].unique()
titles = papers['title'].dropna().values
cap_names = []
for title in tqdm(titles):
    # searh for position of each name in the title and extract the name
    for name in names:
        if name in title.lower():
            # check position of name in title
            s_pos = title.lower().find(name)
            e_pos = s_pos + len(name)
            cap_names.append([name, title[s_pos:e_pos]])
cap_names = pd.DataFrame(cap_names, columns=['cohort_name_lower', 'cohort_name'])
# remove first 4 char from cap_name
cap_names['cohort_name'] = cap_names['cohort_name'].str[4:]
diff_names = cap_names.groupby(['cohort_name_lower', 'cohort_name']).size().reset_index(name='mentions')
diff_names = diff_names.sort_values(['mentions', 'cohort_name_lower'], ascending=False)
cohort_names = cap_names.groupby('cohort_name').size().reset_index(name='mentions')
cohort_names = cohort_names.sort_values('mentions', ascending=False)
# get all the words in cohort names
words = []
for name in tqdm(cohort_names['cohort_name']):
    words.extend(name.split())
# get the unique words and count the frequency of each word
word_count = pd.Series(words).value_counts()
# keep only words that are capitalized
word_count = word_count[word_count.index.str.istitle()]
# remove words in all caps
word_count = word_count[~word_count.index.str.isupper()]
# remove words with three or less characters
word_count = word_count[word_count.index.str.len() > 3]
# for each title, get the words in word_count
title_words = []
for title in tqdm(titles):
    # top 20 words
    top20 = word_count.head(30).index
    # get the words in title that are in top20
    tmp = set()
    for word in sorted(title.split()):
        if word in top20:
            tmp.add(word)
    if tmp:
        title_words.append([tuple(tmp), title])
title_words = pd.DataFrame(title_words, columns=['words', 'title'])
word_in_title = title_words.groupby('words').size().reset_index(name='mentions').sort_values('mentions', ascending=False)
# remove words that tuple is length > 1
word_in_title = word_in_title[word_in_title['words'].apply(lambda x: len(x) == 1)]
# explode the tuple
word_in_title = word_in_title.explode('words')
word_in_title.head(30)
# do the same for the cohort names
cohort_words = []
for name in tqdm(cohort_names['cohort_name']):
    # top 20 words
    top20 = word_count.head(30).index
    # get the words in title that are in top20
    tmp = set()
    for word in sorted(name.split()):
        if word in top20:
            tmp.add(word)
    if tmp:
        cohort_words.append([tuple(tmp), name])
cohort_words = pd.DataFrame(cohort_words, columns=['words', 'cohort_name'])
word_in_cohort = cohort_words.groupby('words').size().reset_index(name='mentions').sort_values('mentions', ascending=False)
# remove words that tuple is length > 1
word_in_cohort = word_in_cohort[word_in_cohort['words'].apply(lambda x: len(x) == 1)]
# explode the tuple
word_in_cohort = word_in_cohort.explode('words')
word_in_cohort.head(30)
keywords = ['Study', 'Biobank', 'Cohort', 'Bank', 'Project', 'Health', 'Project',
            'Survey', 'Registry', 'Biorepository', 'Program', 'Programme',
            'Initiative', 'Biocenter', 'Bioresource', 'Repository',
            'Consortium']
key = cohort_names[cohort_names['cohort_name'].str.contains('|'.join(word_in_cohort['words']))]
cohort_names.merge(key, on='cohort_name')['mentions_x'].sum()
cohort_names['cohort_name_lower'] = 'the ' + cohort_names['cohort_name'].str.lower()
cohorts['pubs'].sum()
cohorts[~cohorts['cohort_name_lower'].str.contains("|".join([x.lower() for x in keywords]), regex=True)].head(50)

