import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from tqdm import tqdm
import countrynames
import pycountry

# load mentions/papers.json
papers = pd.read_json('../../../data/expansion/database/mentions/papers.json', lines=True)
cohort_papers = pd.read_csv('../../../data/expansion/cohort_papers.csv')
cohorts = pd.read_csv('../../../data/expansion/cohorts.csv')
cohort_initials = pd.read_csv('../../../data/expansion/cohort_initials.csv')
cohort2initials = dict(zip(cohort_initials['cohort_name_lower'], cohort_initials['biobank']))

cit = papers[['id', 'citations']]
cit = cit.explode('citations')

def get_id(x):
    try:
        return x['id']
    except:
        return np.nan

cit['citation_id'] = cit['citations'].apply(get_id)
# drop nan values for citation_id
cit = cit.dropna(subset=['citation_id'])
cit = cit.merge(cohort_papers, how='left')
cohort2cit = dict(cit.groupby('cohort_name_lower').citation_id.unique().apply(set))
cohort2num_citations = {k: len(v) for k, v in cohort2cit.items()}
cohort_names = list(cohort2cit.keys())

# read hrcs_impact from cohort_impact folder
hrcs_impact = pd.read_csv('../../../data/expansion/database/cohort_impact/hrcs_impact.csv')
mesh_impact = pd.read_csv('../../../data/expansion/database/cohort_impact/mesh_impact.csv')

# hrcs sum from second column to one before last
hrcs_impact['papers'] = hrcs_impact.iloc[:, 1:-1].sum(axis=1)
main_hrcs_hc_papers = []
for i, row in hrcs_impact.iterrows():
    main = row['main_hrcs_hc']
    n = row[main]
    main_hrcs_hc_papers.append(n)
hrcs_impact['main_hrcs_hc_papers'] = main_hrcs_hc_papers
hrcs_impact['prop'] = hrcs_impact['main_hrcs_hc_papers'] / hrcs_impact['papers']
hrcs_impact['disease'] = hrcs_impact['main_hrcs_hc']
# prop < 0.5 then disease = 'Generic health relevance'
hrcs_impact.loc[hrcs_impact['prop'] < 0.4, 'disease'] = 'Generic health relevance'
cohort2hrcs = dict(zip(hrcs_impact['cohort_name_lower'], hrcs_impact['disease']))

# mesh_impact group by cohort_name_lower and sum papers
# sort mesh_impact by papers in descending order
mesh_impact = mesh_impact.sort_values('papers', ascending=False)
mesh = mesh_impact.groupby(['cohort_name_lower', 'main_mesh_name']).papers.sum().rename('main_mesh_papers').reset_index()
mesh_papers = mesh.groupby('cohort_name_lower').main_mesh_papers.sum().rename('papers').reset_index()
# merge left with mesh_impact
mesh = mesh.merge(mesh_papers, how='left', on='cohort_name_lower')
mesh['prop'] = mesh['main_mesh_papers'] / mesh['papers']
# sort mesh by prop in descending order
mesh = mesh.sort_values('prop', ascending=False)
# drop duplicates by cohort_name_lower
mesh = mesh.drop_duplicates('cohort_name_lower')
cohort2mesh = dict(zip(mesh['cohort_name_lower'], mesh['main_mesh_name']))

# country_biobanks.csv from database/descriptive folder
country = pd.read_csv('../../../data/expansion/database/cohort_data/cohort_places.csv')
country['prop'] = country['cohort_place_count'] / country['papers']
country['country'] = country['cohort_place'].apply(lambda x: countrynames.to_code(x) if countrynames.to_code(x) is not None else np.nan)
country = country.dropna(subset=['country'])
# sort by prop in descending order
country = country.sort_values('prop', ascending=False)
# drop duplicates by cohort_name_lower
country = country.drop_duplicates('cohort_name_lower')
cohort2country = dict(zip(country['cohort_name_lower'], country['country']))

# sum cohorts columns from second to one before last
cohorts['mentions'] = cohorts.iloc[:, 1:-1].sum(axis=1)
cohort2mentions = dict(zip(cohorts['cohort_name_lower'], cohorts['mentions']))

# for each pair of cohorts, calculate the number of common citations
common_citations = []
for pair in tqdm(itertools.combinations(cohort_names, 2)):
    common_citations.append((pair[0], pair[1], len(cohort2cit[pair[0]].intersection(cohort2cit[pair[1]]))))
common_citations = pd.DataFrame(common_citations, columns=['cohort1', 'cohort2', 'common_citations'])
# only those > 0
common_citations = common_citations[common_citations['common_citations'] > 0]
# rename common_citations to weight
common_citations.rename(columns={'common_citations': 'weight'}, inplace=True)

G = nx.from_pandas_edgelist(common_citations, 'cohort1', 'cohort2', 'weight')

# for each node get the neighbor with the highest weight
max_neighbor = {}
for node in G.nodes:
    neighbors = list(G.neighbors(node))
    if len(neighbors) > 0:
        max_neighbor[node] = max(neighbors, key=lambda x: G[node][x]['weight'])

# get the edges to keep
edges_to_keep = []
for edge in G.edges:
    if G[edge[0]][edge[1]]['weight'] == G[edge[0]][max_neighbor[edge[0]]]['weight']:
        edges_to_keep.append(edge)
    elif G[edge[0]][edge[1]]['weight'] == G[edge[1]][max_neighbor[edge[1]]]['weight']:
        edges_to_keep.append(edge)

# create a new graph with only the edges to keep
H = nx.Graph()
H.add_edges_from(edges_to_keep)

# add node attributes
nx.set_node_attributes(H, cohort2num_citations, 'num_citations')
nx.set_node_attributes(H, cohort2hrcs, 'hrcs')
nx.set_node_attributes(H, cohort2mesh, 'mesh')
nx.set_node_attributes(H, cohort2country, 'country')
nx.set_node_attributes(H, cohort2mentions, 'mentions')
nx.set_node_attributes(H, cohort2initials, 'initials')

# add edge weights from G to H
for edge in H.edges:
    H[edge[0]][edge[1]]['weight'] = G[edge[0]][edge[1]]['weight']

# save to graphml in data/networks folder
nx.write_graphml(H, '../../../data/networks/co_citations.graphml')