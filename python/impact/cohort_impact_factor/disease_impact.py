import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

impact_factor = pd.read_csv('../../../data/expansion/database/cohort_impact/target_impact.csv')
mesh = pd.read_csv('../../../data/expansion/database/cohort_impact/disease_impact_mesh.csv')
mesh_disease = pd.read_csv('../../../data/expansion/database/cohort_impact/mesh_impact.csv')
mesh['broad_impact_norm'] = (mesh['broad_impact'] - mesh['broad_impact'].mean()) / mesh['broad_impact'].std()
mesh['specific_impact_norm'] = (mesh['specific_impact'] - mesh['specific_impact'].mean()) / mesh['specific_impact'].std()


mesh['disease_impact'] = mesh['broad_impact_norm'] + mesh['specific_impact_norm']
mesh = mesh.merge(impact_factor[['cohort_name_lower', 'year']], on='cohort_name_lower', how='left')
mesh = mesh.dropna(subset=['year'])
mesh = mesh.fillna(0)

mesh['disease_impact_norm'] = mesh['disease_impact'] / (2023 - mesh['year'] + 1)
# order by disease_impact_norm
mesh = mesh.sort_values('disease_impact_norm', ascending=False)

rcdc = pd.read_csv('../../../data/expansion/database/cohort_impact/rcdc_impact.csv')
rcdc = rcdc.fillna(0)
rcdc = rcdc.merge(impact_factor[['cohort_name_lower', 'year']], on='cohort_name_lower', how='left')
rcdc['rare_disease_impact'] = (rcdc['rare_disease'] - rcdc['rare_disease'].mean()) / rcdc['rare_disease'].std()
rcdc['rare_disease_impact'] = rcdc['rare_disease'] / rcdc['papers']
rcdc['rare_disease_impact_norm'] = rcdc['rare_disease_impact'] / (2023 - rcdc['year'] + 1)
# norm from 0 to 1
rcdc['rare_disease_impact_norm'] = (rcdc['rare_disease_impact_norm'] - rcdc['rare_disease_impact_norm'].min()) / (rcdc['rare_disease_impact_norm'].max() - rcdc['rare_disease_impact_norm'].min())
# order by rare_disease_impact_norm
rcdc = rcdc.sort_values('rare_disease_impact_norm', ascending=False)
rcdc = rcdc.dropna()



rcdc = rcdc[rcdc.cohort_name_lower != 'the childhood cancer survivors']
top_rare = rcdc[rcdc.papers >= 50].sort_values('rare_disease_impact', ascending=False).head(10)
top_rare['biobank'] = top_rare['cohort_name_lower'].apply(lambda x: ' '.join(x.split()[1:]))
top_rare['percent'] = top_rare['rare_disease_impact'] * 100


# truncate to int
top_rare['percent'] = top_rare['percent'].apply(lambda x: int(x))

# Adjusted figure size for better aspect ratio and readability
fig, ax = plt.subplots(figsize=(12, 7))

# Use a diverse color palette and order bars by count
g = sns.barplot(data=top_rare, x='percent', y='biobank', ax=ax, hue='biobank',
                    palette='Greys_r',  # Using a visually appealing color palette
                    )  # Order bars by count

# Set meaningful labels and title
g.set_xlabel('Percentage of Rare Disease Publications')
g.set_ylabel('')
g.set_title('Top 10 Biobanks By Rare Disease Publications', fontsize=16)

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
plt.savefig('../../../figures/disease_impact/top_rare_disease.pdf')

# only keep cohort_name_lower and disease_impact
disease_impact = mesh[['cohort_name_lower', 'disease_impact_norm']]
disease_impact = disease_impact.merge(rcdc[['cohort_name_lower', 'rare_disease_impact_norm']], on='cohort_name_lower', how='outer')
disease_impact = disease_impact.fillna(0)
disease_impact['impact'] = 0.8 * disease_impact['disease_impact_norm'] + 0.2 * disease_impact['rare_disease_impact_norm']
# order by impact
disease_impact = disease_impact.sort_values('impact', ascending=False)
# save to csv
disease_impact.to_csv('../../../data/expansion/database/cohort_impact/disease_target_impact.csv', index=False)
