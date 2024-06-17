import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import boxcox

pis = pd.read_csv('../../data/expansion/database/descriptive/PIs_papers_citations.csv')
cohort_pis = pis.groupby('cohort_name_lower').agg({'publications': 'sum', 'citations': 'max'}).reset_index().dropna()
cohort_pis['PI_high_impact'] = 0
cohort_pis['PI_low_impact'] = 0
cohort_pis.loc[cohort_pis['citations'] > pis.citations.quantile(.9), 'PI_high_impact'] = 1
cohort_pis.loc[cohort_pis['citations'] < pis.citations.quantile(.1), 'PI_low_impact'] = 1
# drop publications and citations
cohort_pis = cohort_pis.drop(['publications', 'citations'], axis=1)


features = pd.read_csv('../../data/expansion/database/cohort_data/features.csv')
# drop country column
features['population'] = features['type'].replace({'population': 1, 'health': 0})
features['large_cohort'] = (features['cohort_size'] > features['cohort_size'].quantile(0.9)) * 1
features['open_data_high'] = (features['open_index'] > features['open_index'].quantile(0.9)) * 1
features['open_data_low'] = (features['open_index'] < features['open_index'].quantile(0.1)) * 1
# drop
features = features.drop(['type', 'cohort_size', 'age_cat', 'country', 'open_index', 'enviromental'], axis=1)

target = pd.read_csv('../../data/expansion/database/cohort_impact/target.csv')

cohorts = features.merge(target[['cohort_name_lower', 'outlier', 'target', 'impact', 'disease']], on='cohort_name_lower', how='left')
cohorts = cohorts.merge(cohort_pis, on='cohort_name_lower', how='left')
cohorts = cohorts.dropna()
y = cohorts['target']
X = cohorts.drop(['cohort_name_lower', 'outlier', 'target', 'impact', 'disease'], axis=1)
X_const = sm.add_constant(X)
y_transformed = np.log(y + 1)
glm_model = sm.GLM(y_transformed, X_const, family=sm.families.Gaussian(link=sm.genmod.families.links.Identity())).fit()
print(glm_model.summary())
# Extracting p-values for each coefficient
p_values = glm_model.pvalues
bonferroni_correction = 0.05 / len(X_const.columns)
significant_features = p_values[p_values < bonferroni_correction]
print("\nFeatures significant after Bonferroni correction:")
print(significant_features)

sns.kdeplot(y_transformed)
renamed_columns = {
    'open_index_2': 'open_data_high', 
    'open_index_1': 'open_data_mid', 
    'open_index_0': 'open_data_low',
    'cohort_size_2': 'cohort_size_large', 
    'cohort_size_1': 'cohort_size_mid', 
    'cohort_size_0': 'cohort_size_small',
    'const': 'intercept', 
    'population': 'population_based'
}

# Apply Seaborn styles for better aesthetics
sns.set_theme(style="whitegrid")


fig, ax = plt.subplots(figsize=(12, 8))

# Indices for the bars
indices = np.arange(len(glm_model.params))

# Bar colors: red for significant coefficients, blue for others
colors = ['#fe6f5e' if p < bonferroni_correction else '#318ce7' for p in glm_model.pvalues]

# Plot bars for coefficients
ax.barh(indices, glm_model.params, color=colors, xerr=(glm_model.conf_int()[1] - glm_model.params), capsize=5, align='center', edgecolor='black')

# Set the y-axis with the renamed labels, marking significant ones
ax.set_yticks(indices)
ax.set_yticklabels([f"{renamed_columns.get(col, col)}{' *' if p < bonferroni_correction else ''}" for col, p in zip(X_const.columns, glm_model.pvalues)])

# Improve the appearance of y-axis labels
plt.setp(ax.get_yticklabels(), rotation=0, horizontalalignment='right')

# Draw a vertical line at 0 to show the baseline
ax.axvline(x=0, color='grey', linestyle='--', linewidth=1)

# Set labels and title for clarity
ax.set_xlabel('Coefficient Value', fontsize=14)
ax.set_title('GLM Coefficients with Statistical Significance Indicated (*)', fontsize=16)

plt.tight_layout()
plt.show()

glm_model.save('../../data/expansion/database/cohort_impact/glm_model.pkl')