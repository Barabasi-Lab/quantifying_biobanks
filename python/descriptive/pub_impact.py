import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

papers = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)
cohort_papers = pd.read_csv('../../data/expansion/cohort_papers.csv')
cohorts = pd.read_csv('../../data/expansion/cohorts.csv')
cohort_initials = pd.read_csv('../../data/expansion/cohort_initials.csv')
cohorts['biobank'] = cohorts['cohort_name_lower'].apply(lambda x: ' '.join(x.split()[1:]))
papers_cohorts = papers.merge(cohort_papers, on='id')
cit = papers_cohorts.groupby('cohort_name_lower').citations_count.sum().rename('citations').reset_index()
cohorts = cohorts.merge(cit, on='cohort_name_lower', how='left')
sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)
cohort_sources = pd.read_csv('../../data/expansion/cohort_sources.csv')
source = cohort_sources.groupby(['cohort_name_lower', 'source']).id.nunique().rename('papers').reset_index()
cohort_sources = cohort_sources.merge(papers[['id', 'year', 'citations_count']], on='id')

paper_authors = papers.explode('authors')
paper_authors = paper_authors.dropna(subset=['authors'])
paper_authors['author'] = paper_authors['authors'].apply(lambda x: x['researcher_id'] if 'researcher_id' in x else np.nan)
paper_authors['corresponding'] = paper_authors['authors'].apply(lambda x: x['corresponding'] if 'corresponding' in x else False)
paper_authors = paper_authors.dropna(subset=['author'])
paper_authors = paper_authors[['id', 'author', 'corresponding']]
paper_authors = paper_authors.merge(papers[['id', 'year', 'citations_count']], on='id')


# plot pubs distribution
plt.figure(figsize=(14, 8))
sns.boxplot(data=cohorts, y='pubs', log_scale=True)
sns.boxplot(data=cohorts, y='citations', log_scale=True)
sns.boxplot(data=source, y='papers', log_scale=True, hue='source')
sns.boxplot(data=cohort_sources, y='citations_count', log_scale=True, hue='source')
plt.title('Distribution of Biobank Mentions in Publications')

# plot top 10 journals by unique id
top_journals = papers.groupby('journal').id.nunique().nlargest(10).reset_index()
plt.figure(figsize=(14, 8))
sns.barplot(data=top_journals, x='id', y='journal')

# plot top 10 journals by citations
top_journals = papers.groupby('journal').citations_count.sum().nlargest(10).reset_index()
top_cohorts = cohorts.nlargest(10, 'citations')
top_cohorts_mentions = cohorts.nlargest(10, 'pubs')
top_authors = paper_authors.groupby('author').citations_count.sum().nlargest(10).reset_index()
top_authors_mentions = paper_authors.groupby('author').id.nunique().nlargest(10).reset_index()
top_corresponding_mentions = paper_authors[paper_authors['corresponding']].groupby('author').id.nunique().nlargest(10).reset_index()
top_corresponding_citations = paper_authors[paper_authors['corresponding']].groupby('author').citations_count.sum().nlargest(10).reset_index()

cohort_authors = paper_authors.merge(cohort_papers, on='id')

author_names = {
    'ur.01337072056.92': 'Ahmedin M Jemal',
    'ur.01014206574.87': 'Rebecca L Siegel',
    'ur.012212666457.88': 'Ronald C Kessler',
    'ur.0607477203.05': 'Walter Churchill Willett',
    'ur.0670056120.12': 'Albert Hofman',
    'ur.011571562657.02': 'Joann Elisabeth Manson',
    'ur.012201547057.87': 'Meir Jonathan Stampfer',
    'ur.01247562420.46': 'Kimberly D Miller',
    'ur.01302706715.35': 'Daniel A Levy',
    'ur.01365031571.41': 'Frank Bingchang Hu',
    'ur.01013747367.23': 'Aaron R Folsom',
    'ur.010663343457.34': 'George G Davey Smith',
    'ur.011026120037.74': 'Ian John Deary',
    'ur.011614604737.21': 'Edward Luciano Giovannucci',
    'ur.012700421217.04': 'Joseph Coresh',
    'ur.015356157217.08': 'Luigi G Ferrucci',
    'ur.01251742611.10': 'Gerald Sanders Berenson',
    'ur.0607050220.48': 'Shou-Ling Wu',
    'ur.01312451146.19': 'Henning W Tiemeier',
    'ur.0724720553.80': 'Parvin Mirmiran',
    'ur.07461536757.28': 'Demosthenes B Panagiotakos',
    'ur.01060421464.45': 'Susanna C Larsson',
    'ur.01157620052.87': 'Hiroyasu Iso',
    'ur.01013747367.23': 'Aaron R Folsom',
    'ur.01351436610.29': 'Shaun M Purcell',
    'ur.012322451762.61': 'Linda P Fried',
    'ur.01057336674.48': 'Arul M Chinnaiyan',
    'ur.0703130243.00': 'Daniel G Macarthur',
    'ur.011517303117.07': 'Mark Joseph Daly',
    'ur.01342616137.05': 'Alkes L Price',
    'ur.0723426172.10': 'Kari Stefansson',
    
}
top_authors['author_name'] = top_authors['author'].apply(lambda x: author_names[x] if x in author_names else x)
top_authors_mentions['author_name'] = top_authors_mentions['author'].apply(lambda x: author_names[x] if x in author_names else x)
top_corresponding_citations['author_name'] = top_corresponding_citations['author'].apply(lambda x: author_names[x] if x in author_names else x)
top_corresponding_mentions['author_name'] = top_corresponding_mentions['author'].apply(lambda x: author_names[x] if x in author_names else x)

plt.figure(figsize=(14, 8))
sns.barplot(data=top_journals, x='citations_count', y='journal')
sns.barplot(data=top_cohorts, x='citations', y='biobank')

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)
sns.barplot(data=top_cohorts_mentions, x='pubs', y='biobank')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_cohorts_mentions,
    x='pubs',
    y='biobank',
    palette='coolwarm',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)

# Add labels and title for clarity
plt.xlabel('Publications', fontsize=14, labelpad=15)
plt.ylabel('', fontsize=14, labelpad=15)
plt.title('Top 10 Biobanks (Mentions)', fontsize=16, pad=20)
# Annotate bars with values
for p in ax.patches:
    width = p.get_width()  # get bar length
    ax.text(width + 10,       # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + half of bar width
            '{:1.0f}'.format(width),  # your value label, formatted as integer
            ha = 'left',   # horizontal alignment
            va = 'center')  # vertical alignment
sns.despine()  # Remove the top and right spines
plt.tight_layout()  # Adjust layout to not cut off labels
# save to descriptive folder
plt.savefig('../../figures/publication_impact/top_biobanks_mentions.pdf')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_cohorts,
    x='citations',
    y='biobank',
    palette='coolwarm',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)

# Add labels and title for clarity
plt.xlabel('Citations', fontsize=14, labelpad=15)
plt.ylabel('', fontsize=14, labelpad=15)
plt.title('Top 10 Biobanks (Citations)', fontsize=16, pad=20)
# Annotate bars with values
for p in ax.patches:
    width = p.get_width()  # get bar length
    ax.text(width + 10,       # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + half of bar width
            '{:1.0f}'.format(width),  # your value label, formatted as integer
            ha = 'left',   # horizontal alignment
            va = 'center')  # vertical alignment
sns.despine()  # Remove the top and right spines
plt.tight_layout()  # Adjust layout to not cut off labels
# save to descriptive folder
plt.savefig('../../figures/publication_impact/top_biobanks_citations.pdf')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_authors_mentions,
    x='id',
    y='author_name',
    palette='coolwarm',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
# Add labels and title for clarity
plt.xlabel('Biobank Publications', fontsize=14, labelpad=15)
plt.ylabel('', fontsize=14, labelpad=15)
plt.title('Top 10 Authors', fontsize=16, pad=20)
# Annotate bars with values
for p in ax.patches:
    width = p.get_width()  # get bar length
    ax.text(width + 10,       # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + half of bar width
            '{:1.0f}'.format(width),  # your value label, formatted as integer
            ha = 'left',   # horizontal alignment
            va = 'center')  # vertical alignment
sns.despine()  # Remove the top and right spines
plt.tight_layout()  # Adjust layout to not cut off labels
# save to descriptive folder
plt.savefig('../../figures/publication_impact/top_authors_mentions.pdf')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_corresponding_mentions,
    x='id',
    y='author_name',
    palette='coolwarm',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
# Add labels and title for clarity
plt.xlabel('Biobank Publications', fontsize=14, labelpad=15)
plt.ylabel('', fontsize=14, labelpad=15)
plt.title('Top 10 Corresponding Authors', fontsize=16, pad=20)
# Annotate bars with values
for p in ax.patches:
    width = p.get_width()  # get bar length
    ax.text(width + 1,       # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + half of bar width
            '{:1.0f}'.format(width),  # your value label, formatted as integer
            ha = 'left',   # horizontal alignment
            va = 'center')  # vertical alignment
sns.despine()  # Remove the top and right spines
plt.tight_layout()  # Adjust layout to not cut off labels
# save to descriptive folder
plt.savefig('../../figures/publication_impact/top_corresponding_mentions.pdf')

plt.figure(figsize=(10, 6))
# Create the barplot with enhancements
ax = sns.barplot(
    data=top_journals,
    x='citations_count',
    y='journal',
    palette='coolwarm',  # Use a thematic color palette
    linewidth=0.7,
    edgecolor='.2',
    width=0.8  # Adjust the width of the bars
)
# Add labels and title for clarity
plt.xlabel('Citations from Biobank Papers', fontsize=14, labelpad=15)
plt.ylabel('', fontsize=14, labelpad=15)
plt.title('Top 10 Journals (Citations)', fontsize=16, pad=20)
# Annotate bars with values
for p in ax.patches:
    width = p.get_width()  # get bar length
    ax.text(width + 1,       # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + half of bar width
            '{:1.0f}'.format(width),  # your value label, formatted as integer
            ha = 'left',   # horizontal alignment
            va = 'center')  # vertical alignment
sns.despine()  # Remove the top and right spines
plt.tight_layout()  # Adjust layout to not cut off labels
# save to descriptive folder
plt.savefig('../../figures/publication_impact/top_journals_citations.pdf')
