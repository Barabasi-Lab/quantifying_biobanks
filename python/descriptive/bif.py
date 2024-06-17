import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.2)

target = pd.read_csv('../../data/expansion/database/cohort_impact/target.csv')

replace = {
    'the uk biobank': 'UK Biobank',
    'the diabetes prevention program': 'DPP',
    'the national health and nutrition examination survey': 'NHANES',
    "the women's health initiative": 'WHI',
    'the human microbiome project': 'HMP',
    'the tcga research network': 'TCGA',
    'the european collection of cell cultures': 'ECACC',
    'the framingham heart study': 'FHS',
    'the genotype-tissue expression project': 'GTEx',
    'the health and retirement study': 'HRS',
    'the atherosclerosis risk in communities': 'ARIC',
    'the multi-ethnic study of atherosclerosis': 'MESA',
    'the national health interview survey': 'NHIS',
    "the alzheimer's disease neuroimaging initiative": 'ADNI',
    'the hapmap project': 'HapMap',
    'the hispanic community health study': 'HCHS/SOL',
    'the labour force survey': 'LFS',
    "the nurses' health study": 'NHS',
    'the all of us research program': 'All of Us',
    "the special supplemental nutrition program": 'SNAP',
    'the avon longitudinal study': 'ALSPAC',
    'the cardiovascular health study': 'CHS',
    'the european prospective investigation into cancer and nutrition': 'EPIC',
}

target['biobank'] = target['cohort_name_lower'].replace(replace)
# drop SNAP and LFS
target = target[target['biobank'] != 'SNAP']
target = target[target['biobank'] != 'LFS']
target = target[target['biobank'] != 'NHIS']

top = target[['biobank', 'impact', 'disease', 'target']].head(20)
# rename target to BIF
top = top.rename(columns={'target': 'BIF'})
data = top

fig, axes = plt.subplots(ncols=3, sharey=True, figsize=(15, 8))

# Plot for disease
axes[0].scatter(data['disease'], data['biobank'], color='blue', s=100)
axes[0].set_title('Disease Scope and Depth')
axes[0].set_xlabel('Value')
axes[0].set_ylabel('Biobank')

# Plot for impact
axes[1].scatter(data['impact'], data['biobank'], color='red', s=100)
axes[1].set_title('Impact')
axes[1].set_xlabel('Value')

# Plot for BIF
axes[2].scatter(data['BIF'], data['biobank'], color='green', s=100)
axes[2].set_title('Biobank Impact Factor')
axes[2].set_xlabel('Value')

# Reverse the order of the y-axis
axes[0].invert_yaxis()

# Remove the main title
fig.suptitle('')

fig.savefig('../../figures/mentions+reach/BIF.pdf')