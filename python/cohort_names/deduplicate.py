# Dedpulicating cohort name records
import pandas as pd
import re
from thefuzz import fuzz

# read cohort names
df = pd.read_csv('../../data/train/cohort_names.csv')
cohorts = df['cohort_name'].unique().tolist()
candidates = []
_id = 0
seen = dict()
for i in range(len(cohorts) - 1):
    _id += 1
    for j in range(i + 1, len(cohorts)):
        ratio = fuzz.partial_ratio(cohorts[i], cohorts[j])
        if ratio >= 99:
            if cohorts[i] in seen:
                e_id = seen[cohorts[i]]
            elif cohorts[j] in seen:
                e_id = seen[cohorts[j]]
            else:
                e_id = _id
            seen[cohorts[i]] = e_id
            seen[cohorts[j]] = e_id
            candidates.append((cohorts[i], cohorts[j], ratio, e_id))
df = pd.DataFrame(candidates, columns=['name_1', 'name_2', 'ratio', 'id'])
# for each row, if "name_1" is a substring of "name_2" or viceversa, add a "The" at the beginning of the substring

for i, row in df.iterrows():
    if row['name_1'].lower().startswith(row['name_2']):
        df.loc[i, 'name_1'] = 'The ' + row['name_1']
    elif row['name_2'].lower().startswith(row['name_1']):
        df.loc[i, 'name_2'] = 'The ' + row['name_2']

repeated = set(df['name_1'].to_list() + df['name_2'].to_list())
non_repeated = [cohort for cohort in cohorts if cohort not in repeated]
both = list(repeated) + non_repeated
clean = pd.DataFrame({'cohort_name': both})
# remove cohort names with only one word
clean['n_words'] = clean['cohort_name'].apply(lambda x: len(x.split(' ')))
clean = clean[clean['n_words'] > 1]
clean = clean[clean['n_words'] <= 10]
# remove everything after "&" including the "&"
pattern = re.compile('(.*)\s&.*')
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: pattern.sub(r'\1', x))
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: x.replace('’', "'"))
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: x.replace('&#8217;', "'"))
clean['cohort_name'] = clean['cohort_name'].apply(lambda x: x.replace('"', ""))
# if word "study" in name but not "the" at beginning, add "the"


def add_the(x):
    if 'study' in x.lower() and not x.lower().startswith('the'):
        return 'The ' + x
    else:
        return x


clean['cohort_name'] = clean['cohort_name'].apply(add_the)
# remove everything after a parenthesis
pattern = re.compile('(.*)\s\(.*')
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: pattern.sub(r'\1', x))
# remove every name containing a comma
clean = clean[~clean['cohort_name'].str.contains(',')]
# for names with ":" separate into two and only keep the part that contains one of the keywords


def split_colon(x):
    if ':' in x:
        start = x.find(':')
        end = len(x)
        if any(keyword in x[start:end].lower() for keyword in ['cohort', 'study', 'program', 'survey', 'project', 'biobank']):
            return x[start+1:end]
        elif any(keyword in x[0:start].lower() for keyword in ['cohort', 'study', 'program', 'survey', 'project', 'biobank']):
            return x[0:start]
        else:
            return x
    else:
        return x


clean['cohort_name'] = clean['cohort_name'].apply(split_colon)
# remove " [fr]" from names
pattern = re.compile('(.*)\s\[fr\]')
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: pattern.sub(r'\1', x))
clean = clean[~clean['cohort_name'].str.contains(
    r"[^\w\s\'-\/\!]", regex=True)]
# replace study cohort with Study
pattern = re.compile('study cohort', flags=re.IGNORECASE)
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: pattern.sub('Study', x))
# remove everything after " - "
pattern = re.compile('(.*)\s-\s.*')
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: pattern.sub(r'\1', x))
pattern = re.compile(r'(.*)\s\/\s.*')
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: pattern.sub(r'\1', x))
tmp = clean[clean['cohort_name'].str.contains(
    r'study [^(of)|(in)|(biobank)]', case=False)]
# remove everything after the first occurence of "Study" in tmp
pattern = re.compile('(.*Study).*')
tmp['cohort_name'] = tmp['cohort_name'].apply(lambda x: pattern.sub(r'\1', x))
clean = clean[~clean['cohort_name'].str.contains(
    r'study [^(of)|(in)|(biobank)]', case=False)]
# remove everythin after "- " in clean
pattern = re.compile('(.*)\s?-\s.*')
clean['cohort_name'] = clean['cohort_name'].apply(
    lambda x: pattern.sub(r'\1', x))
# append tmp to clean
clean = clean.append(tmp)
clean = clean.drop_duplicates(subset=['cohort_name'])
main_keyworkds = ['cohort', 'study', 'program', 'survey', 'project', 'biobank', 'bank', 'respository']
keywords = ['cohort', 'stud', 'program', 'survey', 'project', 'bank',
            'repository', 'health', 'genetics', 'genomics', 'network', 'clinic', 'research',
            'men', r'bio[^\s]+', 'consortium', 'children', 'life', 'all', 'database', 'regist',
            'investigation', 'archive', 'collection', 'born', 'birth', 'kid', 'adult',
            'grow', 'banca', 'banque', 'initiative', 'outcome', 'disease'
            ]
# count words for cohort_name in clean
clean['n_words'] = clean['cohort_name'].apply(lambda x: len(x.split(' ')))
clean = clean[clean['n_words'] > 1]
# remove names starting or ending with a space
clean = clean[~clean['cohort_name'].str.startswith(' ')]
clean = clean[~clean['cohort_name'].str.endswith(' ')]
# remove names with double space or newlines
clean = clean[~clean['cohort_name'].str.contains('  ')]
clean = clean[~clean['cohort_name'].str.contains('\n')]
main_clean = clean[clean['cohort_name'].str.contains(
    '|'.join(main_keyworkds), case=False)]
key_clean = clean[clean['cohort_name'].str.contains(
    '|'.join(keywords), case=False)]

key_clean[['cohort_name']].to_csv(
    '../../data/train/clean_cohort_names.csv', index=False)
