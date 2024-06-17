WITH policy2paper AS (
SELECT
p.id,
m.id paper_id

FROM `dimensions-ai.data_analytics.policy_documents` AS p,
UNNEST(p.cited_publication_ids) pub
LEFT JOIN `ccnr-success.cohorts_expanded.papers` m
ON pub = m.id
WHERE m.id IS NOT NULL)
,
pol AS (
  SELECT
  DISTINCT id
  FROM policy2paper
)

SELECT

pol.id,
p.title,
p.year,
category_bra.values AS bra,
category_rcdc.values AS rcdc,
category_hrcs_hc.values AS hrcs_hc,
p.publisher.name publisher,
p.publisher.country_code country,
p.publisher.grid_id publisher_id,
g.types publisher_type,
g.organization_parent_ids publisher_parent_ids,
p.cited_publication_ids publication_ids

FROM pol
LEFT JOIN
`dimensions-ai.data_analytics.policy_documents` p
ON pol.id = p.id
LEFT JOIN `dimensions-ai.data_analytics.grid` g
ON p.publisher.grid_id = g.id