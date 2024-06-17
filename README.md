# Quantifying the Impact of Biobanks and Cohort Studies

Accompanying code to produce and analyze the data from the paper _Quantifying the Impact of Biobanks and Cohort Studies_.

The associated data can be found in the corresponding [Zenodo Repository](10.5281/zenodo.11671293).

# Datasrouces

Several repositories were used to extract the names of biobanks and associated cohort studies, their mentions across biomedical documents, and their validation.

## Biobanks and Cohorts

- [BioLINCC](https://biolincc.nhlbi.nih.gov/studies/?s=rank&is_not_initial=Yes&q=&study_year_ranges=&study_year_ranges=&d=name&d=acronym&d=available_resources&d=cohort_type&d=is_public_use_dataset&d=objectives&d=publication_urls&d=date_open_data&d=date_open_specimens&d=study_year_ranges_text&d=study_type&d=subjects&d=conditions&page_size=500&so=name&so=acronym&so=available_resources&so=cohort_type&so=is_public_use_dataset&so=objectives&so=publication_urls&so=date_open_data&so=date_open_specimens&so=study_year_ranges_text&so=study_type&so=subjects&so=design)
- [BBMRI-ERIC](https://directory.bbmri-eric.eu/#/catalogue)
- [Birthcohorts](https://www.birthcohorts.net/birthcohorts/list/)
- [CEDC](https://cedcd.nci.nih.gov/) (Cancer Epidemiology Descriptive Cohort Database)
- [Cohort profiles and updates](https://academic.oup.com/ije/pages/General_Instructions#Cohort%20Profiles)
- [DCEG](https://dceg.cancer.gov/research/who-we-study/cohorts) (Division of Cancer Epidemiology & Genetics)
- [dbGaP](https://www.ncbi.nlm.nih.gov/gap/advanced_search/?OBJ=study&COND=%7B%22is_host_of_collection%22:%5B%22yes%22%5D%7D)
- [DPUK](https://portal.dementiasplatform.uk/) (Dementias Platform UK)
- [EPND](https://discover.epnd.org/) (European platform for neurodegenerative diseases)
- [IADRP](https://iadrp.nia.nih.gov/about/cadro/Population-Studies-Cohorts-and-Studies)
- [JPND](https://neurodegenerationresearch.eu/jpnd-global-cohort-portal/jpnd-global-cohort-portal-results/) (EU Join Program Neurodegenerative disease research)
- [Maelstrom](https://www.maelstrom-research.org/study/qlscd)
- [Molgenis](https://data-catalogue.molgeniscloud.org/catalogue/catalogue/#/networks-catalogue) (European Networks Health Data and Cohort Catalogue**)**)
- [P3](https://www.p3gobservatory.org/studylist.htm?reset=true) (Public Population Project in Genomics and Society)
- [SciCrunch](https://rrid.site/data/source/nlx_144509-1/search?q=%2A&l=&facet[]=Resource%20Type:biomaterial%20supply%20resource)
- [The Pooling Project of Prospective Studies of Diet and Cancer](https://www.hsph.harvard.edu/pooling-project/cohort-study-participants/)
- [UKRI](https://www.ukri.org/councils/mrc/facilities-and-resources/find-an-mrc-facility-or-resource/cohort-directory/) (UK research and innovation cohort directory)
- [Wikipedia biobanks](https://en.wikipedia.org/wiki/List_of_biobanks)
- [Wikipedia cohorts](https://en.wikipedia.org/wiki/Category:Cohort_studies)

## Mentions

The following databases were stored in Google BigQuery:

- [Dimensions](https://www.dimensions.ai/)
- [Google Patents](https://console.cloud.google.com/marketplace/product/google_patents_public_datasets/google-patents-public-data?project=baja-207222)

## Validation

- [NHGRI-EBI Catalog](https://www.ebi.ac.uk/gwas/)

## Analysis

- [MeSH Schema](https://www.nlm.nih.gov/databases/download/mesh.html)
- [Cooperative Patent Classification Scheme](https://www.cooperativepatentclassification.org/cpcSchemeAndDefinitions/bulk)
- [NIH funding by RCDC code](https://report.nih.gov/funding/categorical-spending#/)
