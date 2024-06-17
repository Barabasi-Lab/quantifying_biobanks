import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cohorts = pd.read_csv('../../../data/expansion/cohorts.csv')
impact_factor = pd.read_csv('../../../data/expansion/database/cohort_impact/target_impact.csv')
# only keep cohort_name_lower and impact_norm
impact_factor = impact_factor[['cohort_name_lower', 'impact_norm']]
disease_impact = pd.read_csv('../../../data/expansion/database/cohort_impact/disease_target_impact.csv')
disease_impact = disease_impact[['cohort_name_lower', 'impact']]


impact = cohorts[cohorts['pubs'] >= 20][['cohort_name_lower']]
impact = impact.merge(impact_factor, on='cohort_name_lower', how='left')
impact = impact.merge(disease_impact, on='cohort_name_lower', how='left')
impact['target'] = 0.9 * impact['impact_norm'] + 0.1 * impact['impact']
# sort by impact
impact = impact.sort_values('target', ascending=False)
impact = impact.dropna()

impact.columns = ['cohort_name_lower', 'impact', 'disease', 'target']
# plot kde of target
impact['outlier'] = impact['target'] > impact['target'].mean() + (impact['target'].quantile(0.75) - impact['target'].quantile(0.25))
impact.to_csv('../../../data/expansion/database/cohort_impact/target.csv', index=False)

mesh_impact = pd.read_csv('../../../data/expansion/database/cohort_impact/mesh_impact.csv')
cohort_mesh = mesh_impact.drop_duplicates(subset=['cohort_name_lower', 'mesh_name']).groupby(['cohort_name_lower', 'main_mesh_name']).papers.sum().reset_index()
cohort_mesh = cohort_mesh.sort_values('papers', ascending=False)
cohort_mesh = cohort_mesh.drop_duplicates(subset='cohort_name_lower')
cohort_mesh = cohort_mesh[['cohort_name_lower', 'main_mesh_name']].merge(impact, on='cohort_name_lower', how='left')
