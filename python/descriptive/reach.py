import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import circlify

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

trials = pd.read_json('../../data/expansion/database/reach/clinical_trials.json', lines=True)
grants = pd.read_json('../../data/expansion/database/reach/grants.json', lines=True)
policy = pd.read_json('../../data/expansion/database/reach/policies.json', lines=True)
patents = pd.read_json('../../data/expansion/database/reach/patents.json', lines=True)
papers = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)

cohorts = pd.read_csv('../../data/expansion/cohorts.csv')

cohort_papers = pd.read_csv('../../data/expansion/cohort_papers.csv')
cohort_papers = cohort_papers.merge(papers[['id', 'citations_count']], on='id', how='left')
cohort_trials = pd.read_json('../../data/expansion/database/reach/cohort_clinical_trial.json', lines=True)
cohort_grants = pd.read_json('../../data/expansion/database/reach/cohort_grant.json', lines=True)
cohort_patents = pd.read_json('../../data/expansion/database/reach/cohort_patent.json', lines=True)
cohort_policy = pd.read_json('../../data/expansion/database/reach/cohort_policy.json', lines=True)

replace = pd.read_csv('../../data/expansion/replace_cohorts.csv')
replace = dict(zip(replace['cohort_name_lower'], replace['replace']))
# replace cohort names
cohort_trials['cohort_name_lower'] = cohort_trials['cohort_name_lower'].replace(replace)
cohort_grants['cohort_name_lower'] = cohort_grants['cohort_name_lower'].replace(replace)
cohort_patents['cohort_name_lower'] = cohort_patents['cohort_name_lower'].replace(replace)
cohort_policy['cohort_name_lower'] = cohort_policy['cohort_name_lower'].replace(replace)


# count the number of unique ids in each cohort
reach = cohort_grants.groupby('cohort_name_lower').id.nunique().rename('grants').reset_index()
reach = reach.merge(cohort_trials.groupby('cohort_name_lower').id.nunique().rename('trials').reset_index(), on='cohort_name_lower', how='left')
reach = reach.merge(cohort_patents.groupby('cohort_name_lower').id.nunique().rename('patents').reset_index(), on='cohort_name_lower', how='left')
reach = reach.merge(cohort_policy.groupby('cohort_name_lower').id.nunique().rename('policies').reset_index(), on='cohort_name_lower', how='left')
reach.select_dtypes('float').corr()
reach = cohorts[['cohort_name_lower', 'pubs']].merge(reach, how='left')
reach = reach.merge(cohort_papers.groupby('cohort_name_lower').citations_count.sum().rename('papers').reset_index())

reach = reach.fillna(0)



uk_biobank = {
    'grants': 423,
    'trials': 14,
    'policy': 28,
    'patents': 172,
    'reach_grants': 9000,
    'reach_trials': 378,
    'reach_policy': 269,
    'reach_patents': 231,
}



data_uk = [
    {'id': 'Impact', 'datum': 10515, 'children': [
        {'id': 'Grants', 'datum': uk_biobank['grants'] + uk_biobank['reach_grants'],
         'children': [
             {'id': 'Mentions', 'datum': uk_biobank['grants']},
                {'id': 'Reach', 'datum': uk_biobank['reach_grants']}]},
        {'id': 'Trials', 'datum': uk_biobank['trials'] + uk_biobank['reach_trials'],
            'children': [
                {'id': 'Mentions', 'datum': uk_biobank['trials']},
                    {'id': 'Reach', 'datum': uk_biobank['reach_trials']}]},
        {'id': 'Policy', 'datum': uk_biobank['policy'] + uk_biobank['reach_policy'],
            'children': [
                {'id': 'Mentions', 'datum': uk_biobank['policy']},
                    {'id': 'Reach', 'datum': uk_biobank['reach_policy']}]},
        {'id': 'Patents', 'datum': uk_biobank['patents'] + uk_biobank['reach_patents'],
            'children': [
                {'id': 'Mentions', 'datum': uk_biobank['patents']},
                    {'id': 'Reach', 'datum': uk_biobank['reach_patents']}]}
    ]}
]
circles = circlify.circlify(
    data_uk,
    show_enclosure=False,
    target_enclosure=circlify.Circle(x=0, y=0, r=1)
)

# Create just a figure and only one subplot
fig, ax = plt.subplots(figsize=(14, 14))

# Title

# Remove axes
ax.axis('off')

# Find axis boundaries
lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r,
    )
    for circle in circles
)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

# Print circle the highest level (continents):
for circle in circles:
    if circle.level != 2:
        continue
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r, alpha=0.5,
                 linewidth=2, color="lightblue"))

# Print circle and labels for the highest level:
for circle in circles:
    if circle.level != 3:
        continue
    x, y, r = circle
    label_ = circle.ex["id"]
    label = circle.ex['datum']
    if label_ == 'Mentions':
        ax.add_patch(plt.Circle((x, y), r, alpha=0.5,
                    linewidth=2, color="C1"))
        plt.annotate(label, (x, y), ha='center', color="white")
    else:
        ax.add_patch(plt.Circle((x, y), r, alpha=0.5,
                    linewidth=2, color="C0"))
        plt.annotate(label, (x, y), ha='center', color="white")


# save as pdf
fig.savefig('../../figures/mentions+reach/uk_biobank.pdf')


# rename clinical_trials to trials
cohorts = cohorts.rename(columns={'clinical_trials': 'trials'})
# rename policy to policies
cohorts = cohorts.rename(columns={'policy': 'policies'})

vars = ['patents', 'policies', 'trials', 'grants']
increase = dict()
for var in vars:
    val = (reach[var] / cohorts[var])
    val.loc[(~np.isfinite(val)) & val.notnull()] = np.nan
    increase[var] = val.mean()


# melt the data in reach with id cohort_name_lower
reach_melt = reach.drop(['papers', 'pubs'], axis=1).melt(id_vars='cohort_name_lower', var_name='impact', value_name='count')
cohorts_melt = cohorts[vars + ['cohort_name_lower']].melt(id_vars='cohort_name_lower', var_name='impact', value_name='count')
reach_melt['source'] = 'Reach'
cohorts_melt['source'] = 'Mentions'
melt = pd.concat([reach_melt, cohorts_melt])

melt_sum = melt.groupby(['impact', 'source'])['count'].sum().reset_index()
ax = sns.barplot(data=melt_sum, y='impact', x='count', hue='source', linewidth=0.7, edgecolor='.2',
                 hue_order=['Reach', 'Mentions'])
ax.set_xscale('log')
ax.set_ylabel('Impact')
ax.set_xlabel('Number of Documents')
# save as pdf
plt.tight_layout()
plt.savefig('../../figures/mentions+reach/impact_all.pdf')