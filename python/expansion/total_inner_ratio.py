import pandas as pd
import plotly.io as pio
pio.renderers.default = "vscode"
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from tqdm import tqdm

# read database cohorts.csv
cohort = pd.read_csv('../../data/cohorts/final_cohorts.csv')
# remove 'the ' from start of cohort_name_lower
cohort['cohort_name'] = cohort['cohort_name_lower'].str.replace('^the ', '', regex=True)
df = pd.read_json('../../data/expansion/cohorts_counts.json', lines=True)

df['cohort_name_lower'] = 'the ' + df['cohort_name'].str.lower()
df['is_cohort_substring'] = df['cohort_name_lower'].apply(lambda x: any(y in x for y in cohort['cohort_name_lower']))
df['is_cohort'] = df['cohort_name'].str.lower().isin(cohort['cohort_name'])
df = df[(~df['is_cohort_substring']) | (~df['is_cohort'])]
# fillna with 0
df.fillna(0, inplace=True)
df = df[df['pmed_mentions'] > 0]

og_proportion = df[~df['kind'].isin(['biobank', 'bank', 'biorepo', 'consortium', 'network'])].copy()
og_proportion = og_proportion[og_proportion['related_mentions'] > og_proportion['related_mentions'].quantile(0.75)]
numeric_cols = og_proportion.select_dtypes(include='number').columns
og_proportion['total'] = og_proportion[numeric_cols].sum(axis=1)
# calculate the proportion of each cohort
og_proportion[numeric_cols] = og_proportion[numeric_cols].div(og_proportion['total'], axis=0)
# drop the total column
df_proportion = og_proportion.copy()
df_proportion.drop(columns='total', inplace=True)
df_proportion = df_proportion[df_proportion['related_mentions'] > df_proportion['related_mentions'].quantile(0.5)]
df_proportion = df_proportion[df_proportion['search_mentions'] > df_proportion['search_mentions'].quantile(0.05)]
df_proportion[df_proportion['kind'] == 'study']
og_proportion[og_proportion['kind'] == 'study']
# merge df_proportion with df
df_prop_merge = df_proportion.merge(df, on='cohort_name', how='left')
df_select_title = df[(df['is_cohort'] == False) & (df['cohort_name'].isin(df_proportion['cohort_name'])
                                             & (df['is_cohort_substring'] == False))]
df_select_title = df_select_title[df_select_title['cohort_name'] != 'Framingham Study']
df_prop_merge.sort_values('lower_mentions_x', ascending=False).head(40)

og_proportion = df[df['kind'].isin(['consortium', 'network'])].copy()
og_proportion = og_proportion[og_proportion['search_mentions'] > og_proportion['search_mentions'].quantile(0.25)]
numeric_cols = og_proportion.select_dtypes(include='number').columns
og_proportion['total'] = og_proportion[numeric_cols].sum(axis=1)
# calculate the proportion of each cohort
og_proportion[numeric_cols] = og_proportion[numeric_cols].div(og_proportion['total'], axis=0)
# drop the total column
df_proportion = og_proportion.copy()
df_proportion.drop(columns='total', inplace=True)
df_proportion = df_proportion[df_proportion['related_mentions'] > df_proportion['related_mentions'].quantile(0.5)]
df_proportion = df_proportion[df_proportion['search_mentions'] > df_proportion['search_mentions'].quantile(0.05)]
df_proportion[df_proportion['kind'] == 'study']
og_proportion[og_proportion['kind'] == 'study']
# merge df_proportion with df
df_prop_merge = df_proportion.merge(df, on='cohort_name', how='left')
df_select_ack = df[(df['is_cohort'] == False) & (df['cohort_name'].isin(df_proportion['cohort_name'])
                                             & (df['is_cohort_substring'] == False))]
df_prop_merge.sort_values('lower_mentions_x', ascending=False).head(40)

df_select = df[df['kind'].isin(['biobank', 'bank', 'biorepo'])].copy()
df_select = pd.concat([df_select, df_select_title, df_select_ack]).sort_values('mentions', ascending=False)
df_select['cohort_name'] = df_select['cohort_name'].str.replace('And', 'and')
df_select['cohort_name'] = df_select['cohort_name'].str.replace('OF', 'of')
df_select['cohort_name'] = df_select['cohort_name'].str.replace('IN', 'in')
df_select['is_cohort_substring'] = df_select['cohort_name_lower'].apply(lambda x: any(y in x for y in df_select['cohort_name_lower'] if x != y))
df_select = df_select[~(df_select['is_cohort_substring'])]
df_select.to_csv('../../data/expansion/cohorts.csv', index=False)



# melt the dataframe
df_proportion_melt = df_proportion.melt(id_vars=['cohort_name', 'kind', 'is_cohort', 'lower_mentions'], var_name='mention_type', value_name='proportion')
# boxplot of the proportion of mention type
fig = px.box(df_proportion_melt, x='mention_type', y='proportion', color='is_cohort')
fig.show()

# using PCA clustering to find the most related cohorts
# drop the non-numeric columns
df_pca = df.drop(columns=['cohort_name', 'kind', 'is_cohort'])
# standardize the data
scaler = StandardScaler()
pca = PCA()
pipeline = make_pipeline(scaler, pca)
pipeline.fit(df_pca)
# get components for each cohort
components = pipeline.transform(df_pca)
df_pca = pd.DataFrame(components, index=df.index)
df_pca['cohort_name'] = df['cohort_name']
df_pca['is_cohort'] = df['is_cohort']
df_pca = df_pca[df_pca[1] < 0]
df_pca = df_pca[(df_pca[2] < 0.14) & (df_pca[2] > -0.02)]
df_pca = df_pca[~((df_pca[1] > -0.5) & (df_pca[2] > 0))]
df_pca = df_pca[~((df_pca[1] > -5) & (df_pca[2] > 0.05))]
# scatter of the first two components
fig = px.scatter(df_pca, x=1, y=2, hover_name='cohort_name')
# color by is_cohort
fig.update_traces(marker=dict(color=df_pca['is_cohort'].map({True: 'blue', False: 'red'})))
fig.show()

