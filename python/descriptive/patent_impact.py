import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

patents = pd.read_json('../../data/expansion/database/mentions/patents.json', lines=True)
cohort_patents = pd.read_csv('../../data/expansion/cohort_patents.csv')
patents = patents[patents['id'].isin(cohort_patents['id'])]
patent_impact = pd.read_csv('../../data/expansion/database/cohort_impact/patent_impact.csv')
# rename bioinformatics for information_technology
patent_impact.rename(columns={'bioinformatics': 'information_technology'}, inplace=True)
# rename therapeutic for therapeutics
patent_impact.rename(columns={'therapeutic': 'therapeutics'}, inplace=True)
pat_type_cols = ['biotechnology', 'information_technology', 'therapeutics', 'pharmaceutical', 'diagnostics', 'food']
# melt patent_impact by pat_type_cols
pat_type = patent_impact.sum().reset_index()
pat_type.columns = ['patent_type', 'patents']
pat_type = pat_type[pat_type['patent_type'].isin(pat_type_cols)]
# add patent_type other for the rest of the patents
pat_type = pat_type.append({'patent_type': 'other', 'patents': patents.id.nunique() - pat_type['patents'].sum()}, ignore_index=True)
pat_type = pat_type.sort_values('patents', ascending=False)

# Adjusted figure size for better aspect ratio and readability
fig, ax = plt.subplots(figsize=(12, 7))

# Use a diverse color palette and order bars by count
g = sns.barplot(data=pat_type, x='patents', y='patent_type', ax=ax, hue='patent_type',
                    palette='Purples_r',  # Using a visually appealing color palette
                    )  # Order bars by count

# Set meaningful labels and title
g.set_xlabel('Number of Patents')
g.set_ylabel('')
g.set_title('Distribution of Patents by Type', fontsize=16)

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
plt.savefig('../../figures/patent_impact/patent_types.pdf')

cpc_a = pd.read_csv(
    '../../data/patent_classification/cpc_humans.tsv', sep='\t')
cpc_a.columns = ['cpc', 'level', 'description']

cpc_c = pd.read_csv(
    '../../data/patent_classification/cpc_chemistry.tsv', sep='\t')
cpc_c.columns = ['cpc', 'level', 'description']

cpc_g = pd.read_csv(
    '../../data/patent_classification/cpc_physics.tsv', sep='\t')
cpc_g.columns = ['cpc', 'level', 'description']

cpc_y = pd.read_csv('../../data/patent_classification/cpc_y.tsv', sep='\t')
cpc_y.columns = ['cpc', 'level', 'description']

cpc = pd.concat([cpc_a, cpc_c, cpc_g, cpc_y])
cpc['level'].fillna(-1, inplace=True)
