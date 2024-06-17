CREATE OR REPLACE TABLE `ccnr-success.cohorts.papers` AS (

SELECT
m.id,
doi,
type,
year,
citations_count,
reference_ids,
altmetrics,
supporting_grant_ids,
patent_ids,
research_orgs,
research_org_cities,
research_org_countries,
ARRAY(SELECT STRUCT(researcher_id, corresponding) FROM UNNEST(authors)) authors,
citations,
journal.title journal,
journal.title journal_id,
title.preferred title,
pubmed.mesh.headings mesh_headings,
pubmed.mesh.ui mesh_ids,
category_bra.values AS bra,
category_rcdc.values AS rcdc,
category_hrcs_hc.values AS hrcs_hc,
clinical_trial_ids

FROM
`ccnr-success.cohorts.papers` m
LEFT JOIN
`dimensions-ai.data_analytics.publications` p
ON m.id = p.id

ORDER BY
citations_count DESC)