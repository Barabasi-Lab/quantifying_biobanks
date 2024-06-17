import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import spacy

nlp = spacy.load('en_core_web_sm')


sns.set_theme(style="white", context="notebook", font_scale=1.2)

# read database/foundational/papers.json
df = pd.read_json('../../../data/expansion/database/foundational/papers.json', lines=True)

papers = pd.read_json('../../../data/expansion/database/mentions/papers.json', lines=True)
cohorts = pd.read_csv('../../../data/expansion/cohorts.csv')
cohort_papers = pd.read_csv('../../../data/expansion/cohort_papers.csv')
cohort_papers = cohort_papers.merge(papers, on='id', how='left')
df = df.merge(papers[['id', 'citations_count']], on='id', how='left')
df['prop_citations_from_mentions'] = df['inner_citations'] / df['citations_count']
authors = pd.read_csv('../../../data/expansion/database/cohort_impact/authors_impact.csv')


early = df[df['years_after_first_mention'] == 0]
early = early[early['inner_references'] == 0].drop_duplicates(subset='id')
early = early[early['inner_citations'] > 10]

df = df.sort_values('inner_citations', ascending=False)

df = df[df['prop_inner_citations'] != 0 ]

main = df.drop_duplicates(subset='cohort_name_lower')
main = main[main['inner_citations'] > 10].drop_duplicates(subset='id')

design = df[df['title'].str.contains('design', case=False, na=False)]
objectives = df[df['title'].str.contains('objectives', case=False, na=False)]
methodology = df[df['title'].str.contains('Methodology', case=False, na=False)]
rationale = df[df['title'].str.contains('rationale', case=False, na=False)]
baseline = df[df['title'].str.contains('baseline', case=False, na=False)]
characteristics = df[df['title'].str.contains('and characteristics', case=False, na=False)]

# concat design and the rest
key = pd.concat([design, objectives, methodology, rationale, baseline, characteristics]).drop_duplicates(subset='id')
key = key[(key['prop_citations_from_mentions'] > 0.3) & (key['inner_citations'] > 10)]

cohort_profile = df[df['title'].str.contains('cohort profile', case=False, na=False)]

outlier = df.groupby('cohort_name_lower').prop_inner_citations.apply(lambda x: x.quantile(0.95)).rename('quantile_95').reset_index().sort_values('quantile_95', ascending=False)
outlier = outlier.merge(df, on='cohort_name_lower', how='left')
outlier = outlier[(outlier['prop_inner_citations'] > outlier['quantile_95']) & (outlier['inner_citations'] > 100) & (outlier['prop_inner_citations'] > 0.1)]

reference = pd.concat([early, main, key, cohort_profile, outlier]).drop_duplicates(subset='id')

ref_papers = set(reference.id.to_list())
paper_refs = cohort_papers[['cohort_name_lower', 'reference_ids']]
paper_refs = paper_refs.dropna()
paper_refs['reference_ids'] = paper_refs['reference_ids'].apply(set)
paper_refs = paper_refs.values
citing_papers = dict()
for paper in paper_refs:
    citing_papers.setdefault(paper[0], 0)
    if paper[1] & ref_papers:
        citing_papers[paper[0]] += 1
citing_papers = pd.DataFrame(citing_papers.items(), columns=['cohort_name_lower', 'citing_papers'])
hidden = citing_papers.merge(cohorts[['cohort_name_lower', 'pubs']], on='cohort_name_lower', how='left')
hidden['citing_papers_prop'] = hidden['citing_papers'] / hidden['pubs']
hidden = hidden.sort_values('pubs', ascending=False)
# read authors_impact.csv
authors = pd.read_csv('../../../data/expansion/database/cohort_impact/authors_impact.csv')

# Assuming 'main' is your DataFrame and it's already loaded
# Let's take the first 50 cohorts
main['year_first_mention'] = main['year'] - main['years_after_first_mention']
main = cohorts.merge(main, on='cohort_name_lower', how='left')
df_plot = main.head(50)
def get_initials(name):
    doc = nlp(name)
    initials = ''.join([chunk.norm_[0].upper() for chunk in doc if chunk.pos_ not in ['CCONJ', 'ADP',  'SYM', 'AUX', 'DET', 'PUNCT', 'PART']])

    return initials
# Convert 'cohort_name_lower' to initials
df_plot['cohort_initials'] = df_plot['cohort_name_lower'].apply(get_initials)

# Set up the matplotlib figure
plt.figure(figsize=(10, 15))

# Create lollipop chart for year of the first mention
plt.hlines(y=df_plot['cohort_initials'], xmin=df_plot['year_first_mention'], xmax=df_plot['year'], color='gray', alpha=0.4, linewidth=3)
plt.scatter(df_plot['year_first_mention'], df_plot['cohort_initials'], color='gray', alpha=1, label='Year of First Mention')

# Create lollipop chart for year the paper was published
plt.scatter(df_plot['year'], df_plot['cohort_initials'], color='#D37676', alpha=1, label='Reference Paper Published')


# Create lollipop chart for mean citation year
# plt.hlines(y=df_plot['cohort_initials'], xmin=df_plot['year'], xmax=df_plot['mean_citation_year'], color='#114232', alpha=0.4, linewidth=3)
plt.scatter(df_plot['mean_citation_year'], df_plot['cohort_initials'], color='black', alpha=1, label='Cohort Mean Year of Mentions', marker='*', s=60)

# Add titles and labels
plt.title('Publication Year of Cohort Reference Paper vs First and Mean Year of Cohort Mentions', loc='left', fontsize=16, fontweight=0, color='black')
plt.xlabel('Year')
plt.ylabel('Cohort')

# Remove spines
sns.despine()

# Add legend
plt.legend()

# Show the plot
plt.show()

df_plot['total'] = 1
plt.figure(figsize=(10, 15))

# Create lollipop chart for year of the first mention
plt.hlines(y=df_plot['cohort_initials'], xmin=df_plot['prop_hidden_citations'], xmax=df_plot['total'], color='gray', alpha=0.4, linewidth=3, label='Hidden Citations')
plt.scatter(df_plot['prop_hidden_citations'], df_plot['cohort_initials'], color='#D37676', alpha=1, label='Citing')

# Create lollipop chart for year the paper was published
plt.scatter(df_plot['total'], df_plot['cohort_initials'], color='gray', alpha=1, label='Total')


# Create lollipop chart for mean citation year

# Add titles and labels
plt.title('Hidden Citations of Cohorts', loc='left', fontsize=16, fontweight=0, color='black')
plt.xlabel('Mentions (%)')
plt.ylabel('Cohort')
# Remove spines
sns.despine()
plt.xlim(0, 1.1)
# add vertical grid
plt.grid(axis='x')

# Add legend outside the plot with bbox_to_anchor
plt.legend(loc='center left', bbox_to_anchor=(0.5, 1))
plt.tight_layout()
# Show the plot
plt.show()

hidden = hidden.sort_values('pubs', ascending=False)
df_plot = hidden.head(50)
df_plot['initials'] = df_plot['cohort_name_lower'].apply(get_initials)

df_plot['total'] = 1
plt.figure(figsize=(10, 15))

# Create lollipop chart for year of the first mention
plt.hlines(y=df_plot['initials'], xmin=df_plot['citing_papers_prop'], xmax=df_plot['total'], color='gray', alpha=0.4, linewidth=3, label='Hidden Citations')
plt.scatter(df_plot['citing_papers_prop'], df_plot['initials'], color='#D37676', alpha=1, label='Citing')

# Create lollipop chart for year the paper was published
plt.scatter(df_plot['total'], df_plot['initials'], color='gray', alpha=1, label='Total')


# Create lollipop chart for mean citation year

# Add titles and labels
plt.title('Hidden Citations of Cohorts', loc='left', fontsize=16, fontweight=0, color='black')
plt.xlabel('Mentions (%)')
plt.ylabel('Cohort')
# Remove spines
sns.despine()
plt.xlim(0, 1.1)
# add vertical grid
plt.grid(axis='x')

# Add legend outside the plot with bbox_to_anchor
plt.legend(loc='center left', bbox_to_anchor=(0.5, 1))
plt.tight_layout()
# Show the plot
plt.show()

# save reference papers to csv
reference.to_csv('../../../data/expansion/database/cohort_impact/reference_papers.csv', index=False)
# save hidden citations to csv
hidden.to_csv('../../../data/expansion/database/cohort_impact/hidden_citations.csv', index=False)
