import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import plotly.express as px

sns.set_theme(style='white')

papers = pd.read_json('../../../data/expansion/database/authors/paper_authors.json', lines=True)
cohort_papers = pd.read_csv('../../../data/expansion/cohort_papers.csv')
papers['authors'].iloc[0]
def get_corresponding_authors(authors):
    if authors is None:
        return []
    return [author['researcher_id'] for author in authors if author['corresponding'] and 'researcher_id' in author]

def get_name(authors):
    for author in authors:
        if author['corresponding']:
            if 'first_name' not in author:
                if 'last_name' not in author:
                    return np.nan
                return author['last_name']
            return author['first_name'] + ' ' + author['last_name']

def get_corresponding_author_grid_ids(authors):
    for author in authors:
        if author['corresponding']:
            if not author['grid_ids']:
                return np.nan
            return author['grid_ids']

papers['corresponding_authors'] = papers['authors'].apply(get_corresponding_authors)
papers['num_corresponding_authors'] = papers['corresponding_authors'].apply(len)
# get only papers with one corresponding author
papers = papers[papers['num_corresponding_authors'].between(1, 10)]
# rename corresponding author to corresponding_author_id
papers = papers.rename(columns={'corresponding_authors': 'corresponding_author_id'})
papers = papers.explode('corresponding_author_id')


corr = papers.copy()
del corr['authors']
cohort_corr = cohort_papers.merge(corr, on='id')
cohorts = cohort_corr.groupby('cohort_name_lower').id.nunique().rename('papers').sort_values(ascending=False).reset_index()
cohorts = cohorts.merge(cohort_corr.groupby('cohort_name_lower').corresponding_author_id.nunique().rename('unique_corresponding_authors').reset_index(), on='cohort_name_lower', how='left')

# do a scatter plot in plotly with x=papers, y=unique_corresponding_authors hover=cohort_name_lower
fig = px.scatter(cohorts, x='papers', y='unique_corresponding_authors', hover_name='cohort_name_lower')
# set axis in log scale
fig.update_xaxes(type='log')
fig.update_yaxes(type='log')
fig.show()

# the same plot in seaborn
with sns.plotting_context('notebook', font_scale=1.2):
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.scatterplot(data=cohorts, x='papers', y='unique_corresponding_authors', ax=ax)
    # add line with slope 1
    x = np.linspace(1, cohorts['papers'].max(), 100)
    sns.lineplot(x=x, y=x, ax=ax, color='black', linestyle='--')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Number of papers')
    ax.set_ylabel('Number of unique corresponding authors')
    plt.show()

with sns.plotting_context('notebook', font_scale=1.5):
    # Create a larger, more aesthetically pleasing plot
    fig, ax = plt.subplots(figsize=(14, 10))
    # Use a sophisticated color palette and increase point size for better visibility
    scatter = sns.scatterplot(data=cohorts, x='papers', y='unique_corresponding_authors', ax=ax,
                            palette='Spectral', s=120, edgecolor='k', linewidth=0.3, alpha=0.9)

    # Add line with slope 1, with a subtle drop shadow for depth
    x = np.linspace(1, cohorts['papers'].max(), 100)
    line = sns.lineplot(x=x, y=x, ax=ax, color='gray', linestyle='--', linewidth=2)
    line.set_zorder(1)  # Put the line below the scatter points

    # Add drop shadow to line for depth
    xx, yy = line.get_lines()[-1].get_data()
    shadow = Line2D(xx, yy, color='lightgray', linewidth=3, linestyle='--')
    shadow.set_zorder(line.get_zorder() - 1)  # Put the shadow just below the line
    ax.add_line(shadow)

    # Log scale for better distribution
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Customizing the tick labels for log scale for clarity
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())
    ax.tick_params(axis='both', which='major', labelsize=16)

    # Labels and title with increased font sizes and padding for clarity
    ax.set_xlabel('Number of Papers', fontsize=22, labelpad=20)
    ax.set_ylabel('Number of Unique Corresponding Authors', fontsize=22, labelpad=20)
    ax.set_title('Papers vs. Unique Corresponding Authors Relationship', fontsize=24, pad=20)

    # Minimalist improvements: remove top and right spines
    sns.despine(trim=True, offset=10)

    # Legend for clarity
    legend_labels = ['Equality Line', 'Cohorts']
    ax.legend(handles=ax.lines[:1] + [Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10)],
            labels=legend_labels, fontsize=18, frameon=False)

    # Show plot
    plt.tight_layout()
    plt.show()

top = cohort_corr.groupby('cohort_name_lower').corresponding_author_id.apply(lambda x: x.value_counts(normalize=True).head(1)).rename('prop_of_papers_by_top_author').reset_index()
top.columns = ['cohort_name_lower', 'top_author', 'prop_of_papers_by_top_author']
cohorts = cohorts.merge(top, on='cohort_name_lower', how='left')
top = cohort_corr.groupby('cohort_name_lower').corresponding_author_id.apply(lambda x: x.value_counts().head(1)).rename('prop_of_papers_by_top_author').reset_index()
top.columns = ['cohort_name_lower', 'top_author', 'num_of_papers_by_top_author']
del top['top_author']
cohorts = cohorts.merge(top, on='cohort_name_lower', how='left')
cohorts['per_of_papers_by_top_author'] = cohorts['prop_of_papers_by_top_author'] * 100

# do a scatter plot in plotly with x=papers, y=prop_of_papers_by_top_author hover=cohort_name_lower
fig = px.scatter(cohorts[cohorts['papers'] > 10], x='papers', y='num_of_papers_by_top_author', hover_name='cohort_name_lower')
# set axis in log scale
fig.update_xaxes(type='log')
fig.update_yaxes(type='log')

with sns.plotting_context('notebook', font_scale=1.5):
    # Create a larger, more aesthetically pleasing plot
    fig, ax = plt.subplots(figsize=(14, 10))
    # Use a sophisticated color palette and increase point size for better visibility
    scatter = sns.scatterplot(data=cohorts, x='papers', y='per_of_papers_by_top_author', ax=ax,
                            palette='Spectral', s=120, edgecolor='k', linewidth=0.3, alpha=0.9)

    # Add line with slope 1, with a subtle drop shadow for depth
    x = np.linspace(1, cohorts['papers'].max(), 100)
    line = sns.lineplot(x=x, y=-x, ax=ax, color='gray', linestyle='--', linewidth=2)
    line.set_zorder(1)  # Put the line below the scatter points

    # Add drop shadow to line for depth
    xx, yy = line.get_lines()[-1].get_data()
    shadow = Line2D(xx, yy, color='lightgray', linewidth=3, linestyle='--')
    shadow.set_zorder(line.get_zorder() - 1)  # Put the shadow just below the line
    ax.add_line(shadow)

    # Log scale for better distribution
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Customizing the tick labels for log scale for clarity
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())
    ax.tick_params(axis='both', which='major', labelsize=16)

    # Labels and title with increased font sizes and padding for clarity
    ax.set_xlabel('Number of Papers', fontsize=22, labelpad=20)
    ax.set_ylabel('Percentage (%)', fontsize=22, labelpad=20)
    ax.set_title('Percentage of Total Papers by Top Corresponding Author', fontsize=24, pad=20)

    # Minimalist improvements: remove top and right spines
    sns.despine(trim=True, offset=10)

    # Legend for clarity
    legend_labels = ['Cohorts']
    ax.legend(handles=[Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10)],
            labels=legend_labels, fontsize=18, frameon=False)

    # Show plot
    plt.tight_layout()
    plt.show()

papers['corresponding_name'] = papers['authors'].apply(get_name)
names = papers[['corresponding_author_id', 'corresponding_name']].drop_duplicates(subset=['corresponding_author_id'])
names.columns = ['top_author', 'top_author_name']
cohorts = cohorts.merge(names, on='top_author', how='left')
cohorts.to_csv('../../../data/expansion/database/cohort_impact/corresponding_authors_impact.csv', index=False)

