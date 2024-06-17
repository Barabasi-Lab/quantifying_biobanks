import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import countrynames
import spacy
import plotly.express as px



cohort_papers = pd.read_csv('../../data/expansion/cohort_papers.csv')
cohort_grants = pd.read_csv('../../data/expansion/cohort_grants.csv')
cohort_patents = pd.read_csv('../../data/expansion/cohort_patents.csv')
cohort_clinical_trials = pd.read_csv('../../data/expansion/cohort_clinical_trials.csv')
cohort_policy = pd.read_csv('../../data/expansion/cohort_policy.csv')

papers = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)
grants = pd.read_json('../../data/expansion/database/mentions/grants.json', lines=True)
policy = pd.read_json('../../data/expansion/database/mentions/policies.json', lines=True)
patents = pd.read_json('../../data/expansion/database/mentions/patents.json', lines=True)
clinical_trials = pd.read_json('../../data/expansion/database/mentions/clinical_trials.json')

years = papers.groupby('year').id.nunique().rename('papers').reset_index()
years_grant = grants.groupby('start_year').id.nunique().rename('grants').reset_index()
# rename start_year to year
years_grant.rename(columns={'start_year': 'year'}, inplace=True)
years_policy = policy.groupby('year').id.nunique().rename('policies').reset_index()
years_clinical_trials = clinical_trials.groupby('start_year').id.nunique().rename('clinical_trials').reset_index()
# rename start_year to year
years_clinical_trials.rename(columns={'start_year': 'year'}, inplace=True)
years_patents = patents.groupby('publication_year').id.nunique().rename('patents').reset_index()
# rename publication_year to year
years_patents.rename(columns={'publication_year': 'year'}, inplace=True)

# merge all years
years = years.merge(years_grant, how='outer')
years = years.merge(years_policy, how='outer')
years = years.merge(years_clinical_trials, how='outer')
years = years.merge(years_patents, how='outer')

# between 1970 and 2022
years = years[(years['year'] >= 1985) & (years['year'] <= 2022)]

# save to descriptive folder
years.to_csv('../../data/expansion/database/descriptive/mention_years.csv', index=False)

data = years


sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

# Define the size of the figure
plt.figure(figsize=(14, 8))
# set labels to large

# Plotting each category
plt.plot(data['year'], data['papers'], marker='o', linestyle='-', label='Papers')
plt.plot(data['year'], data['grants'], marker='s', linestyle='-', label='Grants')
plt.plot(data['year'], data['policies'], marker='^', linestyle='-', label='Public Policies')
plt.plot(data['year'], data['clinical_trials'], marker='x', linestyle='-', label='Clinical Trials')
plt.plot(data['year'], data['patents'], marker='d', linestyle='-', label='Patents')

# Adding title and labels
plt.title('Yearly Count of Biobank Mentions: 1985-2022', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Biobank Mentions')
plt.xticks(rotation=45)
plt.legend(title='Mentioned in', title_fontsize='large', fontsize='medium', loc='upper left', frameon=True, shadow=True)
# set y scale to log
plt.yscale('log')

# Adding a grid for better readability
plt.grid(True, which='major', linestyle='--', linewidth=0.5, color='grey', alpha=0.3)

# Show the plot
plt.tight_layout()

# save as pdf
plt.savefig('../../figures/mentions/years_mentions.pdf')
# save as png
plt.savefig('../../figures/mentions/years_mentions.png')


