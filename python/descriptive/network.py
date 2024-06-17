import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sns
import itertools

G = nx.read_graphml('../../data/networks/co_citations.graphml')

# print node data
print(G.nodes(data=True))

# transform node data to pandas DataFrame
nodes = G.nodes(data=True)
nodes_df = pd.DataFrame(nodes, columns=['node', 'data'])

# get columns from data
nodes_df['mesh'] = nodes_df['data'].apply(lambda x: x.get('mesh'))
nodes_df['hrcs'] = nodes_df['data'].apply(lambda x: x.get('hrcs'))
nodes_df['num_citations'] = nodes_df['data'].apply(lambda x: x.get('num_citations'))
nodes_df['country'] = nodes_df['data'].apply(lambda x: x.get('country'))
nodes_df['mentions'] = nodes_df['data'].apply(lambda x: x.get('mentions'))

lcc = max(nx.connected_components(G), key=len)
nodes_df['lcc'] = nodes_df['node'].apply(lambda x: x in lcc)

degree = dict(G.degree())
nodes_df['degree'] = nodes_df['node'].apply(lambda x: degree[x])
weighted_degree = dict(G.degree(weight='weight'))
nodes_df['weighted_degree'] = nodes_df['node'].apply(lambda x: weighted_degree[x])

# for each mesh type get the number of edges from and to that mesh type
G = G.subgraph([node for node in G.nodes if 'mesh' in G.nodes[node]])
# get edges dataframe
edges = nx.to_pandas_edgelist(G)
node_source = nodes_df.rename(columns={'node': 'source', 'mesh': 'source_mesh'})
node_target = nodes_df.rename(columns={'node': 'target', 'mesh': 'target_mesh'})
edges = edges.merge(node_source, on='source').merge(node_target, on='target')
mesh_edges = edges[edges['source_mesh'] != edges['target_mesh']].groupby(['source_mesh', 'target_mesh']).size().reset_index(name='edges')
    

mesh_impact = pd.read_csv('../../data/expansion/database/cohort_impact/mesh_impact.csv')
mesh_impact['sec_tree_number'] = mesh_impact['tree_number'].apply(lambda x: '.'.join(x.split('.')[:2]))
mesh_impact['level'] = mesh_impact['tree_number'].apply(lambda x: len(x.split('.')))

mesh_impact = mesh_impact.sort_values('papers', ascending=False)
mesh_impact = mesh_impact.drop('tree_number', axis=1).drop_duplicates()
main_mesh = mesh_impact.groupby(['cohort_name_lower', 'main_mesh_name']).papers.sum().rename('main_mesh_papers').reset_index()
# order main_mesh by main_mesh_papers in descending order
main_mesh = main_mesh.sort_values('main_mesh_papers', ascending=False)
main_mesh = main_mesh.drop_duplicates(subset=['cohort_name_lower'])
# remove Otorhinolaryngologic Diseases and Occupational Diseases
main_mesh = main_mesh[~main_mesh['main_mesh_name'].isin(['Animal Diseases'])]

ax = sns.countplot(y=main_mesh['main_mesh_name'], edgecolor='black')