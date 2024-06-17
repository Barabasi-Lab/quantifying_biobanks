import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="white", context="notebook", font_scale=1.2)

# read ../../reach/policies.json
pol = pd.read_json('../../data/expansion/database/reach/policies.json', lines=True)
pol = pol.explode('publisher_type')

cohort_pol = pd.read_json('../../data/expansion/database/reach/cohort_policy.json', lines=True)

cohort_pol = cohort_pol.merge(pol, on='id', how='left')
cohorts = cohort_pol.groupby('cohort_name_lower').id.nunique().rename('policies').sort_values(ascending=False).reset_index()
cohorts_country = cohort_pol.groupby(['cohort_name_lower']).country.nunique().rename('policy_countries').reset_index().sort_values('policy_countries', ascending=False)
cohorts_orgs = cohort_pol.groupby('cohort_name_lower').publisher_id.nunique().rename('policy_orgs').reset_index().sort_values('policy_orgs', ascending=False)

orgs = cohort_pol.groupby('publisher').id.nunique().rename('policies').sort_values(ascending=False).reset_index()

gov = pol[pol['publisher_type'] == 'Government']

gov_orgs = gov.groupby('publisher').id.nunique().rename('policies').sort_values(ascending=False).reset_index()

gov_cohorts = gov.merge(cohort_pol, on='id', how='left')
cohorts_gov = gov_cohorts.groupby('cohort_name_lower').id.nunique().rename('gov_policies').sort_values(ascending=False).reset_index()

# merge cohorts with cohorts_country, cohorts_orgs, cohorts_gov
cohorts = cohorts.merge(cohorts_country, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(cohorts_orgs, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(cohorts_gov, on='cohort_name_lower', how='left')

# save to ../../data/expansion/database/cohort_reach/policies.csv
cohorts.to_csv('../../data/expansion/database/cohort_reach/policies.csv', index=False)