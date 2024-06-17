import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import countrynames
import spacy
import plotly.express as px

def get_initials(name):
    doc = nlp(name)
    words = []
    for chunk in doc:
       if chunk.pos_ not in ['CCONJ', 'ADP',  'SYM', 'AUX', 'DET', 'PUNCT', 'PART']:
           if len(chunk.norm_) == 2:
               words.append(chunk.norm_.upper())
           else:
               words.append(chunk.norm_[0].upper())
    initials = ''.join(words)

    return initials

nlp = spacy.load('en_core_web_sm')
cohorts = pd.read_csv('../../data/expansion/cohorts.csv')
cohorts['biobank'] = cohorts['cohort_name_lower'].apply(get_initials)
cohort_initials = cohorts[['cohort_name_lower', 'biobank']]
# save to csv
cohort_initials.to_csv('../../data/expansion/cohort_initials.csv', index=False)

countries = pd.read_csv('../../data/expansion/database/cohort_data/cohort_places.csv')
con = countries.cohort_place.unique()
con2code = {x: countrynames.to_code(x) for x in con if countrynames.to_code(x) is not None}
countries['country'] = countries['cohort_place'].apply(lambda x: con2code[x] if x in con2code else np.nan)
countries = countries.dropna(subset=['country'])
origin = countries.groupby('country').cohort_name_lower.nunique().rename('biobanks_origin').reset_index()
country_impact = pd.read_csv('../../data/expansion/database/cohort_impact/country_impact.csv')
use = country_impact.groupby('country').cohort_name_lower.nunique().rename('biobanks_use').reset_index()
country = origin.merge(use, on='country', how='outer').fillna(0)
# save to descriptive folder
country.to_csv('../../data/expansion/database/descriptive/country_biobanks.csv', index=False)
country['iso-3'] = country.country.apply(countrynames.to_code_3)
country.replace(0, np.nan, inplace=True)

# Create the map
fig_origin = px.choropleth(
    country,
    locations='iso-3',
    locationmode='ISO-3',
    color=np.log2(country['biobanks_origin']),
    hover_name='country',
    color_continuous_scale=px.colors.sequential.dense,
    projection='natural earth',
    title='Global Distribution of Biobank Origins',
    height=600
)

# Adjust map aesthetics to show all countries
fig_origin.update_geos(
    showframe=True,  # Remove the frame
    showcoastlines=True,  # Show coastlines for better country delineation
    coastlinecolor='Gray',  # Light gray coastline color
    landcolor='white',  # Light background color
    lakecolor='white',  # Light water color
    visible=True, # Show all countries, including those with no data
    scope='world',  # Set the map scope to world
    lataxis_range=[-59, 90]
)

# Update the colorbar to use a continuous logarithmic scale
ticks = [1, 5, 20, 80, 250]
fig_origin.update_layout(
    coloraxis_colorbar=dict(
        title='Biobank cohorts',
        tickvals=[np.log2(x) for x in ticks],  # Log scale ticks
        ticktext=[str(x) for x in ticks],  # Match tickvals
        thicknessmode="pixels", thickness=20,
        lenmode="pixels", len=200,  # Adjusted for better visibility
        bgcolor="rgba(255,255,255,0.8)"  # Semi-transparent background for readability
    )
)

fig_origin.show()
fig_origin.write_image('../../figures/world/biobank_origins.pdf')
fig_origin.write_image('../../figures/world/biobank_origins.png')

# Adjust map aesthetics to show all countries
fig_origin.update_geos(
    showframe=True,  # Remove the frame
    showcoastlines=True,  # Show coastlines for better country delineation
    coastlinecolor='Gray',  # Light gray coastline color
    landcolor='white',  # Light background color
    lakecolor='white',  # Light water color
    visible=True, # Show all countries, including those with no data
    scope='europe',  # Set the map scope to Europe
    lataxis_range=[-59, 90]
)
fig_origin.write_image('../../figures/world/biobank_origins_europe.pdf')
fig_origin.write_image('../../figures/world/biobank_origins_europe.png')

log2 = np.log2(country['biobanks_use'])
# Create the map
fig_origin = px.choropleth(
    country,
    locations='iso-3',
    locationmode='ISO-3',
    color=log2,
    hover_name='country',
    color_continuous_scale=px.colors.sequential.dense,
    projection='natural earth',
    title='Global Distribution of Biobank Origins',
    height=600
)

# Adjust map aesthetics to show all countries
fig_origin.update_geos(
    showframe=True,  # Remove the frame
    showcoastlines=True,  # Show coastlines for better country delineation
    coastlinecolor='Gray',  # Light gray coastline color
    landcolor='white',  # Light background color
    lakecolor='white',  # Light water color
    visible=True, # Show all countries, including those with no data
    scope='world',  # Set the map scope to Europe
    lataxis_range=[-59, 90]
)

# Update the colorbar to use a continuous logarithmic scale
ticks = [1, 10, 100, 1000]
fig_origin.update_layout(
    coloraxis_colorbar=dict(
        title='Biobanks used',
        thicknessmode="pixels", thickness=20,
        tickvals=[np.log2(x) for x in ticks],  # Log scale ticks
        ticktext=[str(x) for x in ticks],  # Match tickvals
        lenmode="pixels", len=200,  # Adjusted for better visibility
        bgcolor="rgba(255,255,255,0.8)"  # Semi-transparent background for readability
    )
)

fig_origin.show()
fig_origin.write_image('../../figures/world/biobank_use.pdf')
fig_origin.write_image('../../figures/world/biobank_use.png')
# Adjust map aesthetics to show all countries
fig_origin.update_geos(
    showframe=True,  # Remove the frame
    showcoastlines=True,  # Show coastlines for better country delineation
    coastlinecolor='Gray',  # Light gray coastline color
    landcolor='white',  # Light background color
    lakecolor='white',  # Light water color
    visible=True, # Show all countries, including those with no data
    scope='europe',  # Set the map scope to Europe
    lataxis_range=[-59, 90]
)
fig_origin.write_image('../../figures/world/biobank_use_europe.pdf')
fig_origin.write_image('../../figures/world/biobank_use_europe.png')



