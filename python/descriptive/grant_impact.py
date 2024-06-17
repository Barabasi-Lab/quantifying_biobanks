import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

grid = pd.read_json('../../data/database/meta/grid.json', lines=True)
# rename id to funder_org
grid.rename(columns={'id': 'funder_org'}, inplace=True)

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

cohort_grants = pd.read_csv('../../data/expansion/cohort_grants.csv')
grants = pd.read_json('../../data/expansion/database/mentions/grants.json', lines=True)
grants = grants[grants.id.isin(cohort_grants.id.unique())]
grants = grants.merge(grid[['funder_org', 'name', 'country']], on='funder_org', how='left')
grants = grants.explode('bra')
grants = grants.explode('hrcs_hc')

grant_impact = pd.read_csv('../../data/expansion/database/cohort_impact/grants.csv')
funders = grants.groupby('name').agg({'funding_usd': 'sum', 'id': 'nunique'}).sort_values('funding_usd', ascending=False).reset_index()
funders.columns = ['funder', 'total_funding', 'grants']
countries = grants.groupby('country').agg({'funding_usd': 'sum', 'id': 'nunique'}).sort_values('funding_usd', ascending=False).reset_index()
countries.columns = ['country', 'total_funding', 'grants']

top_funders_usd = funders.head(10)
top_funders_num = funders.sort_values('grants', ascending=False).head(10)
top_countries_usd = countries.head(10)
top_countries_num = countries.sort_values('grants', ascending=False).head(10)

grant_impact['biobank'] = grant_impact['cohort_name_lower'].apply(lambda x: ' '.join(x.split()[1:]))
top_biobanks_usd = grant_impact.sort_values('total_funding', ascending=False).head(10)
top_biobanks_num = grant_impact.sort_values('grants', ascending=False).head(10)

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.boxplot(
    data=grant_impact,
    y='total_funding',
    log_scale=True,
    palette='coolwarm',  # Use a thematic color palette
)
ax.set_ylabel('Total Funding (USD)')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.boxplot(
    data=grant_impact,
    y='mean_funding',
    log_scale=True,
    palette='coolwarm',  # Use a thematic color palette
)
ax.set_ylabel('Mean Grant Funding (USD)')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.boxplot(
    data=grant_impact,
    y='grants',
    log_scale=True,
    palette='coolwarm',  # Use a thematic color palette
)
ax.set_ylabel('Grants')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.boxplot(
    data=grant_impact,
    y='training_grants',
    log_scale=False,
    palette='coolwarm',  # Use a thematic color palette
)
ax.set_ylabel('Grants')

grid = grid.explode('acronyms')
top_funders_num = top_funders_num.merge(grid[['name', 'acronyms']], left_on='funder', right_on='name', how='left')
top_funders_num = top_funders_num.drop_duplicates(subset='funder')
plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_funders_num,
    x='grants',
    y='acronyms',
    palette='Oranges_r',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
ax.set_ylabel('')
ax.set_xlabel('Number of Grants')
ax.set_title('Top 10 Funders by Number of Grants')
plt.tight_layout()
plt.savefig('../../figures/grant_impact/top_funders_num.pdf')

top_funders_usd['millions'] = top_funders_usd['total_funding'] / 1_000_000
top_funders_usd = top_funders_usd.merge(grid[['name', 'acronyms']], left_on='funder', right_on='name', how='left')
top_funders_usd = top_funders_usd.drop_duplicates(subset='funder')
plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_funders_usd,
    x='millions',
    y='acronyms',
    palette= 'Oranges_r',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
ax.set_ylabel('')
ax.set_xlabel('Total Funding (Million USD)')
ax.set_title('Top 10 Funders by Total Funding')
plt.tight_layout()
plt.savefig('../../figures/grant_impact/top_funders_usd.pdf')

top_countries_usd['millions'] = top_countries_usd['total_funding'] / 1_000_000
plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_countries_usd,
    x='millions',
    y='country',
    palette='Oranges_r',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
# set xticks to show 0, 10^1, 10^2, 10^3, 10^4
ax.set_xscale("log")
ax.set_ylabel('')
ax.set_xlabel('Total Funding (Million USD)')
ax.set_title('Top 10 Countries by Total Funding')
plt.tight_layout()
plt.savefig('../../figures/grant_impact/top_countries_usd.pdf')



plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_countries_num,
    x='grants',
    y='country',
    palette='Oranges_r',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
# set xticks to show 0, 10^1, 10^2, 10^3, 10^4
ax.set_xscale("log")
ax.set_xticks([1, 10, 100, 1000, 10000])
ax.set_ylabel('')
ax.set_xlabel('Number of Grants')
ax.set_title('Top 10 Countries by Number of Grants')
plt.tight_layout()
plt.savefig('../../figures/grant_impact/top_countries_num.pdf')
#ax.set_xticklabels(['0', r'$10^1$'])

top_biobanks_usd['millions'] = top_biobanks_usd['total_funding'] / 1_000_000
plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_biobanks_usd,
    x='millions',
    y='biobank',
    palette='Oranges_r',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
# set xticks to show 0, 10^1, 10^2, 10^3, 10^4
ax.set_xscale("log")
ax.set_ylabel('')
ax.set_xlabel('Total Funding (Million USD)')
ax.set_title('Top 10 Biobanks by Total Funding')
ax.set_xticks([1, 10, 100, 1000, 10000])
plt.tight_layout()
plt.savefig('../../figures/grant_impact/top_biobanks_usd.pdf')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_biobanks_num,
    x='grants',
    y='biobank',
    palette='Oranges_r',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
# set xticks to show 0, 10^1, 10^2, 10^3, 10^4
ax.set_ylabel('')
ax.set_xlabel('Number of Grants')
ax.set_title('Top 10 Biobanks by Number of Grants')
ax.set_xticks([0, 500, 1000, 1500])
plt.tight_layout()
plt.savefig('../../figures/grant_impact/top_biobanks_num.pdf')

nih = pd.read_csv('../../data/database/meta/nih_activity_codes.csv')
nih.columns = nih.columns.str.lower()
train_grants = nih[nih['description'].str.contains('training|education', case=False)]['code'].values
# collaboration or intramural
collaboration_grants = nih[nih['description'].str.contains('collaboration|intramural', case=False)]['code'].values
# prestigous grants if have 'highly' in description
prestigious_grants = nih[nih['description'].str.contains('highly|promising', case=False)]['code'].values

grants['activity_code'].fillna('-1', inplace=True)
# flag grant as training if it starts with 'S', 'T', 'F', 'K', or 'D' or 'R25'
grants['training'] = grants['activity_code'].apply(lambda x: True if x[0] in ['T', 'F', 'K', 'D'] or x == 'R25' else False)
# flag grant as training if it is in train_grants
grants['training'] = grants['training'] | grants['activity_code'].isin(train_grants)
# flag grant as collaboration if it starts with 'U'
grants['collaboration'] = grants['activity_code'].apply(lambda x: True if x[0] == 'U' else False)
# flag grant as collaboration if it is in collaboration_grants
grants['collaboration'] = grants['collaboration'] | grants['activity_code'].isin(collaboration_grants)

# get research_orgs countries
research_orgs = grants.explode('research_orgs').dropna(subset=['research_orgs'])
# rename research_orgs to research_org
research_orgs.rename(columns={'research_orgs': 'research_org'}, inplace=True)
# grid rename funder_org to research_org
grid.rename(columns={'funder_org': 'research_org'}, inplace=True)
research_orgs = research_orgs.merge(grid[['research_org', 'country']], on='research_org', how='left')
research_orgs = research_orgs.merge(cohort_grants[['id', 'cohort_name_lower']], on='id', how='left')
grant_cohorts = grants.merge(cohort_grants[['id', 'cohort_name_lower']], on='id', how='left')

# melt grants to get id to be id and value to be bra, hrcs_hc, training, and collaboration
melt = grants.melt(id_vars='id', value_vars=['hrcs_hc'], value_name='value', var_name='variable')
melt = melt[~((melt['value']==False))]
# assign number to be 'collaboration' or 'training' if variable is 'collaboration' or 'training' and value is True
melt.loc[melt['variable']=='collaboration', 'value'] = 'Collaboration'
melt.loc[melt['variable']=='training', 'value'] = 'Training'
melt = melt.dropna()
# Calculate counts for each 'variable' and 'number' combination
counts = melt.groupby(['variable', 'value']).size().reset_index(name='counts')

# Sort the counts in decreasing order within each 'variable'
sorted_counts = counts.sort_values(['variable', 'counts'], ascending=[False, False])

# Get the sorted order for 'variable'
order = sorted_counts['value'].unique()




# Increase the figure size for better readability
plt.figure(figsize=(20, 6))

# Plot using seaborn's countplot
ax = sns.countplot(data=melt, y='value', hue='value', legend=False, order=order, palette='Oranges_r')

# Add value labels
for p in ax.patches:
    ax.annotate(f'{int(p.get_width())}',  # The label
                (p.get_x() + p.get_width(), p.get_y() + p.get_height()/2),  # Position
                xytext=(5, 0),  # Offset
                textcoords='offset points',
                ha='left', va='center')

ax.set_title('Number of Grants by HRCS Categories')
ax.set_ylabel('')
ax.set_xlabel('Number of Grants')
# Show the plot
plt.tight_layout()
plt.savefig('../../figures/grant_impact/hrcs_hc.pdf')
