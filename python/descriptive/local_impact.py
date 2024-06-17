import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from statsmodels.stats.proportion import proportions_ztest
from tqdm import tqdm

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)


ref_papers = pd.read_csv('../../data/expansion/database/cohort_impact/reference_papers.csv')
author_impact = pd.read_csv('../../data/expansion/database/cohort_impact/authors_impact.csv')
papers = pd.read_json('../../data/expansion/database/mentions/papers.json', lines=True)
papers['author_list'] = papers['authors'].apply(lambda x: [y['researcher_id'] for y in x if 'researcher_id' in y])
papers['corresponding'] = papers['authors'].apply(lambda x: [y['researcher_id'] for y in x if 'corresponding' in y and 'researcher_id' in y and y['corresponding'] == True])
main_papers = pd.read_csv('../../data/database/foundational/main.csv')
target = pd.read_csv('../../data/expansion/database/cohort_impact/target.csv')
paper_authors = papers[['id', 'author_list']].explode('author_list').dropna()
# rename author_list to researcher_id
paper_authors = paper_authors.rename(columns={'author_list': 'researcher_id'})

openalex = pd.read_csv('../../data/database/foundational/openalex.csv')
# rename corresponding with oa_corresponding
openalex = openalex.rename(columns={'corresponding': 'oa_corresponding'})
openalex = openalex.merge(papers[['id', 'doi', 'corresponding', 'author_list']], on='doi', how='left')
openalex = openalex.drop_duplicates(subset=['id', 'cohort'])

cohort_papers = pd.read_csv('../../data/expansion/cohort_papers.csv')
res = pd.read_json('../../data/expansion/database/authors/authors.json', lines=True)




# explode author_impact by top_10_authors at comma
authors = author_impact[['cohort_name_lower', 'top_10_authors']].dropna()
authors['top_10_authors'] = authors['top_10_authors'].str.split(',')
authors = authors.explode('top_10_authors')
# rename top_10_authors to researcher_id
authors = authors.rename(columns={'top_10_authors': 'researcher_id'})
authors = authors.merge(res, on='researcher_id', how='left')

corr = author_impact[['cohort_name_lower', 'author_id', 'author_prop', 'author_papers']].dropna()
# rename author_id to researcher_id
corr = corr.rename(columns={'author_id': 'researcher_id'})
corr = corr.merge(res, on='researcher_id', how='left')
# rename org_id to biobank_org_id and org_name to biobank_org
corr = corr.rename(columns={'org_id': 'biobank_org_id', 'org_name': 'biobank_org', 'org_country': 'biobank_country'})
corr = corr.dropna()

cohort_papers = cohort_papers.merge(papers[['id', 'corresponding']], on='id', how='left')
corr_papers = cohort_papers.explode('corresponding').dropna()
# rename corresponding to researcher_id
corr_papers = corr_papers.rename(columns={'corresponding': 'researcher_id'})
corr_papers = corr_papers.merge(res, on='researcher_id', how='left')
corr_papers = corr_papers.dropna()
paper_org = corr_papers.groupby('id').org_id.apply(lambda x: x.value_counts().index[0]).rename('org_id').reset_index()
paper_country = corr_papers.groupby('id').org_country.apply(lambda x: x.value_counts().index[0]).rename('country').reset_index()
paper_country = paper_country.merge(cohort_papers[['id', 'cohort_name_lower']], on='id', how='left')
paper_org = paper_org.merge(cohort_papers[['id', 'cohort_name_lower']], on='id', how='left')

main_papers = ref_papers[ref_papers['prop_inner_citations'] > 0.1][['id', 'cohort_name_lower']]
main_papers = main_papers.merge(corr_papers, how='left', on=['id', 'cohort_name_lower'])
main_corr = corr[corr['author_prop'] > 0.05]
main_papers = main_papers[~main_papers.cohort_name_lower.isin(main_corr.cohort_name_lower.unique())]
main_papers = main_papers.dropna()
main_papers = main_papers[['cohort_name_lower', 'researcher_id']]
main_corr = main_corr[['cohort_name_lower', 'researcher_id']]
main = pd.concat([main_papers, main_corr])
main = main.merge(res, on='researcher_id', how='left')
main = main.rename(columns={'org_id': 'biobank_org_id', 'org_name': 'biobank_org', 'org_country': 'biobank_country'})

team_papers = papers[['id', 'corresponding', 'citations_count']].explode('corresponding').dropna()
# rename corresponding to researcher_id
team_papers = team_papers.rename(columns={'corresponding': 'researcher_id'})
team_papers = team_papers.merge(cohort_papers[['id', 'cohort_name_lower']], on='id', how='left')
team_papers = team_papers.merge(main[['cohort_name_lower', 'researcher_id', 'author_name']], on=['cohort_name_lower', 'researcher_id'])
# order by citations_count
team_papers = team_papers.sort_values('citations_count', ascending=False)
# drop duplicates by cohort_name_lower
team_papers = team_papers.drop_duplicates(subset='cohort_name_lower')
author_list = papers[['id', 'author_list']].explode('author_list').dropna()
author_list = author_list.merge(cohort_papers[['id', 'cohort_name_lower']], on='id', how='left')
cohort_list_papers = author_list.groupby('cohort_name_lower').id.nunique().rename('num_papers').reset_index()
team_papers = team_papers.merge(author_list, on=['id', 'cohort_name_lower'], how='left')
team = team_papers[['cohort_name_lower', 'author_list']].drop_duplicates()
team_num = team.groupby('cohort_name_lower').author_list.nunique().rename('num_authors').reset_index()
team_20 = team_num[team_num['num_authors'] <= 20]['cohort_name_lower'].values
team_20 = team[team['cohort_name_lower'].isin(team_20)]
corr_20 = main[main['cohort_name_lower'].isin(team_20.cohort_name_lower.unique())][['cohort_name_lower', 'researcher_id']]
team_20.columns = ['cohort_name_lower', 'team_member']
corr_20.columns = ['cohort_name_lower', 'corrersponding']
same_authors = author_list.merge(team_20, on='cohort_name_lower', how='left').dropna()
same_authors['same_author'] = same_authors['author_list'] == same_authors['team_member']
cohort_team = same_authors[same_authors['same_author']].drop_duplicates(subset=['id', 'cohort_name_lower'])
cohort_team = cohort_team.cohort_name_lower.value_counts().rename('team').reset_index()
cohort_team.columns = ['cohort_name_lower', 'team']
cohort_team = cohort_team.merge(cohort_list_papers, on='cohort_name_lower', how='left')
cohort_team['team_member_per'] = cohort_team['team'] / cohort_team['num_papers'] * 100
same_corr = author_list.merge(corr_20, on='cohort_name_lower', how='left').dropna()
same_corr = same_corr[same_corr['author_list'] == same_corr['corrersponding']]
cohort_corr = same_corr.drop_duplicates(subset=['id', 'cohort_name_lower'])
cohort_corr = cohort_corr.cohort_name_lower.value_counts().rename('corresponding').reset_index()
cohort_corr.columns = ['cohort_name_lower', 'corresponding']
cohort_team = cohort_team.merge(cohort_corr, on='cohort_name_lower', how='left')
cohort_team['corresponding_per'] = cohort_team['corresponding'] / cohort_team['num_papers'] * 100

team_same_country = same_authors[same_authors['same_author']].drop_duplicates(subset=['id', 'cohort_name_lower'])
team_same_country = team_same_country.merge(paper_country.dropna(), on=['id', 'cohort_name_lower'], how='left').dropna()
team_same_country['same_country'] = team_same_country['biobank_country'] == team_same_country['country']

team_same_org = same_authors[same_authors['same_author']].drop_duplicates(subset=['id', 'cohort_name_lower'])
team_same_org = team_same_org.merge(paper_org.dropna(), on=['id', 'cohort_name_lower'], how='left').dropna()
team_same_org['same_org'] = team_same_org['biobank_org_id'] == team_same_org['org_id']

# save team_20 to descriptive
team_20.to_csv('../../data/expansion/database/descriptive/biobank_team_20members.csv', index=False)
# save main to descriptive
main.to_csv('../../data/expansion/database/descriptive/biobank_PIs.csv', index=False)

biobank_country = main.groupby('cohort_name_lower').biobank_country.apply(lambda x: x.value_counts().index[0]).rename('biobank_country').reset_index()
biobank_org = main.groupby('cohort_name_lower').biobank_org_id.apply(lambda x: x.value_counts().index[0]).rename('biobank_org_id').reset_index()
paper_country = paper_country.merge(biobank_country, on='cohort_name_lower', how='left')
paper_org = paper_org.merge(biobank_org, on='cohort_name_lower', how='left')
paper_country['same_country'] = paper_country['country'] == paper_country['biobank_country']
paper_org['same_org'] = paper_org['org_id'] == paper_org['biobank_org_id']
same_country_prop = paper_country.groupby('cohort_name_lower').same_country.mean().sort_values(ascending=False)
same_org_prop = paper_org.groupby('cohort_name_lower').same_org.mean().sort_values(ascending=False)

paper_authors = paper_authors.merge(cohort_papers[['id', 'cohort_name_lower']], on='id', how='left')
paper_authors = paper_authors.merge(main, on=['cohort_name_lower', 'researcher_id'])

target_main = target[target.cohort_name_lower.isin(main.cohort_name_lower.unique())]
bottom_20 = target_main[target_main['target'] <= target_main['target'].quantile(0.2)]['cohort_name_lower'].values
top_20 = target_main[target_main['target'] >= target_main['target'].quantile(0.8)]['cohort_name_lower'].values


cohort_team['Biobank BIF'] = 'All'
cohort_team.loc[cohort_team.cohort_name_lower.isin(bottom_20), 'Biobank BIF'] = 'Bottom 20%'
cohort_team.loc[cohort_team.cohort_name_lower.isin(top_20), 'Biobank BIF'] = 'Top 20%'
cohort_team = cohort_team[cohort_team.cohort_name_lower.isin(target_main.cohort_name_lower.unique())]
cohort_team['corresponding_per'] = cohort_team['corresponding'] / cohort_team['num_papers'] * 100
cohort_team['team_member_per'] = cohort_team['team'] / cohort_team['num_papers'] * 100

same = pd.DataFrame(same_country_prop).reset_index()
same = same.merge(pd.DataFrame(same_org_prop).reset_index(), on='cohort_name_lower', how='left')
same['Biobank BIF'] = 'All'
same.loc[same.cohort_name_lower.isin(bottom_20), 'Biobank BIF'] = 'Bottom 20%'
same.loc[same.cohort_name_lower.isin(top_20), 'Biobank BIF'] = 'Top 20%'
same = same[same.cohort_name_lower.isin(target_main.cohort_name_lower.unique())]
same = same.merge(author_impact[['cohort_name_lower', 'author_per', 'top_10_author_per']], on='cohort_name_lower', how='left')
same['same_country'] = same['same_country'] * 100
same['same_org'] = same['same_org'] * 100

# null model country
np.random.seed(0)
ran_paper_country = paper_country.copy()

ran_df_country = []
for i in tqdm(range(100)):
    np.random.shuffle(ran_paper_country.country.values)
    ran_paper_country['same_country'] = ran_paper_country['country'] == ran_paper_country['biobank_country']
    ran_df_country.append(pd.DataFrame(ran_paper_country.groupby('cohort_name_lower').same_country.mean().sort_values(ascending=False)).reset_index())
ran_df_country = pd.concat(ran_df_country)
ran_df_country = ran_df_country.groupby('cohort_name_lower').same_country.mean().sort_values(ascending=False).reset_index()

ran_paper_org = paper_org.copy()
ran_df_org = []
for i in tqdm(range(100)):
    np.random.shuffle(paper_org.org_id.values)
    ran_paper_org['same_org'] = ran_paper_org['org_id'] == ran_paper_org['biobank_org_id']
    ran_df_org.append(pd.DataFrame(ran_paper_org.groupby('cohort_name_lower').same_org.mean().sort_values(ascending=False)).reset_index())
ran_df_org = pd.concat(ran_df_org)
ran_df_org = ran_df_org.groupby('cohort_name_lower').same_org.mean().sort_values(ascending=False).reset_index()

ran_same = ran_df_country.merge(ran_df_org, on='cohort_name_lower', how='left')
ran_same['distribution'] = 'Null model'

same['distribution'] = 'Biobanks'

ran_same = pd.concat([same[['cohort_name_lower', 'distribution', 'same_country', 'same_org']], ran_same])

observed_c = ran_same[ran_same.distribution=='Biobanks']['same_country'].values
observed_o = ran_same[ran_same.distribution=='Biobanks']['same_org'].values
null_c = ran_same[ran_same.distribution=='Null model']['same_country'].values
null_o = ran_same[ran_same.distribution=='Null model']['same_org'].values

# get p-values for the difference between observed and null model
t, p = ttest_ind(observed_c, null_c)
t, p = ttest_ind(observed_o, null_o)

ran_melt = ran_same.melt(id_vars=['cohort_name_lower', 'distribution'], value_vars=['same_country', 'same_org'])
ran_melt['variable'] = ran_melt['variable'].map({'same_country': 'Same Country', 'same_org': 'Same Institution'})



# PLOTS #
color_org = "#00356b"
color_country = "#ff43a4"

plt.figure(figsize=(8, 6))
g = sns.JointGrid(y="same_country", x="same_org", data=same, space=0)
g = g.plot_joint(sns.kdeplot, cmap="mako", fill=True, thresh=0, levels=100)
sns.kdeplot(same["same_org"], color=color_org, fill=True, bw=0.1, ax=g.ax_marg_x)
sns.kdeplot(same["same_country"], color=color_country, fill=True, bw=0.1, ax=g.ax_marg_y, vertical=True)
g.ax_joint.set_ylim(0, 100)
g.ax_joint.set_xlim(0, 100)
ax = g.ax_joint
ax.set_xlabel('Mentions from Same Institution (%)')
ax.set_ylabel('Mentions from Same Country (%)')
ax2 = g.ax_marg_x
ax1 = g.ax_marg_y
g.figure.suptitle('Joint Distribution of National and Institutional\nBiobank Research Impact')
# remove grid
ax1.grid(False)
ax2.grid(False)
g.figure.tight_layout()
g.figure.savefig('../../figures/local_impact/joint_country_org.pdf')

color_pi = '#33ccff'
color_team = '#ffcc33'

plt.figure(figsize=(8, 6))
g = sns.JointGrid(y="team_member_per", x="corresponding_per", data=cohort_team, space=0)
g = g.plot_joint(sns.kdeplot, cmap="mako", fill=True, thresh=0, levels=100)
sns.kdeplot(cohort_team["team_member_per"], color=color_team, fill=True, bw=0.1, ax=g.ax_marg_x)
sns.kdeplot(cohort_team["corresponding_per"], color=color_pi, fill=True, bw=0.1, ax=g.ax_marg_y, vertical=True)
g.ax_joint.set_ylim(0, 100)
g.ax_joint.set_xlim(0, 100)
ax = g.ax_joint
ax.set_xlabel('Mentions Co-Authored by Biobank PIs (%)')
ax.set_ylabel('Mentions Co-Authored by Biobank Team (%)')
ax2 = g.ax_marg_x
ax1 = g.ax_marg_y
g.figure.suptitle('Joint Distribution of Team and PIs\nBiobank Research Impact')
# remove grid
ax1.grid(False)
ax2.grid(False)
g.figure.tight_layout()
g.figure.savefig('../../figures/local_impact/joint_team.pdf')



ax = sns.boxplot(data=ran_melt[ran_melt.distribution=='Biobanks'], y='value', x='variable', palette='colorblind')


# PLOTS #
plt.figure(figsize=(8, 6))
ax = sns.histplot(data=ran_melt[ran_melt.distribution=='Biobanks'], hue='variable', x='value', palette=[color_country, color_org], cumulative=False,
            common_norm=False, stat='probability', element='step', fill=True, hue_order=['Same Country', 'Same Institution'])
ax.set_xlabel('Mentions (%)')
ax.set_title('Distribution of National and Institutional Biobank Research Impact')
sns.despine()  # Removes top and right borders, trims remaining
sns.move_legend(
    ax, "upper center",
    ncol=1, frameon=True, shadow=False, facecolor='white', edgecolor='white',
    title='From'
)
plt.tight_layout()
plt.savefig('../../figures/local_impact/main.pdf')


team_melt = cohort_team.melt(id_vars=['cohort_name_lower'], value_vars=['team_member_per', 'corresponding_per'])
plt.figure(figsize=(8, 6))
ax = sns.histplot(data=team_melt, hue='variable', x='value', cumulative=False, palette=[color_team, color_pi], alpha=0.5,
            common_norm=False, stat='probability', element='step', fill=True, hue_order=['team_member_per', 'corresponding_per'])
ax.set_xlabel('Mentions (%)')
ax.set_title('Distribution of National and Institutional Biobank Research Impact')
sns.despine()  # Removes top and right borders, trims remaining
sns.move_legend(
    ax, "upper center",
    ncol=1, frameon=True, shadow=False, facecolor='white', edgecolor='white',
    title='From'
)
plt.tight_layout()
plt.savefig('../../figures/local_impact/team.pdf')

melt = cohort_team[cohort_team['Biobank BIF'] != 'All'].melt(id_vars=['cohort_name_lower', 'Biobank BIF'], value_vars=['team_member_per', 'corresponding_per'])
melt['variable'] = melt['variable'].map({'team_member_per': 'Team', 'corresponding_per': 'PIs'})

plt.figure(figsize=(8, 6))
ax = sns.pointplot(data=melt, y='value', hue='Biobank BIF', x='variable', palette='colorblind', linewidth=2.5, errorbar='ci',
                   hue_order=['Bottom 20%', 'Top 20%'])
sns.move_legend(
    ax, "upper right",
    ncol=1, frameon=True, shadow=False, facecolor='white', edgecolor='white'
)
ax.set_ylim(0, 100)
ax.set_ylabel('Mentions (%)')
ax.set_title('Share of Research Impact Co-Authored by Biobank Team and PIs')
ax.set_xlabel('')
sns.despine()  # Removes top and right borders, trims remaining
plt.tight_layout()
plt.savefig('../../figures/local_impact/team_top_bottom.pdf')

dis_top = cohort_team[cohort_team['Biobank BIF'] == 'Bottom 20%']['team'].values
dis_bottom = cohort_team[cohort_team['Biobank BIF'] == 'Bottom 20%']['corresponding'].values
dis_num = cohort_team[cohort_team['Biobank BIF'] == 'Bottom 20%']['team'].values
t, p = ttest_ind(dis_top, dis_bottom)

# get p-values for the difference between the top 20% and bottom 20%
dis_top = same[same['Biobank BIF'] == 'Top 20%']['same_country'].values
dis_bottom = same[same['Biobank BIF'] == 'Bottom 20%']['same_country'].values
t, p = ttest_ind(dis_top, dis_bottom)
# get the 95-confidence interval of the mean of dis_top
top_mean = np.mean(dis_top)
bottom_mean = np.mean(dis_bottom)
top_std = np.std(dis_top)
bottom_std = np.std(dis_bottom)
n_top = len(dis_top)
n_bottom = len(dis_bottom)
top_se = top_std / np.sqrt(n_top)
bottom_se = bottom_std / np.sqrt(n_bottom)
top_ci = (top_mean - 1.96 * top_se, top_mean + 1.96 * top_se)
bottom_ci = (bottom_mean - 1.96 * bottom_se, bottom_mean + 1.96 * bottom_se)

dis_top = same[same['Biobank BIF'] == 'Top 20%']['same_org'].values
dis_bottom = same[same['Biobank BIF'] == 'Bottom 20%']['same_org'].values
t, p = ttest_ind(dis_top, dis_bottom)


melt = same[same['Biobank BIF'] != 'All'].melt(id_vars=['cohort_name_lower', 'Biobank BIF'], value_vars=['author_per', 'top_10_author_per'])
melt['variable'] = melt['variable'].map({'author_per': 'Top Author', 'top_10_author_per': 'Top-10 Authors'})

plt.figure(figsize=(8, 6))
ax = sns.pointplot(data=melt, y='value', hue='Biobank BIF', x='variable', palette='colorblind', linewidth=2.5, errorbar='ci',
                   hue_order=['Bottom 20%', 'Top 20%'])
sns.move_legend(
    ax, "upper left",
    ncol=1, frameon=True, shadow=False, facecolor='white', edgecolor='white'
)
ax.set_ylim(0, 100)
ax.set_ylabel('Mentions (%)')
ax.set_title('Provenance of Biobank Research Impact by BIF')
ax.set_xlabel('')
sns.despine()  # Removes top and right borders, trims remaining
plt.tight_layout()
plt.savefig('../../figures/local_impact/top_authors.pdf')

# get p-values for the difference between the top 20% and bottom 20%
dis_top = same[same['Biobank BIF'] == 'Top 20%']['same_country'].values
dis_bottom = same[same['Biobank BIF'] == 'Bottom 20%']['same_country'].values
t, p = ttest_ind(dis_top, dis_bottom)
# get the 95-confidence interval of the mean of dis_top
top_mean = np.mean(dis_top)
bottom_mean = np.mean(dis_bottom)
top_std = np.std(dis_top)
bottom_std = np.std(dis_bottom)
n_top = len(dis_top)
n_bottom = len(dis_bottom)
top_se = top_std / np.sqrt(n_top)
bottom_se = bottom_std / np.sqrt(n_bottom)
top_ci = (top_mean - 1.96 * top_se, top_mean + 1.96 * top_se)
bottom_ci = (bottom_mean - 1.96 * bottom_se, bottom_mean + 1.96 * bottom_se)

dis_top = same[same['Biobank BIF'] == 'Top 20%']['same_org'].values
dis_bottom = same[same['Biobank BIF'] == 'Bottom 20%']['same_org'].values
t, p = ttest_ind(dis_top, dis_bottom)