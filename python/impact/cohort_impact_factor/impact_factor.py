import pandas as pd
import numpy as np

drop_cohorts = [
    'the multiple cohorts',
    'the summer food service program',
    'the clinical trials network',
    'the research biobank',
    'the complete health improvement program',
    'the census of population',
    'the school breakfast program',
    'the integrated research network',
    'the special supplemental nutrition program',
]
cohorts = pd.read_csv('../../../data/expansion/cohorts.csv')
original = pd.read_csv('../../../data/expansion/cohorts.csv')
papers = pd.read_json('../../../data/expansion/database/mentions/papers.json', lines=True)
grants = pd.read_json('../../../data/expansion/database/mentions/grants.json', lines=True)
patents = pd.read_json('../../../data/expansion/database/mentions/patents.json', lines=True)
clinical_trials = pd.read_json('../../../data/expansion/database/reach/clinical_trials.json', lines=True)
policies = pd.read_json('../../../data/expansion/database/mentions/policies.json', lines=True)

cohort_grants = pd.read_csv('../../../data/expansion/cohort_grants.csv')
cohort_papers = pd.read_csv('../../../data/expansion/cohort_papers.csv')
cohort_papers = cohort_papers.merge(papers[['id', 'citations_count', 'year']], on='id', how='left')
# first year by cohort
first_year = cohort_papers.groupby('cohort_name_lower').year.min().reset_index()

disease_impact = pd.read_csv('../../../data/expansion/database/cohort_impact/hrcs_impact.csv')
rcdc_impact = pd.read_csv('../../../data/expansion/database/cohort_impact/rcdc_impact.csv')
# divide each column by the number of papers in the cohort except cohort_name_lower in rcdc_impact
for col in rcdc_impact.columns:
    if col == 'cohort_name_lower' or col == 'papers':
        continue
    rcdc_impact[col] = rcdc_impact[col] / rcdc_impact['papers']

rcdc_impact.fillna(0, inplace=True)
# sum all columns except cohort_name_lower and papers
rcdc_impact['disease_impact'] = rcdc_impact.iloc[:, 2:].sum(axis=1)
# sort by disease_impact
rcdc_impact = rcdc_impact.sort_values('disease_impact', ascending=False)
# reset index
rcdc_impact = rcdc_impact.reset_index(drop=True)
age_groups = pd.read_csv('../../../data/expansion/database/cohort_data/age_groups.csv')

hidden_citations = pd.read_csv('../../../data/expansion/database/cohort_impact/hidden_citations.csv')
reference_papers = pd.read_csv('../../../data/expansion/database/cohort_impact/reference_papers.csv')



# rank the cohorts by the number of publications
original['original_rank'] = original['pubs'].rank(ascending=False)


drop_cols = ['title', 'abstract', 'acknowledgements', 'datasets']
cohorts = cohorts.drop(drop_cols, axis=1)

# normalize each column except cohort_name_lower between 0 and 1
for col in cohorts.columns:
    if col == 'cohort_name_lower':
        continue
    cohorts[col] = (cohorts[col] - cohorts[col].min()) / (cohorts[col].max() - cohorts[col].min())


# sum all columns except cohort_name_lower
cohorts['impact'] = cohorts.sum(axis=1)
cohorts = cohorts.sort_values('impact', ascending=False)
cohorts = cohorts.merge(first_year, on='cohort_name_lower', how='left')
# normalize the impact column by year - giving less weight to older cohorts
cohorts['impact_norm'] = (cohorts['impact'] - cohorts['impact'].mean()) / cohorts['impact'].std()
cohorts['impact_norm'] = cohorts['impact_norm'] / (2023 - cohorts['year'] + 1)
# sort by impact_norm
cohorts = cohorts.sort_values('impact_norm', ascending=False)
cohorts = cohorts.reset_index(drop=True)
# save to csv
cohorts.to_csv('../../../data/expansion/database/cohort_impact/target_impact.csv', index=False)