import pandas as pd
from thefuzz import fuzz
import numpy as np
from glob import glob
from tqdm import tqdm
import itertools
import networkx as nx
import spacy

REPLACE = {
    'the cancer genome atlas research network': 'the tcga research network',
    'the cancer genome atlas program': 'the tcga research network',
    'the framingham offspring study': 'the framingham heart study',
    "the framingham children's study": 'the framingham heart study',
    "the epic study": "the european prospective investigation into cancer and nutrition",
    "the epic-norfolk study": "the european prospective investigation into cancer and nutrition",
    "the epic-potsdam study": "the european prospective investigation into cancer and nutrition",
    "the epic interact consortium": "the european prospective investigation into cancer and nutrition",
    "the european prospective investigation of cancer norfolk": "the european prospective investigation into cancer and nutrition",
    "the hcv research uk biobank": "the uk biobank",
    "the hunt biobank": "the hunt study",
    "the supplemental nutritional assistance program": "the supplemental nutrition assistance program",
}

DROP = [
    'the multi-ethnic study',
    'the next steps',
    'the english longitudinal study',
    'the australian longitudinal study',
    'the longitudinal aging study',
    'the national biobank',
    'the medical biobank',
    'the electronic medical records',
    'the vascular ageing',
    'the cerebral amyloid angiopathy',
    'the memory clinic',
    'the american national election studies',
    'the general social survey',
    'the national crime victimization survey',
    'the european bioinformatics institute',
    'the canadian network',
    'the macarthur foundation research network',
    'the united states study',
    'the canadian study'
    'the quebec network',
    'the tissue biobank',
    'the central biobank',
    'the national longitudinal study of adolescent',
    'the national epidemiologic survey',
    'the national survey of children',
    'the longitudinal survey of immigrants',
    'the university biobank',
    'the atlantic path',
    'the longitudinal ageing study',
    'the national survey of american',
    'the integrated biobank',
    'the telethon network of genetic',
    'the neurobiobank',
    'the canadian study',
    'the human brain bank',
    'the environment study',
    'the clinical trials network',
]

DATA = '../../data/bquery/pubs/'
DATAE = '../../data/expansion/pubs/'
FULL_UNCASED = DATA + 'uncased_'
FULL_UNCASEDE = DATAE

unpubs = glob(FULL_UNCASED + '*.json')
sources = ['title', 'abstract', 'acknowledgements']
dim = []
for p in unpubs:
    for source in sources:
        if source in p:
            tmp = pd.read_json(p, lines=True)
            tmp['source'] = source
            dim.append(tmp)
dim = pd.concat(dim)

unpubs = glob(FULL_UNCASEDE + '*.json')
dime = []
for p in unpubs:
    for source in sources:
        if source in p:
            tmp = pd.read_json(p, lines=True)
            tmp['source'] = source
            dime.append(tmp)
dime = pd.concat(dime)
df = pd.concat([dim, dime])
df = df.drop_duplicates(subset=['id', 'cohort_name_lower', 'source'])
df['cohort_name_lower'] = df['cohort_name_lower'].str.replace('’', "'")
df = df[~df['cohort_name_lower'].isin(DROP)]
df = df.drop('cohort_name', axis=1).to_csv('../../data/expansion/cohort_sources.csv', index=False)

cohort_names = df['cohort_name_lower'].unique()
cohort_papers = df.groupby('cohort_name_lower')['id'].apply(set).reset_index(name='papers')
cohort_papers = dict(cohort_papers.values)
cohort_mentions = {i: len(cohort_papers[name]) for i, name in enumerate(cohort_names)}
name_mentions = {name: len(cohort_papers[name]) for name in cohort_names}
name_indices = {name: i for i, name in enumerate(cohort_names)}
# make list with all 2-combinations of cohort indices if different
combinations = list(itertools.combinations(range(len(cohort_names)), 2))

patents1 = pd.read_json(
    '../../data/expansion/patents/patents.json', lines=True)
patents2 = pd.read_json(
    '../../data/expansion/patents/dim_patents_abstract.json', lines=True)
patents3 = pd.read_json(
    '../../data/bquery/patents/dim_patents.json', lines=True)
patents4 = pd.read_json(
    '../../data/bquery/patents/dim_patents_abstract.json', lines=True)
patents = pd.concat([patents1, patents2, patents3, patents4])
patents['cohort_name_lower'] = patents['cohort_name_lower'].str.replace(
    '’', "'")
patents = patents[~patents['cohort_name_lower'].isin(DROP)]
patent_names = patents['cohort_name_lower'].unique()
patent_papers = patents.groupby('cohort_name_lower')['id'].apply(set).reset_index(name='patents')
patent_papers = dict(patent_papers.values)
patent_mentions = {i: len(patent_papers[name]) for i, name in enumerate(patent_names)}
patent_name_indices = {name: i for i, name in enumerate(patent_names)}
patent_combinations = list(itertools.combinations(range(len(patent_names)), 2))

M_partial = np.array([[fuzz.partial_ratio(x, y) for x in cohort_names] for y in cohort_names])
M_token = np.array([[fuzz.token_set_ratio(x, y) for x in cohort_names] for y in cohort_names])
M_partial_token = np.array([[fuzz.partial_ratio(' '.join(x.split()[1:-1]), ' '.join(y.split()[1:-1])) for x in cohort_names] for y in cohort_names])

M_partial_token_patents = np.array([[fuzz.partial_ratio(' '.join(x.split()[1:-1]), ' '.join(y.split()[1:-1])) for x in patent_names] for y in patent_names])


M = np.zeros((len(cohort_names), len(cohort_names)))
for i in tqdm(range(len(cohort_names))):
    ci = cohort_names[i]
    for j in tqdm(range(len(cohort_names)), leave=False):
        cj = cohort_names[j]
        if i != j:
            pi = cohort_papers[ci]
            pj = cohort_papers[cj]
            intersection = len(pi.intersection(pj))
            leni = len(pi)
            if intersection > 0:
                M[i, j] = intersection / leni

M_patents = np.zeros((len(patent_names), len(cohort_names)))
for i in tqdm(range(len(patent_names))):
    ci = patent_names[i]
    for j in tqdm(range(len(patent_names)), leave=False):
        cj = patent_names[j]
        if i != j:
            pi = patent_papers[ci]
            pj = patent_papers[cj]
            intersection = len(pi.intersection(pj))
            leni = len(pi)
            if intersection > 0:
                M_patents[i, j] = intersection / leni

# avoid of, in, on if samle length then larger
acronyms = []
for name in tqdm(cohort_names):
    words = [w for w in name.replace('-', ' ').replace('/', ' ').split() if w not in ['and', 'of', 'for', 'on']]
    if len(words) > 3:
        f = words[0]
        l = words[-1]
        acronym = ''.join([w[0] for w in words[1:-1]])
        n = ' '.join([f, acronym, l])
        acronyms.append(n)
    else:
        acronyms.append(name)
M_acronym = np.array([[fuzz.ratio(x, y) for x in acronyms] for y in acronyms])



similar = [(cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j]) for i, j in combinations if min(M[i,j], M[j,i]) >  0 and M_acronym[i, j] > 98 and min(len(cohort_names[i].split()), len(cohort_names[j].split())) == 3]
# order by cohort_mentions 1
rep = dict()
rep_list = []
for ci, mi, cj, mj in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 0])
symbols = ['-', "'", "'s"]
cohorts_symbols = [x.replace('-', ' ').replace("'s", "").replace("'", '') for x in cohort_names]
similar = []
for i, name in enumerate(cohorts_symbols[:-1]):
    j = i
    for _, name2 in enumerate(cohorts_symbols[i+1:]):
        j += 1
        if name == name2:
            similar.append((cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j]))
for ci, mi, cj, mj in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 1])
# get cohort names for those with similarity over 0.9
similar = [(cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j], (i, j)) for i, j in combinations if min(M[i,j], M[j,i]) >=  0.2 and M_partial[i, j] > 90]
for ci, mi, cj, mj, (i,j) in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 2])
similar = [(cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j], (i, j)) for i, j in combinations if max(M[i,j], M[j,i]) >=  0.1 and min(M[i,j], M[j,i]) > 0 and M_token[i, j] == 100 and 'korea' not in cohort_names[j]]
for ci, mi, cj, mj, (i, j) in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 3])


sim1 = [(cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j], (i, j)) for i, j in combinations if min(M[i,j], M[j,i]) > 0.05 and M_partial_token[i, j] == 100]
# print similar elements not in rep items

sim2 = [(cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j], (i, j)) for i, j in combinations if max(M[i,j], M[j,i]) > 0.3 and min(M[i,j], M[j,i]) > 0 and M_partial_token[i, j] > 90]
sim2 = [x for i, x in enumerate(sim2) if 'mexican' not in x[0] and 'mexican' not in x[2]]
similar = sim1 + sim2
for ci, mi, cj, mj, (i, j) in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 4])
similar = [(patent_names[i], patent_mentions[i], patent_names[j], patent_mentions[j], (i, j)) for i, j in patent_combinations if M_patents[i,j] > 0.4 and M_patents[j,i] > 0.3 and patent_mentions[i] > 10  and M_partial_token_patents[i, j] == 100]
for ci, mi, cj, mj, (i, j) in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 5])
# use proper nouns
nlp = spacy.load("en_core_web_sm")
cohort_nouns = []
for name in tqdm(cohort_names):
    doc = nlp(name)
    nouns = ' '.join([chunk.norm_ for chunk in doc if chunk.pos_ not in ['CCONJ', 'ADP', 'NUM', 'SYM', 'AUX', 'DET', 'PUNCT', 'PART']])
    cohort_nouns.append(nouns)
similar = [(cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j], (i, j)) for i, j in combinations if fuzz.ratio(cohort_nouns[i], cohort_nouns[j]) >= 95 and cohort_nouns[i] and cohort_nouns[j] and min(M[i,j], M[j,i]) > 0]
for ci, mi, cj, mj, (i, j) in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 6])
similar = [(cohort_names[i], cohort_mentions[i], cohort_names[j], cohort_mentions[j], (i, j)) for i, j in combinations if fuzz.token_sort_ratio(cohort_nouns[i], cohort_nouns[j]) == 100 and len(cohort_nouns[i].split()) > 1  and len(cohort_nouns[j].split()) > 1]
for ci, mi, cj, mj, (i, j) in similar:
    rep[ci] = cj
    rep_list.append([ci, cj, 7])
    
    
G = nx.Graph()
for u, v, _ in rep_list:
    G.add_edge(u, v)
# count connected components
cc = list(nx.connected_components(G))
rep2 = dict()
for c in cc:
    max_c = 0
    for name in c:
        if len(cohort_papers[name]) > max_c:
            max_c = len(cohort_papers[name])
            max_cohort = name
    for name in c:
        if name != max_cohort:
            rep2[name] = max_cohort

for k, v in REPLACE.items():
    rep2[k] = v
    
replace_df = pd.DataFrame(rep2.items(), columns=['cohort_name_lower', 'replace'])
drop_df = pd.DataFrame(DROP, columns=['cohort_name_lower'])
# save the dataframe
replace_df.to_csv('../../data/expansion/replace_cohorts.csv', index=False)
drop_df.to_csv('../../data/expansion/drop_cohorts.csv', index=False)

df_replaced = df.copy()
df_replaced['cohort_name_lower'] = df_replaced['cohort_name_lower'].replace(rep2)
df_replaced = df_replaced[~df_replaced['cohort_name_lower'].isin(DROP)]
del df_replaced['cohort_name']
df_replaced = df_replaced.drop_duplicates(subset=['id', 'cohort_name_lower', 'source'])
df_replaced.to_csv('../../data/expansion/cohort_mentions.csv', index=False)
df_replaced.drop_duplicates(subset=['id', 'cohort_name_lower'])[['id', 'cohort_name_lower']].to_csv(
    '../../data/expansion/cohort_papers.csv', index=False)
pubs = df_replaced.drop_duplicates(subset='id')[['id']].copy()
pubs.to_csv('../../data/expansion/papers.csv', index=False)

# cohorts
cohorts = df_replaced.groupby('cohort_name_lower')[
    'id'].nunique().rename('pubs').reset_index()
cohorts = cohorts.sort_values('pubs', ascending=False)
cohorts = cohorts.merge(
    df_replaced[df_replaced['source'] == 'title']
    .groupby('cohort_name_lower')['id']
    .nunique()
    .rename('title')
    .reset_index()
    .sort_values('title', ascending=False),
    how='left'
).merge(
    df_replaced[df_replaced['source'] == 'abstract']
    .groupby('cohort_name_lower')['id']
    .nunique()
    .rename('abstract')
    .reset_index()
    .sort_values('abstract', ascending=False),
    how='left'
).merge(
    df_replaced[df_replaced['source'] == 'acknowledgements']
    .groupby('cohort_name_lower')['id']
    .nunique()
    .rename('acknowledgements')
    .reset_index()
    .sort_values('acknowledgements', ascending=False),
    how='left'
)

patents['cohort_name_lower'] = patents['cohort_name_lower'].replace(rep2)
patents = patents[~patents['cohort_name_lower'].isin(DROP)]
patents = patents.drop_duplicates(subset=['id', 'cohort_name_lower'])
patents['cohort_name_lower'] = patents['cohort_name_lower'].replace(rep2)
cohorts = cohorts.merge(
    patents.groupby('cohort_name_lower')['id']
    .nunique()
    .rename('patents')
    .reset_index()
    .sort_values('patents', ascending=False),
    how='left'
    )

patents.to_csv('../../data/expansion/cohort_patents.csv', index=False)
patents.drop_duplicates(subset='id')[['id']].to_csv(
    '../../data/expansion/patents.csv', index=False)

grants1_expansion = pd.read_json(
    '../../data/expansion/grants/grants_title_1.json', lines=True)
grants2_expansion = pd.read_json(
    '../../data/expansion/grants/grants_title_2.json', lines=True)
grants_keywords_expansion = pd.read_json(
    '../../data/expansion/grants/grants_keywords.json', lines=True)
grants_abstract_expansion = pd.read_json(
    '../../data/expansion/grants/grants_abstract.json', lines=True)
grants1_bquery = pd.read_json(
    '../../data/bquery/grants/grants_title_uncased_1.json', lines=True)
grants2_bquery = pd.read_json(
    '../../data/bquery/grants/grants_title_uncased_2.json', lines=True)
grants_keywords_bquery = pd.read_json(
    '../../data/bquery/grants/grants_keywords_uncased.json', lines=True)
grants_abstract_bquery = pd.read_json(
    '../../data/bquery/grants/grants_abstract_uncased.json', lines=True)
grants = pd.concat([
    grants1_expansion, grants2_expansion,
    grants_keywords_expansion, grants_abstract_expansion,
    grants1_bquery, grants2_bquery,
    grants_keywords_bquery, grants_abstract_bquery
])
grants['cohort_name_lower'] = grants['cohort_name_lower'].str.replace(
    '’', "'")
grants['cohort_name_lower'] = grants['cohort_name_lower'].replace(rep2)
grants = grants[~grants['cohort_name_lower'].isin(DROP)]
grants = grants.drop_duplicates(subset=['id', 'cohort_name_lower'])
cohorts = cohorts.merge(
    grants.groupby('cohort_name_lower')['id']
    .nunique()
    .rename('grants')
    .reset_index()
    .sort_values('grants', ascending=False),
    how='left'
)
grants.to_csv('../../data/expansion/cohort_grants.csv', index=False)
grants.drop_duplicates(subset='id')[['id']].to_csv(
    '../../data/expansion/grants.csv', index=False)

clinical_trials_files1 = glob('../../data/expansion/clinical_trials/*.json')
clinical_trials_files2 = glob('../../data/bquery/clinical_trials/*.json')
clinical_trials_files = clinical_trials_files1 + clinical_trials_files2
clinical_trials = []
for f in clinical_trials_files:
    clinical_trials.append(pd.read_json(f, lines=True))
clinical_trials = pd.concat(clinical_trials)
clinical_trials['cohort_name_lower'] = (
    clinical_trials['cohort_name_lower'].str.replace(
    '’', "'"))
clinical_trials['cohort_name_lower'] = (
    clinical_trials['cohort_name_lower'].replace(rep2))
clinical_trials = clinical_trials[
    ~clinical_trials['cohort_name_lower'].isin(DROP)]
clinical_trials = clinical_trials.drop_duplicates(
    subset=['id', 'cohort_name_lower'])
cohorts = cohorts.merge(
    clinical_trials.groupby('cohort_name_lower')['id']
    .nunique()
    .rename('clinical_trials')
    .reset_index()
    .sort_values('clinical_trials', ascending=False),
    how='left'
)
clinical_trials.to_csv(
    '../../data/expansion/cohort_clinical_trials.csv', index=False)
clinical_trials.drop_duplicates(subset='id')[['id']].to_csv(
    '../../data/expansion/clinical_trials.csv', index=False)

policy_files1 = glob('../../data/bquery/policy/*uncased*.json')
policy_files2 = glob('../../data/expansion/policy/*.json')
policy_files = policy_files1 + policy_files2
policy = []
B = True
for file in policy_files:
    if 'title' in file:
        B = False
    else:
        B = True
    tmp = pd.read_json(file, lines=B)
    policy.append(tmp)
policy = pd.concat(policy)
policy['cohort_name_lower'] = policy['cohort_name_lower'].str.replace(
    '’', "'")
policy['cohort_name_lower'] = policy['cohort_name_lower'].replace(rep2)
policy = policy[~policy['cohort_name_lower'].isin(DROP)]
policy = policy.drop_duplicates(subset=['id', 'cohort_name_lower'])
cohorts = cohorts.merge(
    policy.groupby('cohort_name_lower')['id']
    .nunique()
    .rename('policy')
    .reset_index()
    .sort_values('policy', ascending=False),
    how='left'
)
policy.to_csv('../../data/expansion/cohort_policy.csv', index=False)
policy.drop_duplicates(subset='id')[['id']].to_csv(
    '../../data/expansion/policy.csv', index=False)
datasets1 = pd.read_json(
    '../../data/bquery/datasets/datasets_description_uncased.json', lines=True)
datasets2 = pd.read_json(
    '../../data/expansion/datasets/datasets_description.json', lines=True)
datasets = pd.concat([datasets1, datasets2])
datasets['cohort_name_lower'] = datasets['cohort_name_lower'].str.replace(
    '’', "'")
datasets['cohort_name_lower'] = datasets['cohort_name_lower'].replace(rep2)
datasets = datasets[~datasets['cohort_name_lower'].isin(DROP)]
datasets = datasets.drop_duplicates(subset=['id', 'cohort_name_lower'])
cohorts = cohorts.merge(
    datasets.groupby('cohort_name_lower')['id']
    .nunique()
    .rename('datasets')
    .reset_index()
    .sort_values('datasets', ascending=False),
    how='left'
)
datasets.to_csv('../../data/expansion/cohort_datasets.csv', index=False)
datasets.drop_duplicates(subset='id')[['id']].to_csv(
    '../../data/expansion/datasets.csv', index=False)
cohorts = cohorts.fillna(0)
cohorts.to_csv('../../data/expansion/cohorts.csv', index=False)
