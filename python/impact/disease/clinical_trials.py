import pandas as pd

# import clinical trials from expansions/database

ct_cohorts = pd.read_csv('../../../data/expansion/cohort_clinical_trials.csv')
ct = pd.read_json('../../../data/expansion/database/mentions/clinical_trials.json')
ct = ct.merge(ct_cohorts)
cohorts = ct.groupby('cohort_name_lower').id.nunique().rename('clinical_trials').sort_values(ascending=False).reset_index()

ct['study_type']
# get number of interventional clinical trials per cohort use study_type
study_types = ct.groupby('cohort_name_lower').study_type.value_counts().unstack().fillna(0).reset_index().sort_values('Interventional', ascending=False)

ct['drug'] = ct.interventions.apply(lambda x: x[0]['type'] if x else 'NA').apply(lambda x: 1 if x == 'Drug' else 0)
drugs = ct.groupby('cohort_name_lower').drug.sum().sort_values(ascending=False).reset_index()

rcdc = ct.explode('rcdc').fillna('NA')
rcdc['vaccine'] = rcdc.rcdc.apply(lambda x: True if 'vaccine' in x.lower() else False)
rcdc['minority_health'] = rcdc.rcdc.apply(lambda x: True if ('minority' in x.lower() or 'minorities' in x.lower()) else False)
rcdc['rare_disease'] = rcdc.rcdc.apply(lambda x: True if 'rare' in x.lower() else False)
rcdc['women_health'] = rcdc.rcdc.apply(lambda x: True if 'women' in x.lower() else False)
rcdc['social_determinants'] = rcdc.rcdc.apply(lambda x: True if ('social' in x.lower() or 'disparities' in x.lower()) else False)

rcdc.rcdc.value_counts().head(40)


social = rcdc[rcdc.social_determinants].groupby('cohort_name_lower').id.nunique().rename('social_determinants').sort_values(ascending=False).reset_index()
women_health = rcdc[rcdc['women_health']].groupby('cohort_name_lower').id.nunique().rename('women_health').sort_values(ascending=False).reset_index()
vaccines = rcdc[rcdc.vaccine].groupby('cohort_name_lower').id.nunique().rename('vaccines').sort_values(ascending=False).reset_index()
minority_health = rcdc[rcdc.minority_health].groupby('cohort_name_lower').id.nunique().rename('minority_health').sort_values(ascending=False).reset_index()
rare_disease = rcdc[rcdc.rare_disease].groupby('cohort_name_lower').id.nunique().rename('rare_disease').sort_values(ascending=False).reset_index()

# Merge the 5 dataframes to cohorts using left join
cohorts = cohorts.merge(study_types, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(drugs, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(social, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(women_health, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(vaccines, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(minority_health, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(rare_disease, on='cohort_name_lower', how='left')

# fillna 0
cohorts = cohorts.fillna(0)
cohorts.to_csv('../../../data/expansion/database/cohort_impact/clinical_trials_impact.csv', index=False)
