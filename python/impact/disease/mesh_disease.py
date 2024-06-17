import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


papers = pd.read_json('../../../data/database/mentions/papers.json', lines=True)
papers = papers[papers['year'] < 2024]
papers = papers[papers['year'] >= 2000]
cohort_papers = pd.read_csv('../../../data/database/cohort_papers.csv')

mesh = pd.read_csv('../../../data/database/meta/mesh.csv')
mesh['disease'] = mesh['tree_number'].apply(lambda x: True if x.startswith('C') else False)
mesh = mesh[mesh['disease']]
mesh['main_level'] = mesh['tree_number'].apply(lambda x: x.split('.')[0])
main_level = mesh[mesh['tree_number'].apply(lambda x: len(x.split('.')) == 1)][['main_level', 'mesh_name', 'mesh_id']].rename(columns={'mesh_name': 'main_mesh_name', 'mesh_id': 'main_mesh_id'})

pmesh = papers.explode('mesh_ids').dropna(subset=['mesh_ids'])
pmesh.rename(columns={'mesh_ids': 'mesh_id'}, inplace=True)
pmesh = pmesh.merge(mesh)
pmesh = pmesh.merge(main_level, on='main_level')
pmesh = cohort_papers.merge(pmesh, on='id')
cohort_mesh = pmesh.groupby(['cohort_name_lower', 'mesh_name', 'mesh_id', 'main_mesh_id', 'main_mesh_name', 'year']).id.nunique().rename('papers').reset_index()
dis_papers = pmesh.groupby(['mesh_name', 'mesh_id', 'year']).id.nunique().rename('papers').reset_index()
dis_papers = dis_papers.sort_values('papers', ascending=False)
# 108498 papers with mesh_ids
# rename mesh_ids to mesh_id

# read meta/pubs_mesh_diseases.csv
# total papers: 10486605
TOTAL_DIS_PAPERS = 10486605
pubs = pd.read_csv('../../../data/database/meta/pubs_mesh_diseases_2000_year.csv')

cohort_mesh = cohort_mesh.merge(pubs, on=['mesh_id', 'year'], how='left')
cohort_mesh['year_prop'] = cohort_mesh['papers'] / cohort_mesh['total_papers']
cohort_mesh = cohort_mesh.drop_duplicates(subset=['cohort_name_lower', 'mesh_id'])
cohort_mesh = cohort_mesh.sort_values('year_prop', ascending=False)
cohort_max = cohort_mesh.drop_duplicates(subset=['cohort_name_lower', 'mesh_id'])

pubs_main = pubs[pubs['total_papers'] >= 100]


mesh_2 = mesh[mesh['tree_number'].apply(lambda x: len(x.split('.')) == 2)]

cohort_broad = cohort_mesh[(cohort_mesh['total_papers']>=10)].groupby('cohort_name_lower').year_prop.sum().rename('broad_impact').reset_index()

cohort_spec = cohort_mesh[(cohort_mesh['mesh_id'].isin(pubs_main['mesh_id'].unique())) & (cohort_mesh['mesh_id'].isin(mesh_2.mesh_id.unique()))].groupby(['cohort_name_lower', 'mesh_name']).year_prop.mean().rename('specific_impact').reset_index()
cohort_spec = cohort_spec.sort_values('specific_impact', ascending=False).drop_duplicates(subset='cohort_name_lower')
# rename mesh_name to specific_mesh_name
cohort_spec.rename(columns={'mesh_name': 'specific_mesh_name'}, inplace=True)

disease_impact = cohort_broad.merge(cohort_spec, on='cohort_name_lower', how='left')

# save to csv
disease_impact.to_csv('../../../data/expansion/database/cohort_impact/disease_impact_mesh.csv', index=False)

top_scope = cohort_mesh.groupby('cohort_name_lower').mesh_id.nunique().rename('conditions').reset_index().sort_values('conditions', ascending=False).head(10)
top_spec = cohort_spec.head(10)
top_scope['biobank'] = top_scope['cohort_name_lower'].apply(lambda x: ' '.join(x.split()[1:]))
top_spec['biobank'] = top_spec['cohort_name_lower'].apply(lambda x: ' '.join(x.split()[1:]))

# Adjusted figure size for better aspect ratio and readability
fig, ax = plt.subplots(figsize=(12, 7))

# Use a diverse color palette and order bars by count
g = sns.barplot(data=top_scope, x='conditions', y='biobank', ax=ax, hue='biobank',
                    palette='Greys_r',  # Using a visually appealing color palette
                    )  # Order bars by count

# Set meaningful labels and title
g.set_xlabel('Number of Conditions Studied')
g.set_ylabel('')
g.set_title('Top 10 Biobanks By Disease Scope', fontsize=16)

# Improve readability
sns.despine(left=True, bottom=True)  # Remove the top and right spines
# Add horizontal gridlines for better readability
plt.grid(axis='x', color='gray', linestyle='--', linewidth=0.5)

# Annotations for each bar to show the count
for p in ax.patches:
    width = p.get_width()
    ax.text(width + 3,  # Position the text 3 units right from the bar's end
            p.get_y() + p.get_height() / 2,
            int(width),  # The count
            ha='left', va='center')
plt.tight_layout()
plt.savefig('../../../figures/disease_impact/top_biobanks_scope.pdf')

# calculate percentage based on specific impact and remove decimals
top_spec['specific_impact'] = top_spec['specific_impact'] * 100
top_spec['specific_impact'] = top_spec['specific_impact'].apply(lambda x: round(x, 0))


# Adjusted figure size for better aspect ratio and readability
fig, ax = plt.subplots(figsize=(12, 7))

# Use a diverse color palette and order bars by count
g = sns.barplot(data=top_spec, x='specific_impact', y='biobank', ax=ax, hue='biobank',
                    palette='Greys_r',  # Using a visually appealing color palette
                    )  # Order bars by count

# Set meaningful labels and title
g.set_xlabel('Percentage of Publications Relative to Total Papers for a Condition')
g.set_ylabel('')
g.set_title('Top 10 Biobanks By Disease Depth', fontsize=16)

# Improve readability
sns.despine(left=True, bottom=True)  # Remove the top and right spines
# Add horizontal gridlines for better readability
plt.grid(axis='x', color='gray', linestyle='--', linewidth=0.5)

# Annotations for each bar to show the count
for p in ax.patches:
    width = p.get_width()
    ax.text(width + 0.2,  # Position the text 3 units right from the bar's end
            p.get_y() + p.get_height() / 2,
            str(int(width))+'%',  # The count
            ha='left', va='center')
plt.tight_layout()
plt.savefig('../../../figures/disease_impact/top_biobanks_depth.pdf')