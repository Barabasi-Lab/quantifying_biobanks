import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

trials = pd.read_json('../../data/expansion/database/mentions/clinical_trials.json')
cohort_trials = pd.read_csv('../../data/expansion/cohort_clinical_trials.csv')
trials = trials[trials['id'].isin(cohort_trials['id'])]
trial_impact = pd.read_csv('../../data/expansion/database/cohort_impact/clinical_trials_impact.csv')
# drop the smart study from cohorts
trial_impact = trial_impact[trial_impact['cohort_name_lower'] != 'the smart study']

trial_impact['biobank'] = trial_impact['cohort_name_lower'].apply(lambda x: ' '.join(x.split()[1:]))
top_biobanks = trial_impact.sort_values('clinical_trials', ascending=False).head(10)

# Adjusted figure size for better aspect ratio and readability
fig, ax = plt.subplots(figsize=(12, 7))

# Use a diverse color palette and order bars by count
g = sns.barplot(data=top_biobanks, x='clinical_trials', y='biobank', ax=ax, hue='biobank',
                    palette='Reds_r',  # Using a visually appealing color palette
                    )  # Order bars by count

# Set meaningful labels and title
g.set_xlabel('Number of Clinical trials')
g.set_ylabel('')
g.set_title('Top 10 Biobanks by Clinical Trials', fontsize=16)

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
plt.savefig('../../figures/clinical_trials_impact/top_biobanks.pdf')