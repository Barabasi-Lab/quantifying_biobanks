import pandas as pd
import numpy as np
import spacy
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from adjustText import adjust_text
from tqdm import tqdm
import itertools
sns.set_context("notebook", font_scale=1.2)
sns.set_style("whitegrid")

# import papers from expansions/database
papers = pd.read_json('../../../data/expansion/database/mentions/papers.json', lines=True)
# read cohort_papers
cohort_papers = pd.read_csv('../../../data/expansion/cohort_papers.csv')
papers = papers.merge(cohort_papers[['id', 'cohort_name_lower']], on='id', how='left')
cohorts = papers.groupby('cohort_name_lower').id.nunique().rename('papers').sort_values(ascending=False).reset_index()
cohorts10 = cohorts[cohorts.papers >= 10]
papers.head()
hrcs = papers.explode('hrcs_hc')
# create a dataframe with the count of papers in each hrcs_hc category per cohort
cohort_hrcs = hrcs.groupby(['cohort_name_lower', 'hrcs_hc']).id.nunique().rename('papers').reset_index()
# unstack hrcs_hc
cohort_hrcs = cohort_hrcs.pivot(index='cohort_name_lower', columns='hrcs_hc', values='papers').fillna(0).reset_index()
# get main hrcs_hc per cohort
cohort_hrcs['main_hrcs_hc'] = cohort_hrcs.iloc[:, 1:].idxmax(axis=1)
cohort_hrcs.to_csv('../../../data/expansion/database/cohort_impact/hrcs_impact.csv', index=False)

hrcs_cols = cohort_hrcs.columns[1:-1]


hrcs.groupby('hrcs_hc').id.nunique().sort_values(ascending=False).head(20)

rcdc = papers.explode('rcdc').fillna('NA')
# count number of unicque ids per year and rcdc in papers
rcdc_year = rcdc.groupby(['year', 'rcdc']).id.nunique().rename('papers').reset_index()
# drop NA
rcdc_year = rcdc_year[rcdc_year.rcdc != 'NA']

rcdc['vaccine'] = rcdc.rcdc.apply(lambda x: True if 'vaccine' in x.lower() else False)
rcdc['minority_health'] = rcdc.rcdc.apply(lambda x: True if ('minority' in x.lower() or 'minorities' in x.lower()) else False)
rcdc['rare_disease'] = rcdc.rcdc.apply(lambda x: True if 'rare' in x.lower() else False)
rcdc['women_health'] = rcdc.rcdc.apply(lambda x: True if 'women' in x.lower() else False)
rcdc['social_determinants'] = rcdc.rcdc.apply(lambda x: True if ('social' in x.lower() or 'disparities' in x.lower()) else False)

social = rcdc[rcdc.social_determinants].groupby('cohort_name_lower').id.nunique().rename('social_determinants').sort_values(ascending=False).reset_index()
women_health = rcdc[rcdc['women_health']].groupby('cohort_name_lower').id.nunique().rename('women_health').sort_values(ascending=False).reset_index()
vaccines = rcdc[rcdc.vaccine].groupby('cohort_name_lower').id.nunique().rename('vaccines').sort_values(ascending=False).reset_index()
minority_health = rcdc[rcdc.minority_health].groupby('cohort_name_lower').id.nunique().rename('minority_health').sort_values(ascending=False).reset_index()
rare_disease = rcdc[rcdc.rare_disease].groupby('cohort_name_lower').id.nunique().rename('rare_disease').sort_values(ascending=False).reset_index()

cohorts = cohorts.merge(social, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(women_health, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(vaccines, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(minority_health, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(rare_disease, on='cohort_name_lower', how='left')
cohorts.to_csv('../../../data/expansion/database/cohort_impact/rcdc_impact.csv', index=False)

# read rcdc_funding_categories.xlsx from data/database/meta
rcdc_funding = pd.read_excel('../../../data/database/meta/rcdc_funding_categories.xlsx', skiprows=2, skipfooter=48)
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
rcdc_mean = rcdc_mean[rcdc_mean['mean'] > 500]
# make seaborn scatterplot x to be mean and y to be cohort_papers
with sns.plotting_context("notebook", font_scale=1.2):
    plt.figure(figsize=(10, 10))

    # Create a scatter plot
    g = sns.scatterplot(data=rcdc_mean, x='mean', y='cohort_papers', s=100, color='royalblue', edgecolor='black', alpha=0.3)

    # Set labels and title with improved aesthetics
    g.set_xlabel('Mean Funding per RCDC Category (Million USD)', fontsize=14, weight='bold')
    g.set_ylabel('Number of Cohort Papers on RCDC Category', fontsize=14, weight='bold')
    g.set_title('Funding per RCDC Category vs Number of Cohort Papers', fontsize=16, weight='bold')

    # Identify outliers - you may need to adjust this based on your data
    # Here, we're considering points with 'mean' value greater than a threshold as outliers
    slope, intercept = np.polyfit(rcdc_mean['mean'], rcdc_mean['cohort_papers'], 1)
    x_vals = np.array(plt.gca().get_xlim())
    y_vals = intercept + slope * x_vals
    rcdc_mean['predicted'] = slope * rcdc_mean['mean'] + intercept
    rcdc_mean['residual'] = np.abs(rcdc_mean['cohort_papers'] - rcdc_mean['predicted'])

    # Identify the top 5% points with the largest residuals
    outliers = rcdc_mean.nlargest(int(len(rcdc_mean) * 0.22), 'residual')

    # Prepare for annotation adjustments
    texts = []
    for i, row in outliers.iterrows():
        texts.append(plt.text(row['mean'], row['cohort_papers'], row['rcdc'], ha='center', fontdict={'size': 12, 'weight': 'bold'}))

    # Use adjust_text to prevent overlap, adjust the position of texts
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black'))

    # Plot the linear fit line
    plt.plot(x_vals, y_vals, '--', color='black', linewidth=0.5, label='Linear Fit')


    # Improve layout to ensure everything fits without overlapping
    plt.tight_layout()

    # Show the plot
    plt.show()
    
with sns.plotting_context('notebook', font_scale=1.2):
    plt.figure(figsize=(10, 10))
    slope, intercept = np.polyfit(rcdc_mean['mean'], rcdc_mean['cohort_papers'], 1)

    # Calculate the expected number of papers based on the regression line
    rcdc_mean['expected'] = slope * rcdc_mean['mean'] + intercept

    # Calculate the difference between the actual and expected number of papers
    rcdc_mean['difference'] = rcdc_mean['cohort_papers'] - rcdc_mean['expected']

    # Sort the categories by difference to find the top 10 underfunded (negative difference) and overfunded (positive difference)
    top_underfunded = rcdc_mean.sort_values(by='difference').head(10)
    top_overfunded = rcdc_mean.sort_values(by='difference', ascending=False).head(10)

    # Combine the top underfunded and overfunded categories
    top_categories = pd.concat([top_underfunded, top_overfunded])

    # Plot a barplot showing the difference for these categories
    plt.figure(figsize=(12, 8))
    barplot = sns.barplot(data=top_categories, x='difference', y='rcdc', hue='difference', palette='coolwarm_r', dodge=False)

    # Set labels and title
    barplot.set_xlabel('Difference between Actual and Expected Number of Papers', fontsize=14, weight='bold')
    barplot.set_ylabel('RCDC Category', fontsize=14, weight='bold')
    barplot.set_title('Top 10 Under and Over Represented Categories in Cohort Papers (2010 - 2022)', fontsize=16, weight='bold')

    # Color bar based on positive or negative difference
    barplot.legend_.remove()  # Remove the legend as we're coloring based on the value

    # Improve layout
    plt.tight_layout()

    # Show the plot
    plt.show()

# do a co mention network
cohort2papers = dict(cohort_papers[cohort_papers['cohort_name_lower'].isin(cohorts['cohort_name_lower'])].groupby('cohort_name_lower').id.apply(set))
cohort_names = list(cohort2papers.keys())
combinations = list(itertools.combinations(cohort_names, 2))
weighted_edges = []
for a, b in combinations:
    weight = len(cohort2papers[a].intersection(cohort2papers[b]))
    if weight > 0:
        weighted_edges.append((a, b, weight))
G = nx.Graph()
G.add_weighted_edges_from(weighted_edges)
# get cohort2main_hrcs_hc
cohort2main_hrcs_hc = dict(cohort_hrcs[['cohort_name_lower', 'main_hrcs_hc']].values)
# get number of paper by hrsc_hc and cohort
cohort2hrcs = dict(cohort_hrcs.set_index('cohort_name_lower').iloc[:, :-1].T.to_dict('list'))
hrcs_cols2index = {col: i for i, col in enumerate(cohort_hrcs.columns[1:-1])}

pcountries = papers.explode('research_org_countries').dropna(subset=['research_org_countries'])
cohort_country = pcountries.groupby('cohort_name_lower').research_org_countries.apply(lambda x: x.value_counts(normalize=True)).reset_index()
cohort_country.columns = ['cohort_name_lower', 'country', 'proportion']
cohort_country.to_csv('../../../data/expansion/database/cohort_impact/country_impact.csv', index=False)

outlier = cohort_country.groupby('cohort_name_lower').proportion.apply(lambda x: x.mean() + 2 * x.std()).rename('outlier_value').reset_index().dropna()

main_country =pcountries.groupby('cohort_name_lower').research_org_countries.apply(lambda x: x.value_counts(normalize=True).head(1)).reset_index()
main_country.columns = ['cohort_name_lower', 'country', 'proportion']
main_country = main_country.merge(outlier, on='cohort_name_lower')
main_country.loc[(main_country['proportion'] < main_country['outlier_value']) & (main_country['proportion'] < 0.5), 'country'] = 'International'
main_country.loc[(main_country['proportion'] < 0.3), 'country'] = 'International'
cohort2country = dict(zip(main_country['cohort_name_lower'], main_country['country']))

cohort_hrcs = hrcs.groupby(['cohort_name_lower']).hrcs_hc.value_counts(normalize=True).rename('propotion').reset_index()
outlier = cohort_hrcs.groupby('cohort_name_lower').propotion.apply(lambda x: x.mean() + 2 * x.std()).rename('outlier_value').reset_index().dropna()
main_hrcs = hrcs.groupby('cohort_name_lower').hrcs_hc.apply(lambda x: x.value_counts(normalize=True).head(1)).reset_index()
main_hrcs.columns = ['cohort_name_lower', 'hrcs_hc', 'proportion']
main_hrcs = main_hrcs.merge(outlier, on='cohort_name_lower')
main_hrcs.loc[(main_hrcs['proportion'] < main_hrcs['outlier_value']) & (main_hrcs['proportion'] < 0.5), 'hrcs_hc'] = 'General'
main_hrcs.loc[(main_hrcs['proportion'] < 0.3), 'hrcs_hc'] = 'General'
cohort2hrcs = dict(zip(main_hrcs['cohort_name_lower'], main_hrcs['hrcs_hc']))

cohorts['label'] = cohorts['cohort_name_lower'].apply(lambda x: x.replace('the ', ''))
cohort2label = cohorts.set_index('cohort_name_lower').label.to_dict()
# add node attributes
nx.set_node_attributes(G, cohort2country, 'country')
nx.set_node_attributes(G, cohort2hrcs, 'main_hrcs_hc')
nx.set_node_attributes(G, cohort2label, 'name')


# save graph
nx.write_graphml(G, '../../../data/networks/cohort_co_mentions.graphml')

# do a co-citation network
def get_citations(C):
    cits = set()
    for P in C:
        for c in P:
            cits.add(c['id'])
    return cits
            

cohort2citations = dict(papers.groupby('cohort_name_lower').citations.apply(lambda x: list(x)).apply(get_citations))
cohort2citations = {k: v for k, v in cohort2citations.items() if len(v) > 100}
weighted_edges = []
for a, b in tqdm(combinations):
    if a not in cohort2citations or b not in cohort2citations:
        continue
    inter = cohort2citations[a].intersection(cohort2citations[b])
    if len(inter) > 0:
        weight = len(inter) / max(len(cohort2citations[a]), len(cohort2citations[b]))
        if weight > 0.01:
            weighted_edges.append((a, b, weight))

G = nx.Graph()
G.add_weighted_edges_from(weighted_edges)
# add node attributes
nx.set_node_attributes(G, cohort2hrcs, 'main_hrcs_hc')
nx.set_node_attributes(G, cohort2country, 'country')
nx.set_node_attributes(G, cohort2label, 'name')

nx.write_graphml(G, '../../../data/networks/cohort_co_citations.graphml')

# Diseases, Vaccines and & Drug development, Rare diseases
# Diseases start with C
# Vaccines start with E05.952 or D20.215.894
# Drugs start with E05.290 or D26
# Rare Diseases start with C23.550.291.906 or C23.550.291.968 or C23.550.291.890
mesh = pd.read_csv('../../../data/database/meta/mesh.csv')
mesh['disease'] = mesh['tree_number'].apply(lambda x: True if x.startswith('C') else False)
mesh['vaccine'] = mesh['tree_number'].apply(lambda x: True if x.startswith('E05.952') or x.startswith('D20.215.894') else False)
mesh['drug'] = mesh['tree_number'].apply(lambda x: True if x.startswith('E05.290') or x.startswith('D26') else False)
mesh['rare_disease'] = mesh['tree_number'].apply(lambda x: True if x.startswith('C23.550.291.906')
                                                 or x.startswith('C23.550.291.968') or x.startswith('C23.550.291.890') else False)


pmesh = papers[['id', 'cohort_name_lower', 'mesh_ids']].explode('mesh_ids').dropna(subset=['mesh_ids'])
# rename mesh_ids to mesh_id
pmesh = pmesh.rename(columns={'mesh_ids': 'mesh_id'})
mesh_papers = pmesh.groupby('cohort_name_lower').id.nunique().rename('papers').reset_index()

pmesh_vaccine = pmesh.merge(mesh[mesh['vaccine']])
pmesh_drug = pmesh.merge(mesh[mesh['drug']])
pmesh_rare_disease = pmesh.merge(mesh[mesh['rare_disease']])

cohort_vaccine = pmesh_vaccine.groupby('cohort_name_lower').id.nunique().rename('vaccine_papers').reset_index()
cohort_vaccine = mesh_papers.merge(cohort_vaccine, on='cohort_name_lower', how='left').fillna(0)
# sort by vaccine_papers
cohort_vaccine = cohort_vaccine.sort_values('vaccine_papers', ascending=False)

cohort_drug = pmesh_drug.groupby('cohort_name_lower').id.nunique().rename('drug_papers').reset_index()
cohort_vaccine = cohort_vaccine.merge(cohort_drug, on='cohort_name_lower', how='left').fillna(0)

cohort_rares = pmesh_rare_disease.groupby('cohort_name_lower').id.nunique().rename('rare_disease_papers').reset_index()
cohort_vaccine = cohort_vaccine.merge(cohort_rares, on='cohort_name_lower', how='left').fillna(0)

# save to csv
cohort_vaccine.to_csv('../../../data/expansion/database/cohort_impact/vaccine_drug_impact.csv', index=False)

mesh = mesh[mesh['disease']]
mesh['main_level'] = mesh['tree_number'].apply(lambda x: x.split('.')[0])
main_level = mesh[mesh['tree_number'].apply(lambda x: len(x.split('.')) == 1)][['main_level', 'mesh_name']].rename(columns={'mesh_name': 'main_mesh_name'})
pmesh = pmesh.merge(mesh)
pmesh = pmesh.merge(main_level, on='main_level')

cohort_mesh = pmesh.groupby(['cohort_name_lower', 'mesh_name', 'tree_number', 'main_level', 'main_mesh_name']).id.nunique().rename('papers').reset_index()
cohort_mesh.to_csv('../../../data/expansion/database/cohort_impact/mesh_impact.csv', index=False)
