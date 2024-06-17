import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

grid = pd.read_json('../../data/database/meta/grid.json', lines=True)

grants = pd.read_json('../../data/expansion/database/mentions/grants.json', lines=True)
policy = pd.read_json('../../data/expansion/database/mentions/policies.json', lines=True)
pubs = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)
patents = pd.read_json('../../data/expansion/database/mentions/patents.json', lines=True)
clinical_trials = pd.read_json('../../data/expansion/database/mentions/clinical_trials.json')
indirect_ct = pd.read_csv('../../data/expansion/database/indirect_impact/clinical_trials.csv')

cohort_papers = pd.read_csv('../../data/expansion/cohort_papers.csv')
cohort_grants = pd.read_csv('../../data/expansion/cohort_grants.csv')
cohort_patents = pd.read_csv('../../data/expansion/cohort_patents.csv')
cohort_clinical_trials = pd.read_csv('../../data/expansion/cohort_clinical_trials.csv')
cohort_policy = pd.read_csv('../../data/expansion/cohort_policy.csv')

pubs = pubs[pubs['id'].isin(cohort_papers['id'])]
grants = grants[grants['id'].isin(cohort_grants['id'])]
patents = patents[patents['id'].isin(cohort_patents['id'])]
clinical_trials = clinical_trials[clinical_trials['id'].isin(cohort_clinical_trials['id'])]
policy = policy[policy['id'].isin(cohort_policy['id'])]

print('Papers:', pubs.id.nunique())
print('Grants:', grants.id.nunique())
print('Patents:', patents.id.nunique())
print('Clinical Trials:', clinical_trials.id.nunique())
print('Policy:', policy.id.nunique())

# get the total number of unique ids for all categories
total = pubs.id.nunique() + grants.id.nunique() + patents.id.nunique() + clinical_trials.id.nunique() + policy.id.nunique()
print('Total:', total)

# Research impact
pubs_grants = grants['resulting_publication_ids'].explode().dropna().nunique()
pubs_trials = indirect_ct['citing_publication_ids'].explode().dropna().nunique()
pubs_trials2 = indirect_ct['resulting_publication_ids'].explode().dropna().nunique()
print('Citations:', pubs['citations_count'].sum())
print('Papers from Grants:', pubs_grants)
print('Papers from Trials:', pubs_trials + pubs_trials2)
print('Grant USD:', f"{grants['funding_usd'].sum() / 1e9:.1f}B")
print('Grant USD median:', f"{grants['funding_usd'].median() / 1e6:.1f}M")
print('Grant USD STD:', f"{grants['funding_usd'].std() / 1e6:.1f}M")

# Research capacity
def is_training(code):
    # if nan return False
    if code is np.nan:
        return False    
    if code in train_grants:
        return True
    if code[0] in ['T', 'F', 'K', 'D']:
        return True
    return False

def is_collaboration(code):
    # if nan return False
    if code is np.nan:
        return False
    if code in collaboration_grants:
        return True
    if code[0] == 'U':
        return True
    return False

def is_presitigious(code):
    # if nan return False
    if not code:
        return False
    if code in prestigious_grants:
        return True
    return False

INFRASTRUCTURE = 'D000096102'
CAPACITY = 'D057191'
nih = pd.read_csv('../../data/database/meta/nih_activity_codes.csv')
nih.columns = nih.columns.str.lower()
train_grants = nih[nih['description'].str.contains('training|education', case=False)]['code'].values
# collaboration or intramural
collaboration_grants = nih[nih['description'].str.contains('collaboration|intramural', case=False)]['code'].values
# prestigous grants if have 'highly' in description
prestigious_grants = nih[nih['description'].str.contains('highly|promising', case=False)]['code'].values
grants['training'] = grants['activity_code'].apply(is_training)
grants['collaboration'] = grants['activity_code'].apply(is_collaboration)
grants['prestigious'] = grants['activity_code'].apply(is_presitigious)
pubs_mesh = pubs.explode('mesh_ids').dropna(subset=['mesh_ids'])[['id', 'mesh_ids']]
pubs_mesh['infrastucture'] = pubs_mesh['mesh_ids'].apply(lambda x: INFRASTRUCTURE == x)
pubs_mesh['capacity'] = pubs_mesh['mesh_ids'].apply(lambda x: CAPACITY == x)
# save grants as json to data/figures
grants.to_json('../../data/figures/grants.json', orient='records', lines=True)

# Therapeutic innovation
def has_vaccine(codes):
    for code in codes:
        if 'vaccine' in code.lower():
            return True
    return False



clinical_trials['intervention_types'] = clinical_trials['interventions'].apply(lambda x: [i['type'] for i in x if 'type' in i])
clinical_trials[clinical_trials['study_type']=='Interventional']['intervention_types'].explode().value_counts().head(20)
clinical_trials[clinical_trials['study_type']=='Interventional'].explode('intervention_types').groupby(['intervention_types']).id.nunique().sort_values(ascending=False)
clinical_trials['vaccine'] = clinical_trials['rcdc'].apply(has_vaccine)
patents['vaccine'] = patents['rcdc'].apply(has_vaccine)
# save clinical_trials as json to data/figures
clinical_trials.to_json('../../data/figures/clinical_trials.json', orient='records', lines=True)

# Partnerships
def get_parent(org, org2parent):
    parent = org2parent.get(org)
    while parent in org2parent:
        parent = org2parent[parent]
    return parent

def is_sponsor(orgs):
    sponsors = []
    for org in orgs:
        if 'grid_id' in org:
            sponsors.append(org['grid_id'])
    return np.nan if len(sponsors) == 0 else sponsors

def is_company(orgs):
    if 'Company' in orgs:
        return True
    return False

grid.rename(columns={'id': 'research_org'}, inplace=True)
# Vanderbilt Health is actually a healthcare provider
grid.loc[grid['research_org'] == 'grid.490555.8', 'types'] = ['Healthcare']
parents = grid.explode('parent_ids').dropna(subset=['parent_ids'])
org2parent = dict(zip(parents['research_org'], parents['parent_ids']))
org2root = dict()
for org in tqdm(org2parent):
    org2root[org] = get_parent(org, org2parent)
roots = grid[grid['parent_ids'].apply(lambda x: len(x) == 0)]
root2root = dict(zip(roots['research_org'], roots['research_org']))
# update org2root to have root2root
for root in root2root:
    org2root[root] = root
root2name = dict(zip(roots['research_org'], roots['name']))
root2types = dict(zip(roots['research_org'], roots['types']))
root2country = dict(zip(roots['research_org'], roots['country']))
org2name = dict()
org2types = dict()
org2country = dict()
for org in org2root:
    org2name[org] = root2name[org2root[org]]
    org2types[org] = root2types[org2root[org]]
    org2country[org] = root2country[org2root[org]]
    

# Publications
paper_orgs = pubs.explode('research_orgs').dropna(subset=['research_orgs'])[['id', 'research_orgs']]
# rename research_orgs to research_org
paper_orgs.rename(columns={'research_orgs': 'research_org'}, inplace=True)
paper_orgs['name'] = paper_orgs['research_org'].apply(lambda x: org2name.get(x))
paper_orgs['types'] = paper_orgs['research_org'].apply(lambda x: org2types.get(x))
paper_orgs['country'] = paper_orgs['research_org'].apply(lambda x: org2country.get(x))
paper_orgs['is_company'] = paper_orgs['types'].apply(is_company)
paper_orgs['is_gov'] = paper_orgs['types'].apply(lambda x: 'Government' in x if x else False)
paper_orgs['is_healthcare'] = paper_orgs['types'].apply(lambda x: 'Healthcare' in x if x else False)
paper_orgs['is_nonprofit'] = paper_orgs['types'].apply(lambda x: 'Nonprofit' in x if x else False)
paper_orgs['is_edu'] = paper_orgs['types'].apply(lambda x: 'Education' in x if x else False)
paper_orgs['is_facility'] = paper_orgs['types'].apply(lambda x: 'Facility' in x if x else False)
# Patents
patent_orgs = patents.explode('assignee_orgs').dropna(subset=['assignee_orgs'])[['id', 'assignee_orgs']]
patent_orgs.rename(columns={'assignee_orgs': 'research_org'}, inplace=True)
patent_orgs['name'] = patent_orgs['research_org'].apply(lambda x: org2name.get(x))
patent_orgs['types'] = patent_orgs['research_org'].apply(lambda x: org2types.get(x))
patent_orgs['country'] = patent_orgs['research_org'].apply(lambda x: org2country.get(x))
patent_orgs['is_company'] = patent_orgs['types'].apply(is_company)
patent_orgs['is_gov'] = patent_orgs['types'].apply(lambda x: 'Government' in x if x else False)
patent_orgs['is_healthcare'] = patent_orgs['types'].apply(lambda x: 'Healthcare' in x if x else False)
patent_orgs['is_nonprofit'] = patent_orgs['types'].apply(lambda x: 'Nonprofit' in x if x else False)
patent_orgs['is_edu'] = patent_orgs['types'].apply(lambda x: 'Education' in x if x else False)
patent_orgs['is_facility'] = patent_orgs['types'].apply(lambda x: 'Facility' in x if x else False)
# Clinical Trials
clinical_trials['research_org'] = clinical_trials['organisation_details'].apply(is_sponsor)
trial_orgs = clinical_trials.explode('research_org').dropna(subset=['research_org'])[['id', 'research_org']]
trial_orgs['name'] = trial_orgs['research_org'].apply(lambda x: org2name.get(x))
trial_orgs['types'] = trial_orgs['research_org'].apply(lambda x: org2types.get(x))
trial_orgs['country'] = trial_orgs['research_org'].apply(lambda x: org2country.get(x))
trial_country = trial_orgs['research_org'].apply(lambda x: org2country.get(x))
trial_orgs['is_company'] = trial_orgs['types'].apply(is_company)
trial_orgs['is_gov'] = trial_orgs['types'].apply(lambda x: 'Government' in x if x else False)
trial_orgs['is_healthcare'] = trial_orgs['types'].apply(lambda x: 'Healthcare' in x if x else False)
trial_orgs['is_nonprofit'] = trial_orgs['types'].apply(lambda x: 'Nonprofit' in x if x else False)
trial_orgs['is_edu'] = trial_orgs['types'].apply(lambda x: 'Education' in x if x else False)
trial_orgs['is_facility'] = trial_orgs['types'].apply(lambda x: 'Facility' in x if x else False)
# Grants
grant_orgs = grants[['id', 'funder_org']].dropna()
grant_orgs.rename(columns={'funder_org': 'research_org'}, inplace=True)
grant_orgs['name'] = grant_orgs['research_org'].apply(lambda x: org2name.get(x))
grant_orgs['types'] = grant_orgs['research_org'].apply(lambda x: org2types.get(x))
grant_orgs['country'] = grant_orgs['research_org'].apply(lambda x: org2country.get(x))
grant_orgs = grant_orgs.dropna()
grant_orgs['is_company'] = grant_orgs['types'].apply(is_company)
grant_orgs['is_gov'] = grant_orgs['types'].apply(lambda x: 'Government' in x if x else False)
grant_orgs['is_healthcare'] = grant_orgs['types'].apply(lambda x: 'Healthcare' in x if x else False)
grant_orgs['is_nonprofit'] = grant_orgs['types'].apply(lambda x: 'Nonprofit' in x if x else False)
grant_orgs['is_edu'] = grant_orgs['types'].apply(lambda x: 'Education' in x if x else False)
grant_orgs['is_facility'] = grant_orgs['types'].apply(lambda x: 'Facility' in x if x else False)
# Policy
policy_orgs = policy[['id', 'publisher_id']].dropna()
policy_orgs.rename(columns={'publisher_id': 'research_org'}, inplace=True)
policy_orgs['name'] = policy_orgs['research_org'].apply(lambda x: org2name.get(x))
policy_orgs['types'] = policy_orgs['research_org'].apply(lambda x: org2types.get(x))
policy_orgs['country'] = policy_orgs['research_org'].apply(lambda x: org2country.get(x))

paper_orgs['source'] = 'Papers'
patent_orgs['source'] = 'Patents'
trial_orgs['source'] = 'Clinical Trials'
grant_orgs['source'] = 'Grants'
policy_orgs['source'] = 'Policy'

# Companies
paper_company = paper_orgs[paper_orgs['is_company']]
grant_company = grant_orgs[grant_orgs['is_company']]
patent_company = patent_orgs[patent_orgs['is_company']]
trial_company = trial_orgs[trial_orgs['is_company']]
print(f'Company Papers (Ratio): {paper_company.id.nunique()} ({paper_company.id.nunique()/pubs.id.nunique()*100:.1f}%)')
print(f'Company Patents (Ratio): {patent_company.id.nunique()} ({patent_company.id.nunique()/patents.id.nunique()*100:.1f}%)')
print(f'Company Clinical Trials (Ratio): {trial_company.id.nunique()} ({trial_company.id.nunique()/clinical_trials.id.nunique()*100:.1f}%)')
print(f'Company Grants (Ratio): {grant_company.id.nunique()} ({grant_company.id.nunique()/grants.id.nunique()*100:.1f}%)')



all_partners = pd.concat([paper_orgs, patent_orgs, trial_orgs, grant_orgs, policy_orgs])
# save all_partners as json to data/figures
all_partners.to_json('../../data/figures/all_partners.json', orient='records', lines=True)
innovation_partners = pd.concat([patent_orgs, trial_orgs])
# save innovation_partners as json to data/figures
innovation_partners.to_json('../../data/figures/innovation_partners.json', orient='records', lines=True)
all_company = pd.concat([paper_company, patent_company, trial_company])
all_edu = pd.concat([trial_orgs[trial_orgs['is_edu']], patent_orgs[patent_orgs['is_edu']]])
all_healthcare = pd.concat([paper_orgs[paper_orgs['is_healthcare']], trial_orgs[trial_orgs['is_healthcare']], patent_orgs[patent_orgs['is_healthcare']]])
(all_company.groupby(['name']).id.nunique().sort_values(ascending=False).head(10) / all_company.id.nunique() * 100).cumsum()
top6 = (all_company.groupby(['name']).id.nunique().sort_values(ascending=False).head(6) / all_company.id.nunique() * 100).index
all_company[all_company['name'].isin(top6)].groupby(['name']).id.nunique().sort_values(ascending=False).sum()
paper_company[paper_company['name'].isin(top6)].groupby(['name']).id.nunique().sort_values(ascending=False).sum()
trial_company[trial_company['name'].isin(top6)].groupby(['name']).id.nunique().sort_values(ascending=False).sum()
patent_company[patent_company['name'].isin(top6)].groupby(['name']).id.nunique().sort_values(ascending=False).sum()

(all_partners.explode('name').groupby('name').id.nunique() / all_partners.id.nunique() * 100).sort_values(ascending=False).head(20)
(all_edu.groupby('name').id.nunique() / all_edu.id.nunique() * 100).sort_values(ascending=False).head(10)
(all_healthcare.groupby('name').id.nunique() / all_healthcare.id.nunique() * 100).sort_values(ascending=False).head(10)

(grant_orgs[grant_orgs['is_nonprofit']].groupby('name').id.nunique() / grant_orgs[grant_orgs['is_nonprofit']].id.nunique() * 100).sort_values(ascending=False).head(10)

# Public Health
pubs['bra'].explode().value_counts(normalize=True)
pubs_bra = pubs[['id', 'bra']].explode('bra')
# save pubs_bra as json to data/figures
pubs_bra.to_json('../../data/figures/pubs_bra.json', orient='records', lines=True)

def is_social(codes):
    for code in codes:
        if 'social' in code.lower():
            return True
    return False

def is_prevention(codes):
    for code in codes:
        if 'prevention' in code.lower():
            return True
    return False

def is_clinical(codes):
    for code in codes:
        if 'clinical' in code.lower():
            return True
    return False

def is_substance(codes):
    substances = ['Alcoholism, Alcohol Use and Health', 'Substance Misuse', 'Tobacco',
                  'Tobacco Smoke and Health', 'Prescription Drug Misuse',
                  'Screening and Brief Intervention for Substance Misuse',
                  'Substance Misuse Prevention', 'Cocaine', 'Fetal Alcohol Spectrum Disorders (FASD)',
                  ]
    for code in codes:
        for substance in substances:
            if substance.lower() in code.lower():
                return True
    return False

policy_orgs = policy_orgs.explode('types')
policy = policy.explode('bra')
policy['social'] = policy['rcdc'].apply(is_social)
policy['prevention'] = policy['rcdc'].apply(is_prevention)
policy['clinical'] = policy['rcdc'].apply(is_clinical)
policy['substance'] = policy['rcdc'].apply(is_substance)
policy = policy.explode('publisher_type')
policy['three'] = policy['social'].astype(int) + policy['prevention'].astype(int) + policy['clinical'].astype(int)
policy['four'] = policy['three'].astype(int) + policy['substance'].astype(int)

policy.explode('rcdc').groupby('rcdc').id.nunique().sort_values(ascending=False).head(40)
policy.explode('bra').groupby('bra').id.nunique().sort_values(ascending=False).head(40)
policy[policy['social']].publisher.value_counts().head(10)
policy[policy['social']].explode('rcdc').groupby('rcdc').id.nunique().sort_values(ascending=False).head(10)
policy_orgs.name.value_counts().head(10)
policy[policy['clinical']].publisher.value_counts().head(10)
policy.groupby('publisher_type')[['social', 'prevention', 'clinical', 'substance']].sum()
# save policy as json to data/figures
policy.to_json('../../data/figures/policy.json', orient='records', lines=True)