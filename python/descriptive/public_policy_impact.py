import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

policy = pd.read_json('../../data/expansion/database/mentions/policies.json', lines=True)
cohort_policy = pd.read_csv('../../data/expansion/cohort_policy.csv')
policy = policy[policy['id'].isin(cohort_policy['id'])]
policy_impact = pd.read_csv('../../data/expansion/database/cohort_impact/policy.csv')

top_publishers = policy.groupby('publisher').id.nunique().reset_index().sort_values('id', ascending=False).head(10)
top_biobanks = policy_impact.sort_values('policies', ascending=False).head(10)
top_biobanks['biobank'] = top_biobanks['cohort_name_lower'].apply(lambda x: ' '.join(x.split()[1:]))

# Adjusted figure size for better aspect ratio and readability
fig, ax = plt.subplots(figsize=(12, 7))

# Use a diverse color palette and order bars by count
g = sns.barplot(data=top_biobanks, x='policies', y='biobank', ax=ax, hue='biobank',
                    palette='Greens_r',  # Using a visually appealing color palette
                    )  # Order bars by count

# Set meaningful labels and title
g.set_xlabel('Number of Public Policies')
g.set_ylabel('')
g.set_title('Top 10 Biobanks by Public Policies', fontsize=16)

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
plt.savefig('../../figures/public_policy_impact/top_biobanks.pdf')

# Adjusted figure size for better aspect ratio and readability
fig, ax = plt.subplots(figsize=(12, 7))

# Use a diverse color palette and order bars by count
g = sns.barplot(data=top_publishers, x='id', y='publisher', ax=ax, hue='publisher',
                    palette='Greens_r',  # Using a visually appealing color palette
                    )  # Order bars by count

# Set meaningful labels and title
g.set_xlabel('Number of Public Policies')
g.set_ylabel('')
g.set_title('Top 10 Institutions by Public Policies', fontsize=16)

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
plt.savefig('../../figures/public_policy_impact/top_institutions.pdf')