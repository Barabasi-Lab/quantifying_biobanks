import pandas as pd
from glob import glob

# read replace df
replace = pd.read_csv('../../data/expansion/replace_cohorts.csv')
rep = dict(zip(replace['cohort_name_lower'], replace['replace']))

dfct = pd.read_json('../../data/expansion/database/reach_raw/cohort_clinical_trial.json', lines=True)
dfct['cohort_name_lower'] = dfct['cohort_name_lower'].replace(rep)
dfct.to_json(f'../../data/expansion/database/reach/cohort_clinical_trial.json', orient='records', lines=True)

# same for cohort_grant
dfg = pd.read_json('../../data/expansion/database/reach_raw/cohort_grant.json', lines=True)
dfg['cohort_name_lower'] = dfg['cohort_name_lower'].replace(rep)
dfg.to_json(f'../../data/expansion/database/reach/cohort_grant.json', orient='records', lines=True)

# same for cohort_patent
dfp = pd.read_json('../../data/expansion/database/reach_raw/cohort_patent.json', lines=True)
dfp['cohort_name_lower'] = dfp['cohort_name_lower'].replace(rep)
dfp.to_json(f'../../data/expansion/database/reach/cohort_patent.json', orient='records', lines=True)

# same for cohort_policy
dfpol = pd.read_json('../../data/expansion/database/reach_raw/cohort_policy.json', lines=True)
dfpol['cohort_name_lower'] = dfpol['cohort_name_lower'].replace(rep)
dfpol.to_json(f'../../data/expansion/database/reach/cohort_policy.json', orient='records', lines=True)

df = pd.read_json('../../data/expansion/database/raw_foundational/papers.json', lines=True)
df['cohort_name_lower'] = df['cohort_name_lower'].replace(rep)
df.to_json('../../data/expansion/database/foundational/papers.json', orient='records', lines=True)

