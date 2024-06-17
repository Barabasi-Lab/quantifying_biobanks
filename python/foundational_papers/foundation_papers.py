import pandas as pd
import numpy as np

# read database/foundational/papers.json
df = pd.read_json('../../data/database/foundational/papers.json', lines=True)

cohorts = pd.read_csv('../../data/database/cohorts.csv')
pub = pd.read_json('../../data/database/mentions/papers.json', lines=True)

df['prop_post_mentions_citing'] = df['post_mentions_citing'] / df['post_mentions']
df = df.merge(pub[['id', 'citations_count']], on='id', how='left')
# rename pubs column in cohorts to mentions
cohorts = cohorts.rename(columns={'pubs': 'cohort_mentions'})
df = df.merge(cohorts[['cohort_name_lower', 'cohort_mentions']], on='cohort_name_lower', how='left')

df['prop_citations_inner'] = df['inner_citations'] / df['citations_count']
# round to 2 decimal places
df['prop_citations_inner'] = df['prop_citations_inner'].apply(lambda x: round(x, 2))

df['prop_post_mentions'] = df['post_mentions'] / df['cohort_mentions']
main = df.drop_duplicates(subset='cohort_name_lower')
main = main.sort_values('cohort_mentions', ascending=False)
main.to_csv('../../data/database/foundational/main.csv', index=False)
