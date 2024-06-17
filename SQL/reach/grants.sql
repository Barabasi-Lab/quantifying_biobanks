WITH paper2grant AS (
SELECT
p.id,
g grant_id

FROM
`ccnr-success.cohorts_expanded.papers` p,
UNNEST(p.supporting_grant_ids) g
WHERE
g IS NOT NULL)
,
grants AS (
  SELECT
  DISTINCT grant_id
  FROM paper2grant
)

SELECT
r.grant_id,
title,
activity_code,
funding_usd,
start_year,
end_year,
funder_org,
funder_org_countries,
researcher_ids,
research_orgs,
ARRAY(SELECT STRUCT(researcher_id, role) FROM UNNEST(investigators) WHERE researcher_id IS NOT NULL) investigators,
category_bra.values AS bra,
category_rcdc.values AS rcdc,
category_hrcs_hc.values AS hrcs_hc,
resulting_publication_ids

FROM grants r
LEFT JOIN `dimensions-ai.data_analytics.grants` g
ON r.grant_id = g.id