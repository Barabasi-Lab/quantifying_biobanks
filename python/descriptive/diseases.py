import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
from adjustText import adjust_text
import networkx as nx
from scipy.stats import pearsonr

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

papers = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)

rcdc = papers.explode('rcdc').fillna('NA')
# count number of unicque ids per year and rcdc in papers
rcdc_year = rcdc.groupby(['year', 'rcdc']).id.nunique().rename('papers').reset_index()
# drop NA
rcdc_year = rcdc_year[rcdc_year.rcdc != 'NA']

mesh = pd.read_csv('../../data/database/meta/mesh.csv')
# replace name tree_number with sec_tree_number
mesh.columns = ['mesh_id', 'mesh_name', 'sec_tree_number']

mesh_impact = pd.read_csv('../../data/expansion/database/cohort_impact/mesh_impact.csv')
mesh_impact['sec_tree_number'] = mesh_impact['tree_number'].apply(lambda x: '.'.join(x.split('.')[:2]))
mesh_impact['level'] = mesh_impact['tree_number'].apply(lambda x: len(x.split('.')))
sec_mesh = mesh_impact[mesh_impact['level'] >= 2]


mesh_colors = pd.read_csv('../../data/expansion/database/descriptive/colors_disease_mesh.csv')
mesh_colors.columns = ['color', 'main_mesh_name']
# order mesh_impact by papers in descending order
mesh_impact = mesh_impact.sort_values('papers', ascending=False)

mesh_impact = mesh_impact.drop('tree_number', axis=1).drop_duplicates()

main_mesh = mesh_impact.groupby(['cohort_name_lower', 'main_mesh_name']).papers.sum().rename('main_mesh_papers').reset_index()
# order main_mesh by main_mesh_papers in descending order
main_mesh = main_mesh.sort_values('main_mesh_papers', ascending=False)
main_mesh = main_mesh.drop_duplicates(subset=['cohort_name_lower'])
# remove Otorhinolaryngologic Diseases and Occupational Diseases
main_mesh = main_mesh[~main_mesh['main_mesh_name'].isin(['Animal Diseases'])]

# print sns palette with color column
sns.palplot(mesh_colors['color'])
pal = dict(zip(mesh_colors['main_mesh_name'], mesh_colors['color']))
# get desc order of main_mesh_name
order = main_mesh['main_mesh_name'].value_counts().index

# plot barplot of value_counts of main_mesh_name in main_mesh table
plt.figure(figsize=(14, 8))
ax = sns.countplot(y=main_mesh['main_mesh_name'], palette=pal, order=order, edgecolor='black')
plt.title('Main MeSH Disease Category of Biobanks')
plt.xlabel('Number of Biobanks')
plt.ylabel('')
# Adjust bar width
for bar in ax.patches:
    bar.set_height(0.8)

# Add grid
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)

# Remove unnecessary spines
sns.despine(top=True, right=True, left=False, bottom=False)

# Add value labels to each bar
for p in ax.patches:
    width = p.get_width()  # get bar length
    ax.text(width + 3,       # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + half of bar width
            '{:1.0f}'.format(width),  # your value label, formatted as integer
            ha = 'left',   # horizontal alignment
            va = 'center')  # vertical alignment

plt.tight_layout()
# save to descriptive folder as pdf
plt.savefig('../../figures/diseases/biobank_main_diseases.pdf')

sub_disease = main_mesh.merge(mesh_impact[['cohort_name_lower', 'main_mesh_name', 'mesh_name', 'papers']], on=['cohort_name_lower', 'main_mesh_name'])
sub_disease = sub_disease[sub_disease['main_mesh_name'] != sub_disease['mesh_name']]
# order by papers in descending order
sub_disease = sub_disease.sort_values('papers', ascending=False)
# drop duplicates by cohort_name_lower
sub_disease = sub_disease[sub_disease['main_mesh_name'] != sub_disease['mesh_name']].drop_duplicates(subset=['cohort_name_lower'])




# make function to remove everything after comma from string
def remove_after_comma(string):
    return string.split(',')[0]


def create_grouped_treemap(df, color_dict):
    # Sort the DataFrame first by 'main_mesh_name' and then by 'counts' within each 'main_mesh_name'
    df_sorted = df.sort_values(by=['main_mesh_name', 'counts'], ascending=[True, False])

    # Generate sizes for the treemap
    sizes = df_sorted['counts'].values

    # Generate labels for the treemap
    nl = '\n'
    labels = [f"{nl.join(remove_after_comma(name).split())}{nl}({count})" for name, count in zip(df_sorted['mesh_name'], df_sorted['counts'])]

    # Create a color list based on the sorted DataFrame
    colors = df_sorted['main_mesh_name'].map(color_dict).values

    # Plot the treemap
    plt.figure(figsize=(25, 20))
    plt.title('Main Diseases by Category (Number of Biobanks)', fontsize=24, weight='bold')
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.7, pad=False,
                  text_kwargs={'wrap': True, 'fontsize': 14, 'fontweight': 'bold', 'color': 'black'})
    plt.axis('off')
    # return figure
    return plt.gcf()

top5_main_mesh = sub_disease['main_mesh_name'].value_counts().nlargest(20).index
# Count occurrences of 'mesh_name' within each 'main_mesh_name'
sub_disease['mesh_name'] = sub_disease['mesh_name'].apply(remove_after_comma)
df_count = sub_disease[sub_disease.main_mesh_name.isin(top5_main_mesh)].groupby(['main_mesh_name', 'mesh_name']).size().reset_index(name='counts')
df_count = df_count[df_count['counts'] >= 10]

# Sort and select the top 5 'mesh_name' diseases by count within each 'main_mesh_name'
df_top5 = df_count.groupby('main_mesh_name').apply(lambda x: x.nlargest(20, 'counts')).reset_index(drop=True)
fig = create_grouped_treemap(df_top5, pal)
# save as pdf
fig.savefig('../../figures/diseases/biobank_sub_diseases.pdf')


# read rcdc_funding_categories.xlsx from data/database/meta
rcdc_funding = pd.read_excel('../../data/database/meta/rcdc_funding_categories.xlsx', skiprows=2, skipfooter=48)
# drop columns with "ARRA" on their names
rcdc_funding = rcdc_funding[rcdc_funding.columns.drop(list(rcdc_funding.filter(regex='ARRA')))]
# replace + with NaN
rcdc_funding = rcdc_funding.replace('+', pd.NA)
# replace * with NaN
rcdc_funding = rcdc_funding.replace('*', pd.NA)
# drop last 4 columns
rcdc_funding = rcdc_funding.iloc[:, :-4]
# replace name of first column to rcdc
rcdc_funding.columns = ['rcdc'] + list(rcdc_funding.columns[1:])
# make all columns except the first one numeric
rcdc_funding[rcdc_funding.columns[1:]] = rcdc_funding[rcdc_funding.columns[1:]].apply(pd.to_numeric, errors='coerce')
# remove numbers from column rcdc
rcdc_funding['rcdc'] = rcdc_funding['rcdc'].str.replace(r'\d+', '')
# remove blank spaces from column rcdc
rcdc_funding['rcdc'] = rcdc_funding['rcdc'].str.strip()
# groupby rcdc and take the mean of the rest of the columns
rcdc_funding_mean = rcdc_funding.groupby('rcdc').mean().reset_index()
mean_per_rcdc = rcdc_funding_mean.mean(axis=1, skipna=True)
mean_per_rcdc = pd.DataFrame(mean_per_rcdc, columns=['mean'])
# merge by index with rcdc_funding_mean
rcdc_funding_mean = rcdc_funding_mean[['rcdc']].merge(mean_per_rcdc, left_index=True, right_index=True)
# replace 'NA' with pd.NA
rcdc_year = rcdc_year.replace('NA', pd.NA)
rcdc_mean = rcdc_year[rcdc_year.year.between(2008, 2022)].groupby('rcdc')['papers'].sum().rename('cohort_papers').reset_index()
rcdc_mean = rcdc_mean.merge(rcdc_funding_mean, on='rcdc')
rcdc_mean = rcdc_mean[rcdc_mean['mean'] > 1000]
# calculate p-values of pearson correlation between mean and cohort_papers
p_value = pearsonr(rcdc_mean['mean'], rcdc_mean['cohort_papers'])
# get rank of rcdc_mean by mean and cohort_papers
rcdc_mean['rank_mean'] = rcdc_mean['mean'].rank(ascending=False)
rcdc_mean['rank_papers'] = rcdc_mean['cohort_papers'].rank(ascending=False)

plt.figure(figsize=(10, 10))

# Create a scatter plot
g = sns.scatterplot(data=rcdc_mean, x='mean', y='cohort_papers', s=100, color='royalblue', edgecolor='black', alpha=0.3)

# Set labels and title with improved aesthetics
g.set_xlabel('Mean Funding per RCDC Category (Million USD)', fontsize=14, weight='bold')
g.set_ylabel('Number of Biobank Papers on RCDC Category', fontsize=14, weight='bold')
g.set_title('Funding per RCDC Category vs Number of Biobank Papers', fontsize=16, weight='bold')

# Identify outliers - you may need to adjust this based on your data
# Here, we're considering points with 'mean' value greater than a threshold as outliers
slope, intercept = np.polyfit(rcdc_mean['mean'], rcdc_mean['cohort_papers'], 1)
x_vals = np.array(plt.gca().get_xlim())
y_vals = intercept + slope * x_vals
rcdc_mean['predicted'] = slope * rcdc_mean['mean'] + intercept
rcdc_mean['residual'] = np.abs(rcdc_mean['cohort_papers'] - rcdc_mean['predicted'])
rcdc_mean['percentage'] = (rcdc_mean['cohort_papers'] - rcdc_mean['predicted']) / rcdc_mean['cohort_papers'] * 100

# Identify the top 5% points with the largest residuals
outliers = rcdc_mean.nlargest(int(len(rcdc_mean) * 0.22), 'residual')
out_mean = rcdc_mean.nlargest(10, 'mean')
out_papers = rcdc_mean.nlargest(15, 'cohort_papers')
outliers = pd.concat([outliers, out_mean, out_papers]).drop_duplicates()

# Prepare for annotation adjustments
texts = []
for i, row in outliers.iterrows():
    texts.append(plt.text(row['mean'], row['cohort_papers'], row['rcdc'], ha='center', fontdict={'size': 12, 'weight': 'bold'}))

# Use adjust_text to prevent overlap, adjust the position of texts
adjust_text(texts)

# start axis at 0
plt.xlim(0, plt.gca().get_xlim()[1])
plt.ylim(0, plt.gca().get_ylim()[1])

# Plot the linear fit line
plt.plot(x_vals, y_vals, '--', color='black', linewidth=0.5, label='Linear Fit')


# Improve layout to ensure everything fits without overlapping
plt.tight_layout()

# Remove unnecessary spines
sns.despine(top=True, right=True, left=False, bottom=False)
# save to descriptive folder as pdf
plt.savefig('../../figures/diseases/funding_vs_papers.pdf')


slope, intercept = np.polyfit(rcdc_mean['mean'], rcdc_mean['cohort_papers'], 1)

# Calculate the expected number of papers based on the regression line
rcdc_mean['expected'] = slope * rcdc_mean['mean'] + intercept

# Calculate the difference between the actual and expected number of papers
rcdc_mean['difference'] = rcdc_mean['cohort_papers'] - rcdc_mean['expected']

# Sort the categories by difference to find the top 10 underfunded (negative difference) and overfunded (positive difference)
top_underfunded = rcdc_mean.sort_values(by='percentage').head(10)
top_overfunded = rcdc_mean.sort_values(by='percentage', ascending=False).head(10)

# Combine the top underfunded and overfunded categories
top_categories = pd.concat([top_underfunded, top_overfunded])

# Plot a barplot showing the difference for these categories
plt.figure(figsize=(20, 8))
barplot = sns.barplot(data=top_categories, x='percentage', y='rcdc', hue='percentage', palette='coolwarm_r', dodge=False,
                      order=top_categories.sort_values('percentage')['rcdc'], edgecolor='black', linewidth=1.5)

# Set labels and title
barplot.set_xlabel('Difference between Actual and Expected Number of Papers (%)', fontsize=14, weight='bold')
barplot.set_ylabel('RCDC Category', fontsize=14, weight='bold')
barplot.set_title('Top 10 Under and Over Represented Categories in Biobank Papers (2010 - 2022)', fontsize=16, weight='bold')


# Color bar based on positive or negative difference
barplot.legend_.remove()  # Remove the legend as we're coloring based on the value
# Remove unnecessary spines
sns.despine(top=True, right=True, left=False, bottom=False)
# Improve layout
plt.tight_layout()
# save to descriptive folder as pdf
plt.savefig('../../figures/diseases/top_under_over_funded.pdf')

mesh_disease = mesh[mesh['sec_tree_number'].str.contains('C')].mesh_id.unique()
mesh_papers = papers.explode('mesh_ids').dropna(subset=['mesh_ids'])
# rename mesh_ids to mesh_id
mesh_papers.rename(columns={'mesh_ids': 'mesh_id'}, inplace=True)
mesh_papers = mesh_papers[mesh_papers['mesh_id'].isin(mesh_disease)]
mesh_papers = mesh_papers.merge(mesh[['mesh_id', 'mesh_name']], on='mesh_id')
# sort mesh_impact by papers in descending order
mesh_impact = mesh_impact.sort_values('papers', ascending=False)

# read co_citation network from data/networks/co_citations.graphml
G = nx.read_graphml('../../data/networks/co_citations.graphml')
# get nodes with mesh attribute equal to Neoplasms
nodes = [(n, d) for n, d in G.nodes(data=True) if 'mesh' in d]
nodes = [n for n, d in nodes if d['mesh'] == 'Neoplasms']

