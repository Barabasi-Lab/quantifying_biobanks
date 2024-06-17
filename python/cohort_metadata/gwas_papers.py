import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob

cohorts = pd.read_csv('../../data/expansion/cohorts.csv')
cohort_papers = pd.read_csv('../../data/expansion/cohort_papers.csv')

sns.set_theme(context='notebook', font_scale=1.2)
gwas_names = pd.read_csv('../../data/database/meta/pgs_all_metadata_cohorts.csv')
gwas_names.columns = ['biobank', 'NAME', 'OTHER NAMES']

papers = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)
gwas = pd.read_csv('../../data/database/meta/gwas-catalog-v1.0.3.1-studies-r2024-06-07.tsv', sep='\t')
pmid = pd.read_csv('../../data/database/meta/papers_pmid.csv')

gwas['year'] = gwas['DATE'].str[:4].astype(int)


# gwas = gwas[gwas['year'] < 2023]
# gwas = gwas[gwas['COHORT'].notna()]
# gwas = gwas[gwas['COHORT'].str.lower() != 'other']
# gwas = gwas[gwas['COHORT'].str.lower() != 'others']
# gwas = gwas[gwas['COHORT'] != 'NR']

gwas_ids = set(gwas['PUBMED ID'])

pmid_ids = set(pmid['pmid'])

inga = gwas_ids - pmid_ids
over = gwas_ids & pmid_ids
over_ids = pmid[pmid['pmid'].isin(over)]['id'].unique()

both = papers[papers['id'].isin(over_ids)]
cp = cohort_papers[cohort_papers['id'].isin(both['id'])]
gb = cp.groupby('cohort_name_lower').id.nunique().reset_index()
gb.columns = ['cohort_name_lower', 'in_gwas']
cohorts = cohorts.merge(gb, how='left')

inga = gwas[gwas['PUBMED ID'].isin(inga)].drop_duplicates(subset=['PUBMED ID'], keep='first')
inga['biobank'] = inga['COHORT'].str.split('|') 
gwas['biobank'] = gwas['COHORT'].str.split('|')
inga_cohorts = inga.explode('biobank').drop_duplicates(subset=['PUBMED ID', 'biobank'], keep='first')
gwas_cohorts = gwas.explode('biobank').drop_duplicates(subset=['PUBMED ID', 'biobank'], keep='first')
gwas_cohorts = gwas_cohorts.merge(gwas_names, left_on='biobank', right_on='biobank', how='left')
inga_cohorts = inga_cohorts.merge(gwas_names, left_on='biobank', right_on='biobank', how='left')
gwas_cohorts['NAME'] = gwas_cohorts['NAME'].str.lower()
inga_cohorts['NAME'] = inga_cohorts['NAME'].str.lower()

cohorts['NAME'] = cohorts['cohort_name_lower'].str[4:]

gwas_cohorts = gwas_cohorts.merge(cohorts[['NAME', 'cohort_name_lower']], left_on='NAME', right_on='NAME', how='left')
inga_cohorts = inga_cohorts.merge(cohorts[['NAME', 'cohort_name_lower']], left_on='NAME', right_on='NAME', how='left')

gb_gwas = gwas_cohorts.groupby('cohort_name_lower')['PUBMED ID'].nunique().rename('gwas_pubs').reset_index().sort_values('gwas_pubs', ascending=False)

gb_both = gb_gwas.merge(gb)
gb_both['better'] = gb_both['gwas_pubs'] < gb_both['in_gwas']
gb_both['diff'] = gb_both['in_gwas'] - gb_both['gwas_pubs']
gb_both['proportion_covered'] =  gb_both['in_gwas'] / gb_both['gwas_pubs']

missing_coverage = inga_cohorts.dropna(subset=['cohort_name_lower'])
missing_coverage = missing_coverage.groupby('cohort_name_lower')['PUBMED ID'].nunique().rename('missing_pubs').reset_index().sort_values('missing_pubs', ascending=False)
missing_coverage = missing_coverage.merge(gb_both, on='cohort_name_lower', how='left')
missing_coverage['proportion_missing'] = missing_coverage['missing_pubs'] / missing_coverage['gwas_pubs']

missing_coverage.to_csv('../../data/database/meta/coverage.csv', index=False)

# UK Biobank example
ukb_pmed = set(pmid[pmid['id'].isin(cp[cp['cohort_name_lower'] == 'the uk biobank']['id'])]['pmid'])
gwas_pmed = set(gwas_cohorts[gwas_cohorts['cohort_name_lower'] == 'the uk biobank']['PUBMED ID'])
ukb_gwas = gwas_cohorts[gwas_cohorts['PUBMED ID'].isin(ukb_pmed - gwas_pmed)]

