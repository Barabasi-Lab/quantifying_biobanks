WITH patent2paper AS (

SELECT

m.id paper_id,
patent_id id

FROM
`ccnr-success.cohorts_expanded.papers` m,
UNNEST(m.patent_ids) patent_id


WHERE
patent_id IS NOT NULL),

patents AS (
  SELECT
  DISTINCT id
  FROM patent2paper
)

SELECT
m.id,
p.title,
p.publication_year,
ARRAY_LENGTH(cited_by_ids) patent_citation_count,
p.jurisdiction country,
p.assignee_countries,
p.assignee_orgs,
p.orange_book,
category_bra.values AS bra,
category_rcdc.values AS rcdc,
category_hrcs_hc.values AS hrcs_hc,
p.cpc,
researcher_ids,
reference_ids

FROM patents m
LEFT JOIN `dimensions-ai.data_analytics.patents` p
ON m.id = p.id
ORDER BY patent_citation_count DESC