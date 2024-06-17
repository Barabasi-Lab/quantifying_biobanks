""""
Focus on grants to get training and education oriented data.
"""

import pandas as pd
import numpy as np

cohorts = pd.read_csv('../../../data/expansion/cohorts.csv')
grants = pd.read_json('../../../data/expansion/database/mentions/grants.json', lines=True)
cohort_grants = pd.read_csv('../../../data/expansion/cohort_grants.csv')
# read grid json from meta dir
grid = pd.read_json('../../../data/database/meta/grid.json', lines=True)
# add _org to each column except the first one
grid.columns = 'org_' + grid.columns
# rename org_id to funder_org
grid.rename(columns={'org_id': 'funder_org'}, inplace=True)
grid_cols = ['funder_org', 'org_name', 'funder']
# remove empty lists from org_acronyms
grid['org_acronyms'] = grid['org_acronyms'].apply(lambda x: x if x else np.nan)
# get first acronym as funder if not np.nan
grid['funder'] = grid['org_acronyms'].apply(lambda x: x[0] if type(x) == list else np.nan)
# merge grid to grants to get funder name
grants = grants.merge(grid[grid_cols], on='funder_org', how='left')
# replace grant_id with id
grants.rename(columns={'grant_id': 'id'}, inplace=True)
# read nih_activity_codes from meta dir csv
nih = pd.read_csv('../../../data/database/meta/nih_activity_codes.csv')
nih.columns = nih.columns.str.lower()
train_grants = nih[nih['description'].str.contains('training|education', case=False)]['code'].values
# collaboration or intramural
collaboration_grants = nih[nih['description'].str.contains('collaboration|intramural', case=False)]['code'].values
# prestigous grants if have 'highly' in description
prestigious_grants = nih[nih['description'].str.contains('highly|promising', case=False)]['code'].values

# merge left to get grants per cohort
cohort_grants = cohort_grants.merge(grants, on='id', how='left')

cohort_grants['funder_country'] = cohort_grants['funder_org_countries'].apply(lambda x: x[0] if x is not np.nan and len(x) > 0 else np.nan)

cohort_grants['activity_code'].fillna('-1', inplace=True)
# flag grant as training if it starts with 'S', 'T', 'F', 'K', or 'D' or 'R25'
cohort_grants['training'] = cohort_grants['activity_code'].apply(lambda x: True if x[0] in ['T', 'F', 'K', 'D'] or x == 'R25' else False)
# flag grant as training if it is in train_grants
cohort_grants['training'] = cohort_grants['training'] | cohort_grants['activity_code'].isin(train_grants)
# flag grant as collaboration if it starts with 'U'
cohort_grants['collaboration'] = cohort_grants['activity_code'].apply(lambda x: True if x[0] == 'U' else False)
# flag grant as collaboration if it is in collaboration_grants
cohort_grants['collaboration'] = cohort_grants['collaboration'] | cohort_grants['activity_code'].isin(collaboration_grants)
# flag as prestigious if starts with 'DP' or equal to 'R01'
cohort_grants['prestigious'] = cohort_grants['activity_code'].apply(lambda x: True if x[:2] == 'DP' or x == 'R01' else False)
# flag as prestigious if it is in prestigious_grants
cohort_grants['prestigious'] = cohort_grants['prestigious'] | cohort_grants['activity_code'].isin(prestigious_grants)

# count training grants per cohort
cohort_training = cohort_grants.groupby('cohort_name_lower').agg(training_grants=('training', 'sum')).reset_index().sort_values('training_grants', ascending=False)
cohort_collaboration = cohort_grants.groupby('cohort_name_lower').agg(collaboration_grants=('collaboration', 'sum')).reset_index().sort_values('collaboration_grants', ascending=False)
cohort_prestigious = cohort_grants.groupby('cohort_name_lower').agg(prestigious_grants=('prestigious', 'sum')).reset_index().sort_values('prestigious_grants', ascending=False)

# for cohort grants groupby cohort_name_lower and agg:
# unique id
# unique funder_org
# unique funder_country
# total funding_usd
# mean funding_usd, convert to int
# total training_grants
# total collaboration_grants
# total prestigious_grants
# unique activity_codes

cohort_grants_data = cohort_grants.groupby('cohort_name_lower').agg(
    grants=('id', 'nunique'),
    funders=('funder_org', 'nunique'),
    funder_countries=('funder_country', 'nunique'),
    total_funding=('funding_usd', 'sum'),
    mean_funding=('funding_usd', 'mean'),
    std_funding=('funding_usd', 'std'),
    median_funding=('funding_usd', 'median'),
    training_grants=('training', 'sum'),
    collaboration_grants=('collaboration', 'sum'),
    prestigious_grants=('prestigious', 'sum'),
    nih_activity_codes=('activity_code', 'nunique')
).reset_index().sort_values('grants', ascending=False)
# round mean_funding to 0 decimal
cohort_grants_data['mean_funding'] = cohort_grants_data['mean_funding'].apply(lambda x: round(x, 0))
cohort_grants_data['std_funding'] = cohort_grants_data['std_funding'].apply(lambda x: round(x, 0))

# save in data/database/cohort_impact/
cohort_grants_data.to_csv('../../../data/expansion/database/cohort_impact/grants.csv', index=False)
