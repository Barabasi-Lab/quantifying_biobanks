CREATE TABLE `ccnr-success.cohorts.related_pubs` AS (

SELECT 

DISTINCT p.id,
CASE 
  WHEN pc.id IS NOT NULL OR pc.id = p.id THEN 1
  ELSE 0
  END AS related

FROM
`dimensions-ai.data_analytics.publications` p,
UNNEST(p.reference_ids) ref
LEFT JOIN
`ccnr-success.cohorts.papers_citations` pc
ON pc.id = ref

WHERE

p.year < 2024
AND
p.type = 'article')

