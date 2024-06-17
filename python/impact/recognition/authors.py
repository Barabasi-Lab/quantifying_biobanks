import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", context='notebook', font_scale=1.2)

papers = pd.read_json('../../../data/expansion/database/mentions/papers.json', lines=True)
cohort_papers = pd.read_csv('../../../data/expansion/cohort_papers.csv')

paper_authors = papers.explode('authors')
paper_authors = paper_authors.dropna(subset=['authors'])
paper_authors['author_id'] = paper_authors['authors'].apply(lambda x: x['researcher_id'] if x and 'researcher_id' in x else np.nan)
paper_authors = paper_authors.dropna(subset=['author_id'])

paper_authors = paper_authors.merge(cohort_papers, on='id')

counts = paper_authors.groupby(['cohort_name_lower', 'author_id']).id.nunique().rename('author_papers').reset_index().sort_values('author_papers', ascending=False)
counts = counts.drop_duplicates(subset='cohort_name_lower')
cohorts = paper_authors.groupby('cohort_name_lower').id.nunique().sort_values(ascending=False).rename('papers').reset_index()
cohorts = cohorts.merge(counts, on='cohort_name_lower', how='left')
cohorts['author_prop'] = cohorts['author_papers'] / cohorts['papers']
cohorts['author_per'] = cohorts['author_prop'] * 100

paper_authors.head()
first = paper_authors.sort_values('year').drop_duplicates(subset=['author_id', 'cohort_name_lower'], keep='first')
last = paper_authors.sort_values('year').drop_duplicates(subset=['author_id', 'cohort_name_lower'], keep='last')
first = first.rename(columns={'year': 'first_pub_year'})
last = last.rename(columns={'year': 'last_pub_year'})
first = first[first['author_id'].isin(cohorts['author_id'])][['cohort_name_lower', 'author_id', 'first_pub_year']]
last = last[last['author_id'].isin(cohorts['author_id'])][['cohort_name_lower', 'author_id', 'last_pub_year']]
cohorts = cohorts.merge(first, on=['cohort_name_lower', 'author_id'], how='left')
cohorts = cohorts.merge(last, on=['cohort_name_lower', 'author_id'], how='left')

potential = paper_authors.merge(cohorts[['cohort_name_lower', 'first_pub_year', 'last_pub_year']], on=['cohort_name_lower'], how='left')
potential = potential[(potential['year'] >= potential['first_pub_year']) & (potential['year'] <= potential['last_pub_year'])].groupby('cohort_name_lower').id.nunique().rename('potential_papers').reset_index()
cohorts = cohorts.merge(potential, on='cohort_name_lower', how='left')
cohorts['author_potential_prop'] = cohorts['author_papers'] / cohorts['potential_papers']
cohorts['author_potential_per'] = cohorts['author_potential_prop'] * 100

counts = paper_authors.groupby(['cohort_name_lower', 'author_id']).id.nunique().rename('author_papers').reset_index().sort_values(['cohort_name_lower', 'author_papers'], ascending=False)
top10 = counts.groupby(['cohort_name_lower']).head(10)
top10authors = top10.groupby('cohort_name_lower').author_id.apply(lambda x: ','.join(x)).rename('top_10_authors').reset_index()
top10 = top10.merge(paper_authors[['cohort_name_lower', 'author_id', 'id']], on=['cohort_name_lower', 'author_id'], how='left')
top10 = top10.groupby('cohort_name_lower').id.nunique().rename('top_10_author_papers').reset_index()
cohorts = cohorts.merge(top10, on='cohort_name_lower', how='left')
cohorts['top_10_author_per'] = cohorts['top_10_author_papers'] / cohorts['papers'] * 100
cohorts = cohorts.merge(top10authors, on='cohort_name_lower', how='left')

counts = paper_authors.groupby(['cohort_name_lower', 'author_id']).id.nunique().rename('author_papers').reset_index().sort_values(['cohort_name_lower', 'author_papers'], ascending=False)
top1 = counts.groupby(['cohort_name_lower']).head(1)
top1 = top1.merge(paper_authors[['cohort_name_lower', 'author_id', 'id', 'citations_count']], on=['cohort_name_lower', 'author_id'], how='left')
# groupby cohort_name_lower and author_id and get citations_count sum and mean
cit1 = top1.groupby(['cohort_name_lower', 'author_id']).citations_count.sum().rename('author_citations').reset_index().fillna(0)
cit2 = top1.groupby(['cohort_name_lower', 'author_id']).citations_count.mean().rename('author_citations_mean').reset_index().fillna(0)
cohorts = cohorts.merge(cit1, on=['cohort_name_lower', 'author_id'], how='left')
cohorts = cohorts.merge(cit2, on=['cohort_name_lower', 'author_id'], how='left')

cohort_papers = cohort_papers.merge(papers[['id', 'citations_count']], on='id', how='left')
total_citations = cohort_papers.groupby('cohort_name_lower').citations_count.sum().rename('cohort_citations').reset_index().fillna(0)
mean_citations = cohort_papers.groupby('cohort_name_lower').citations_count.mean().rename('cohort_citations_mean').reset_index().fillna(0)
cohorts = cohorts.merge(total_citations, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(mean_citations, on='cohort_name_lower', how='left')

orgs_papers = papers.explode('research_orgs').dropna(subset=['research_orgs'])
orgs_papers = orgs_papers.merge(cohort_papers[['cohort_name_lower', 'id']], on='id')
cohort_orgs = orgs_papers.groupby('cohort_name_lower')['id'].nunique().rename('cohort_papers_with_orgs').reset_index().sort_values('cohort_papers_with_orgs', ascending=False)
paper_orgs = orgs_papers.groupby(['cohort_name_lower', 'research_orgs']).id.nunique().rename('org_papers').reset_index().sort_values(['cohort_name_lower', 'org_papers'], ascending=False)
paper_orgs = paper_orgs.drop_duplicates(subset='cohort_name_lower')
paper_orgs = paper_orgs.merge(cohort_orgs, on='cohort_name_lower', how='left')
# rename research_orgs to top_org
paper_orgs = paper_orgs.rename(columns={'research_orgs': 'top_org'})
# merge with cohorts
cohorts = cohorts.merge(paper_orgs, on='cohort_name_lower', how='left')

# plot the kde of author proportion
plt.figure(figsize=(10, 6))
g = sns.kdeplot(data=cohorts[cohorts['papers'] > 10], x='top_10_author_per', fill=True, color='skyblue', alpha=0.5)
g.set_xlabel('Percentage of Cohort Papers by Top 10 Authors')
g.set_ylabel('Density')
g.set_title('Distribution of Percentage of Cohort Papers by Top 10 Authors (N > 100)')

# plot scatterplot seaborn
plt.figure(figsize=(10, 6))
g = sns.scatterplot(data=cohorts, x='org_papers', y='papers', color='skyblue',
                    alpha=0.3)
g = sns.scatterplot(data=cohorts, x='author_papers', y='papers', color='C1',
                    alpha=0.3)
# legend gray marker is author_papers and skyblue marker is org_papers
g.legend(['Top Insitution Papers', 'Top Author Papers'])


g.set_xscale('log')
g.set_yscale('log')
g.set_xlabel('Top Institution Papers in Cohort Papers')
g.set_ylabel('Total Cohort Papers')
g.set_title('Top Insitution Papers in Cohort Papers vs Total Cohort Papers')

cohorts.to_csv('../../../data/expansion/database/cohort_impact/authors_impact.csv', index=False)
