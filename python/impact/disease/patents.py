import pandas as pd
import numpy as np
import plotly.express as px
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid", context='paper')
# show all columns
pd.set_option('display.max_columns', None)

THERAPEUTIC = 'A61P'
patent_main_areas = {
    'A': 'HUMAN NECESSITIES',
    'B': 'PERFORMING OPERATIONS; TRANSPORTING',
    'C': 'CHEMISTRY; METALLURGY',
    'D': 'TEXTILES; PAPER',
    'E': 'FIXED CONSTRUCTIONS',
    'F': 'MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING',
    'G': 'PHYSICS',
    'H': 'ELECTRICITY',
    'Y': 'GENERAL TAGGING OF NEW TECHNOLOGICAL DEVELOPMENTS',
    'Z': 'GENERAL TAGGING OF CROSS-SECTIONAL TECHNOLOGIES SPANNING OVER SEVERAL SECTIONS OF THE IPC'
}

patents = pd.read_json(
    '../../../data/expansion/database/mentions/patents.json', lines=True)
patents.head(10)
cpc_a = pd.read_csv(
    '../../../data/patent_classification/cpc_humans.tsv', sep='\t')
cpc_a.columns = ['cpc', 'level', 'description']

cpc_c = pd.read_csv(
    '../../../data/patent_classification/cpc_chemistry.tsv', sep='\t')
cpc_c.columns = ['cpc', 'level', 'description']

cpc_g = pd.read_csv(
    '../../../data/patent_classification/cpc_physics.tsv', sep='\t')
cpc_g.columns = ['cpc', 'level', 'description']

cpc_y = pd.read_csv('../../../data/patent_classification/cpc_y.tsv', sep='\t')
cpc_y.columns = ['cpc', 'level', 'description']

cpc = pd.concat([cpc_a, cpc_c, cpc_g, cpc_y])
cpc['level'].fillna(-1, inplace=True)
cpc.head()
# read grid json from meta dir
grid = pd.read_json('../../../data/database/meta/grid.json', lines=True)
grid.rename(columns={'id': 'assignee_orgs'}, inplace=True)
grid = grid.explode('types')
# rename types by org_type
grid.rename(columns={'types': 'org_type'}, inplace=True)
# rename id to assignee_orgs
cohort_patents = pd.read_csv('../../../data/expansion/cohort_patents.csv')
patents.info()
cohorts = cohort_patents.groupby('cohort_name_lower')['id'].nunique().rename(
    'patents').sort_values(ascending=False).reset_index()

patent_class = patents.explode('cpc').merge(
    cpc[cpc['level'] == 0], how='left').dropna()
patent_class['root'] = patent_class['cpc'].str[:4]
patent_class = patent_class.merge(cpc[cpc['level'] == -1].drop(columns=['level']).rename(
    columns={'cpc': 'root', 'description': 'root_description'}), on='root', how='left')
patent_class[patent_class['description'].str.contains('Drugs')].groupby(
    ['cpc', 'description'])['id'].nunique().sort_values(ascending=False).reset_index().head(40)
# do main codes for different drugs
drug_codes = {
    'A61P35': 'chemotherapy',
    'A61P43': 'disease specific',
    'A61P9': 'cardiovascular',
    'A61P25': 'nervous_system',
    'A61P29': 'analgesics',
    'A61P3': 'metabolism',
    'A61P1': 'digestive',
    'A61P11': 'respiratory',
    'A61P37': 'immunological',
    'A61P17': 'dermatological',
    'A61P31': 'antiinfectives',
    'A61P21': 'muscular',
    'A61P15': 'genetical',
    'A61P67': 'blood',
    'A61P19': 'skeletal',
    'A61P27': 'sensorial',
    'A61P5': 'endocrine',
    'A61P13': 'urinary',
    'A61P41': 'surgical',

}
# add /00 to every key string
drug_codes = {k + '/00': v for k, v in drug_codes.items()}
patent_class['drug_type'] = patent_class['cpc'].map(drug_codes)
# save patent class to data/figures
patent_class.to_json('../../../data/figures/patent_class.json', orient='records', lines=True)
patent_class = patent_class.merge(cohort_patents, on='id')
# get drug_type of each cohort and add it to a column in cohorts
cohorts = cohorts.merge(patent_class[patent_class['drug_type'].notnull()].groupby(['cohort_name_lower'])['drug_type'].apply(
    lambda x: x.mode().iat[0]).rename('main_drug_type').reset_index(), how='left', on='cohort_name_lower')
# add total number of drug patents to each cohort
cohorts = cohorts.merge(patent_class[patent_class['drug_type'].notnull()].groupby(['cohort_name_lower'])[
                        'id'].nunique().rename('drug_patents').reset_index(), how='left', on='cohort_name_lower')
# get number of patents by main_drug_type of each cohort
cohorts = cohorts.merge(patent_class[patent_class['drug_type'].notnull()].groupby(['cohort_name_lower', 'drug_type'])['id'].nunique().rename(
    'main_drug_patents').reset_index().rename(columns={'drug_type': 'main_drug_type'}), how='left', on=['cohort_name_lower', 'main_drug_type'])
with sns.plotting_context('notebook', rc={'axes.grid': False}, font_scale=1.2):
    # Adjusted figure size for better aspect ratio
    fig, ax = plt.subplots(figsize=(12, 6))

    # Using hue for color variation and adjusting size scale
    g = sns.scatterplot(data=cohorts,
                        x=cohorts['drug_patents'],
                        y=cohorts['main_drug_patents'],
                        # Adjust size scale for better visualization
                        size='therapeutic', sizes=(20, 200),
                        palette='tab10',
                        ax=ax,
                        edgecolor='k', linewidth=0.5)  # Adding point borders for better visibility

    # Log scale for x-axis and linear scale for y-axis
    g.set_xscale('log')

    # Set meaningful labels and title
    g.set_xlabel('Total Drug Patents', fontsize=14)
    g.set_ylabel('Main Drug Patents', fontsize=14)
    g.set_title('Total and Main Drug Patents by Cohort', fontsize=16)

    # Improve readability
    sns.despine()  # Remove the top and right spines

    # Enhance the legend to be more informative
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles[1:], labels=labels[1:],
              title="Therapeutic Patents")

patent_class_u = patent_class.drop_duplicates(subset=['id', 'type'])
drugs = patent_class_u.groupby(['drug_type'])['id'].nunique().rename(
    'patents').sort_values(ascending=False).reset_index()


with sns.plotting_context('notebook', font_scale=1.2):
    # Adjusted figure size for better aspect ratio
    fig, ax = plt.subplots(figsize=(12, 7))

    # Use a diverse color palette and add bar borders
    g = sns.barplot(data=drugs, x='patents', y='drug_type',
                    ax=ax, palette='Purples_r', edgecolor='.2')

    # Set meaningful labels and title
    g.set_xlabel('Number of Patents')
    g.set_ylabel('')
    g.set_title('Number of Patents by Drug Type')

    # Improve readability
    sns.despine(left=True, bottom=True)  # Remove the top and right spines
    plt.grid(axis='x', color='gray', linestyle='--',
             linewidth=0.5)  # Add gridlines

    # Annotations (optional, depending on space and readability)
    for p in ax.patches:
        ax.annotate(f"{int(p.get_width())}",  # Annotate the bars
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    xytext=(5, 0),  # 5 points horizontal offset
                    textcoords='offset points',
                    ha='left', va='center')
    plt.tight_layout()
    plt.savefig('../../../figures/patent_impact/drug_types.pdf')

main_codes = {
    'A61P': 'therapeutic',
    # 'A61K': 'pharmaceutical',
    'G16B': 'information_technology',
    'C12N': 'biotechnology',
    'C07K': 'biotechnology',
    'A23V': 'food',
    'G01N': 'diagnostics',
    'G16H': 'information_technology',
    'G16Z': 'information_technology',
    'G06N': 'information_technology',
    'A61B': 'diagnostics',
    'A61Q': 'cosmetics',
    'A61M': 'medical_devices',
    'A61F': 'medical_devices',
    'A23L': 'food',
    'G06Q': 'information_technology',
    # 'C07D': 'pharmaceutical',
    'C12Y': 'biotechnology',
    # 'C07H': 'pharmaceutical',
    'G06T': 'information_technology',
    'G06F': 'information_technology',
    'C08B': 'biotechnology',
    'C12P': 'biotechnology',
    'G09B': 'information_technology',
    # 'C07C': 'pharmaceutical',
    'A61H': 'medical_devices',
    'C12Q': 'biotechnology',
    # 'C07J': 'pharmaceutical',
    'C40B': 'biotechnology',
}

patent_class['type'] = patent_class['root'].map(main_codes)

patent_class_u = patent_class.drop_duplicates(subset=['id', 'type'])
with sns.plotting_context('notebook', font_scale=1.2):
    # Adjusted figure size for better aspect ratio and readability
    fig, ax = plt.subplots(figsize=(12, 7))

    # Use a diverse color palette and order bars by count
    g = sns.countplot(data=patent_class_u, y='type', ax=ax,
                      palette='Purples_r',  # Using a visually appealing color palette
                      order=patent_class_u['type'].value_counts().index)  # Order bars by count

    # Set meaningful labels and title
    g.set_xlabel('Number of Patents')
    g.set_ylabel('')
    g.set_title('Distribution of Patents by Type')

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
    plt.savefig('../../../figures/patent_impact/patent_types.pdf')

cohorts = cohorts.merge(patent_class[patent_class['type'] == 'therapeutic'].groupby(['cohort_name_lower'])[
                        'id'].nunique().rename('therapeutic').sort_values(ascending=False).reset_index(), how='left', on='cohort_name_lower')
# information technology
cohorts = cohorts.merge(patent_class[patent_class['type'] == 'information_technology'].groupby(['cohort_name_lower'])[
                        'id'].nunique().rename('bioinformatics').sort_values(ascending=False).reset_index(), how='left', on='cohort_name_lower')
# pharmaceutical
cohorts = cohorts.merge(patent_class[patent_class['type'] == 'pharmaceutical'].groupby(['cohort_name_lower'])[
                        'id'].nunique().rename('pharmaceutical').sort_values(ascending=False).reset_index(), how='left', on='cohort_name_lower')
# biotechnology
cohorts = cohorts.merge(patent_class[patent_class['type'] == 'biotechnology'].groupby(['cohort_name_lower'])[
                        'id'].nunique().rename('biotechnology').sort_values(ascending=False).reset_index(), how='left', on='cohort_name_lower')
# diagnostics
cohorts = cohorts.merge(patent_class[patent_class['type'] == 'diagnostics'].groupby(['cohort_name_lower'])[
                        'id'].nunique().rename('diagnostics').sort_values(ascending=False).reset_index(), how='left', on='cohort_name_lower')
# food
cohorts = cohorts.merge(patent_class[patent_class['type'] == 'food'].groupby(['cohort_name_lower'])[
                        'id'].nunique().rename('food').sort_values(ascending=False).reset_index(), how='left', on='cohort_name_lower')


with sns.plotting_context('notebook', font_scale=1.2):
    # Adjusted figure size for better aspect ratio
    fig, ax = plt.subplots(figsize=(12, 6))

    # Using hue for color variation and adjusting size scale
    g = sns.scatterplot(data=cohorts,
                        x=cohorts['therapeutic'].div(cohorts['patents']),
                        y=cohorts['bioinformatics'].div(cohorts['patents']),
                        # Adjust size scale for better visualization
                        size='patents', sizes=(20, 200),
                        palette='tab10',
                        ax=ax,
                        edgecolor='k', linewidth=0.5)  # Adding point borders for better visibility

    # Log scale for x-axis and linear scale for y-axis
    g.set_xscale('log')

    # Set meaningful labels and title
    g.set_xlabel('Therapeutic Patents per Patent', fontsize=14)
    g.set_ylabel('Bioinformatics Patents per Patent', fontsize=14)
    g.set_title(
        'Comparison of Therapeutic and Bioinformatics Patents per Total Patents', fontsize=16)

    # Improve readability
    plt.grid(True, axis="x", ls="--", linewidth=0.5)  # Add gridlines
    sns.despine()  # Remove the top and right spines

    # Enhance the legend to be more informative
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles[1:], labels=labels[1:], title="Patents")


# Partnerships
grid = pd.read_json('../../../data/database/meta/grid.json', lines=True)
grid.rename(columns={'id': 'assignee_orgs'}, inplace=True)
patents_orgs = patents.explode('assignee_orgs').merge(
    grid[['assignee_orgs', 'name', 'country', 'org_type']], on='assignee_orgs', how='left').dropna()
patents.head()


parents = grid.explode('parent_ids').dropna()
# rename parent_ids to parent_org
parents.rename(columns={'parent_ids': 'parent_org'}, inplace=True)
parents = parents[['assignee_orgs', 'parent_org']].merge(
    grid[['assignee_orgs', 'name', 'country', 'types']], left_on='parent_org', right_on='assignee_orgs')
# rename assignee_orgs_x to assignee_orgs
parents.rename(columns={'assignee_orgs_x': 'assignee_orgs'}, inplace=True)
# remove assignee_orgs_y
parents.drop(columns='assignee_orgs_y', inplace=True)
# rename name country and types to parent_name parent_country and parent_type
parents.rename(columns={'name': 'parent_name',
               'country': 'parent_country', 'types': 'parent_type'}, inplace=True)
patents_parents = patents_orgs.merge(parents, on='assignee_orgs', how='left')
# if parent_name is null add name to parent_name
patents_parents['parent_name'] = patents_parents['parent_name'].fillna(
    patents_parents['name'])
# same with country and type
patents_parents['parent_country'] = patents_parents['parent_country'].fillna(
    patents_parents['country_y'])
patents_parents['parent_type'] = patents_parents['parent_type'].fillna(
    patents_parents['org_type'])
# explode parent_type
patents_parents = patents_parents.explode('parent_type')
parent_patents = patents_parents.groupby(['parent_name', 'parent_type'])[
    'id'].nunique().rename('patents').sort_values(ascending=False).reset_index()


partnerships = cohort_patents.merge(
    patents_parents[['id', 'parent_name', 'parent_type']], on='id')
part_n = partnerships.groupby(['cohort_name_lower'])['parent_name'].nunique(
).rename('partnerships').sort_values(ascending=False).reset_index()
educ_n = partnerships[partnerships['parent_type'] == 'Education'].groupby(['cohort_name_lower'])[
    'parent_name'].nunique().rename('education').sort_values(ascending=False).reset_index()
comp_n = partnerships[partnerships['parent_type'] == 'Company'].groupby(['cohort_name_lower'])[
    'parent_name'].nunique().rename('companies').sort_values(ascending=False).reset_index()
gov_n = partnerships[partnerships['parent_type'] == 'Government'].groupby(['cohort_name_lower'])[
    'parent_name'].nunique().rename('government').sort_values(ascending=False).reset_index()
health_n = partnerships[partnerships['parent_type'] == 'Healthcare'].groupby(['cohort_name_lower'])[
    'parent_name'].nunique().rename('healthcare').sort_values(ascending=False).reset_index()
nonfp_n = partnerships[partnerships['parent_type'] == 'Nonprofit'].groupby(['cohort_name_lower'])[
    'parent_name'].nunique().rename('nonprofit').sort_values(ascending=False).reset_index()
# merge all
cohorts = cohorts.merge(part_n, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(educ_n, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(comp_n, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(gov_n, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(health_n, on='cohort_name_lower', how='left')
cohorts = cohorts.merge(nonfp_n, on='cohort_name_lower', how='left')

# network of partnerships
parent_type_dict = dict(
    zip(parent_patents['parent_name'], parent_patents['parent_type']))
weighted_edges = partnerships.groupby(['cohort_name_lower', 'parent_name'])[
    'id'].nunique().rename('weight').reset_index()
G = nx.from_pandas_edgelist(
    weighted_edges, 'cohort_name_lower', 'parent_name', 'weight')
# add node attributes
for node in G.nodes:
    if node in cohorts['cohort_name_lower'].values:
        G.nodes[node]['type'] = 'cohort'
    else:
        G.nodes[node]['type'] = parent_type_dict[node]
# save in data/networks as graphml
nx.write_graphml(G, '../../../data/networks/patent_partnerships.graphml')
# do a projection of the graph
# get non cohort nodes
non_cohort = [
    node for node in G.nodes if node not in cohorts['cohort_name_lower'].values]
# get nodes with type cohort
cohort = [node for node in G.nodes if node in cohorts['cohort_name_lower'].values]
G_proj = nx.bipartite.weighted_projected_graph(G, cohort, ratio=False)
# remove edges with weight smaller than .2
edges = [(u, v) for (u, v, d) in G_proj.edges(data=True) if d['weight'] < 2]
G_proj.remove_edges_from(edges)
# get node attributes
# save in data/networks as graphml
nx.write_graphml(
    G_proj, '../../../data/networks/patent_partnerships_proj.graphml')

# line plots
patents_parents = patents_parents[(patents_parents['publication_year'].between(2000, 2022)) & (
    patents_parents['parent_type'].isin(['Company', 'Education', 'Government', 'Healthcare', 'Nonprofit']))]
gb_year = patents_parents.groupby(['publication_year', 'parent_type'])[
    'id'].nunique().reset_index()

with sns.plotting_context('notebook', font_scale=1.2):
    # Adjusted figure size for better visualization
    fig, ax = plt.subplots(figsize=(12, 7))

    # Line plot with a distinct color palette and line styles
    g = sns.lineplot(data=gb_year, x='publication_year', y='id', hue='parent_type', style='parent_type',
                     markers=True, dashes=False, palette='Set2', ax=ax)  # Using 'Set2' for better color contrast

    # Setting descriptive labels and title
    g.set_xlabel('Year', fontsize=14)
    g.set_ylabel('Number of Patents', fontsize=14)
    g.set_title('Annual Trend of Patents by Assignee Type (2000-2022)', fontsize=16)

    # Improving readability
    plt.grid(True, which='both', linestyle='--',
             linewidth=0.5)  # Adding gridlines
    sns.despine()  # Removing the top and right spines

    # Refining the legend
    g.legend(title='Assignee Type', bbox_to_anchor=(1.05, 1),
             loc='upper left')  # Moving the legend outside the plot

    # Optional: Annotate significant data points
    # for x, y, label in zip(data_points['x'], data_points['y'], data_points['label']):
    #     plt.text(x, y, label)
    fig.tight_layout()
    # save fig
    fig.savefig('../../../figures/patent_impact/patent_timeline.pdf')

top_companies = parent_patents[parent_patents['parent_type'] == 'Company'].head(10)
with sns.plotting_context('notebook', font_scale=1.2):
# Use a diverse color palette and order bars by count
    fig, ax = plt.subplots(figsize=(12, 7))
    g = sns.barplot(data=top_companies, x='patents', y='parent_name', ax=ax, hue='parent_name',
                        palette='Purples_r',  # Using a visually appealing color palette
                        )  # Order bars by count

    # Set meaningful labels and title
    g.set_xlabel('Number of Patents')
    g.set_ylabel('')
    g.set_title('Top 10 Companies by Patents', fontsize=16)

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
    fig.tight_layout()
    # save fig
    fig.savefig('../../../figures/patent_impact/top_companies.pdf')

cohorts['biobank'] = cohorts['cohort_name_lower'].apply(
    lambda x: ' '.join(x.split()[1:]))
top_cohorts = cohorts.head(10)
with sns.plotting_context('notebook', font_scale=1.2):
# Use a diverse color palette and order bars by count
    fig, ax = plt.subplots(figsize=(12, 7))
    g = sns.barplot(data=top_cohorts, x='patents', y='biobank', ax=ax, hue='biobank',
                        palette='Purples_r',  # Using a visually appealing color palette
                        )  # Order bars by count

    # Set meaningful labels and title
    g.set_xlabel('Number of Patents')
    g.set_ylabel('')
    g.set_title('Top 10 Biobanks by Patents', fontsize=16)

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
    fig.tight_layout()
    # save fig
    fig.savefig('../../../figures/patent_impact/top_biobanks.pdf')

# save cohorts in data/expansion/database/cohort_impact
cohorts.to_csv(
    '../../../data/expansion/database/cohort_impact/patent_impact.py', index=False)
