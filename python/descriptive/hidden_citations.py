import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="white", context="notebook", font_scale=1.2)

cohorts = pd.read_csv('../../data/expansion/cohorts.csv')
cohort_initials = pd.read_csv('../../data/expansion/cohort_initials.csv')
papers = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)

cohort_papers = pd.read_csv('../../data/expansion/cohort_papers.csv')
ref_papers = pd.read_csv('../../data/expansion/database/cohort_impact/reference_papers.csv')
cohorts = cohorts[cohorts['cohort_name_lower'].isin(ref_papers['cohort_name_lower'])]



cohort_years = ref_papers.groupby('cohort_name_lower').year.min().rename('ref_year').reset_index()
cohort_papers = cohort_papers.merge(cohort_years, on='cohort_name_lower', how='left')
cohort_papers = cohort_papers.merge(papers[['id', 'year']], on='id', how='left')
cohort_papers = cohort_papers[cohort_papers['year'] > cohort_papers['ref_year']]
cohort_mentions = cohort_papers.groupby('cohort_name_lower').id.nunique().rename('cohort_mentions').reset_index()

paper_citations = papers[papers['id'].isin(ref_papers['id'].unique())][['id', 'citations']]
paper_citations = paper_citations.explode('citations').dropna()
# rename id to reference_id
paper_citations = paper_citations.rename(columns={'id': 'reference_id'})
paper_citations['id'] = paper_citations['citations'].apply(lambda x: x['id'] if 'id' in x else np.nan)
paper_citations['cit_year'] = paper_citations['citations'].apply(lambda x: x['year'] if 'year' in x else np.nan)
# drop citations column
paper_citations = paper_citations.drop(columns='citations')
# rename id to reference_id in ref_papers
ref_papers = ref_papers.rename(columns={'id': 'reference_id'})
paper_citations = paper_citations.merge(ref_papers[['reference_id', 'cohort_name_lower']], on='reference_id', how='left')

proper = paper_citations.merge(cohort_papers[['id', 'cohort_name_lower']], on=['id', 'cohort_name_lower'])
cohort_proper = proper.groupby('cohort_name_lower').id.nunique().rename('proper_mentions').reset_index()
cohort_hidden = cohort_proper.merge(cohort_mentions, on='cohort_name_lower', how='left')
cohort_hidden['hidden_citations'] = cohort_hidden['cohort_mentions'] - cohort_hidden['proper_mentions']
cohort_hidden['hidden_per'] = cohort_hidden['hidden_citations'] / cohort_hidden['cohort_mentions'] * 100

half_cohorts = ref_papers[ref_papers['prop_inner_citations'] >= 0.2]['cohort_name_lower'].unique()
hidden = cohort_hidden[cohort_hidden['cohort_name_lower'].isin(half_cohorts)]
ref = ref_papers[ref_papers['cohort_name_lower'].isin(half_cohorts)]
ref_citations = ref.groupby('cohort_name_lower')['citations_count'].sum().reset_index()
cohort_data = cohorts[cohorts['cohort_name_lower'].isin(ref['cohort_name_lower'])][['cohort_name_lower', 'pubs']]
cohort_data = cohort_data.merge(ref_citations, on='cohort_name_lower', how='left')
cohort_data = cohort_data.merge(hidden, on='cohort_name_lower', how='left')

cohort_papers = cohort_papers.merge(papers[['id', 'citations_count']], on='id', how='left')
cohort_reach = papers[['id', 'citations']].explode('citations').dropna()
cohort_reach['cit_id'] = cohort_reach['citations'].apply(lambda x: x['id'] if 'id' in x else np.nan).dropna()
# drop citations column
cohort_reach = cohort_reach.drop(columns='citations')
cohort_reach = cohort_reach.merge(cohort_papers[['id', 'cohort_name_lower']], on='id', how='left')
cohort_reach = cohort_reach.groupby('cohort_name_lower').cit_id.nunique().rename('reach').reset_index()

cohort_data = cohort_data.merge(cohort_reach, on='cohort_name_lower', how='left')
cohort_data = cohort_data.dropna()
cohort_data['true_impact'] = cohort_data['citations_count'] + cohort_data['hidden_citations']
cohort_data['true_impact_per'] = cohort_data['hidden_citations'] / cohort_data['citations_count'] * 100
cohort_data['reach_per'] = (cohort_data['reach']) / cohort_data['citations_count']

ax = sns.kdeplot(data=cohort_data, x='hidden_per', fill=True, color='skyblue', label='Hidden Citations', cumulative=True)
sns.rugplot(data=cohort_data, x='hidden_per', color='blue', alpha=1, ax=ax)
ax.set_xlim(0, 100)

melt = cohort_data.melt(id_vars='cohort_name_lower', value_vars=['hidden_citations', 'cohort_mentions', 'citations_count', 'reach'], var_name='metric', value_name='count')
# rename metrics
melt['metric'] = melt['metric'].replace({'hidden_citations': 'Hidden Citations', 'cohort_mentions': 'Mentions', 'citations_count': 'Citations', 'reach': 'Scientific Reach'})

plt.figure(figsize=(10, 6))
ax = sns.boxplot(data=melt, y='metric', x='count', log_scale=True, hue='metric', width=.5, palette='Set2', whis=(10, 90), linewidth=1.5,
            showfliers=False)
sns.stripplot(data=melt, y='metric', x='count', log_scale=True, hue='metric', palette='Set2', alpha=.1, ax=ax, zorder=0)
ax.set_xlabel('Papers')
ax.set_ylabel('')
ax.set_title('Scientific Impact of Biobanks')
plt.tight_layout()
sns.despine()
plt.savefig('../../figures/local_impact/impact_boxplot.pdf')

ax = sns.scatterplot(data=cohort_data, x='hidden_per', y='cohort_mentions', alpha=0.5, color='skyblue')
ax.set_yscale('log')
#ax.set_xscale('log')
ax.set_xlabel('Hidden Citations')

biobanks = {
    'the uk biobank': 'UK Biobank',
    'the biobank japan': 'BioBank Japan',
    'the genotype-tissue expression project': 'GTEx',
    'the south west dementia brain bank': 'SWDBB',
    'the copenhagen aging and midlife biobank': 'CAMB',
    'the guangzhou biobank': 'Guangzhou Biobank',
    'the china kadoorie biobank': 'Kadoorie Biobank',
    'the generation r study': 'Generation R',
    'the million veteran program': 'MVP',
}

cohort_sel = cohort_data[cohort_data['cohort_name_lower'].isin(biobanks.keys())]
cohort_sel['biobank'] = cohort_sel['cohort_name_lower'].apply(lambda x: biobanks[x])
melt_sel = melt[melt['cohort_name_lower'].isin(biobanks.keys())]
melt_sel['biobank'] = melt_sel['cohort_name_lower'].apply(lambda x: biobanks[x])
order = cohort_sel.sort_values('hidden_per', ascending=False)['biobank'].to_list()

plt.figure(figsize=(10, 6))
ax = sns.pointplot(data=melt_sel, y='biobank', x='count', hue='metric', palette='Set2', dodge=False, join=False, order=order,
                   markers=['o', '^', 's', 'D'])
ax.set_xscale('log')
# set horizontal grid
ax.yaxis.grid(True)
# move legend
sns.move_legend(
    ax, "lower center",
    bbox_to_anchor=(0.5, 1), ncol=4, title=None, frameon=False,
)
ax.set_xlabel('Papers')
ax.set_ylabel('')
plt.tight_layout()
sns.despine()
plt.savefig('../../figures/local_impact/hidden_citations.pdf')
