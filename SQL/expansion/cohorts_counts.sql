WITH total_mentions AS (

SELECT
ep.cohort_name,
COUNT(DISTINCT id) mentions
FROM `ccnr-success.cohorts.expanded_papers` ep
GROUP BY cohort_name
-- LEFT JOIN `ccnr-success.cohorts.expanded_cohorts`

ORDER BY mentions DESC)
,
lower_mentions AS (

SELECT
ep.cohort_name,
COUNT(DISTINCT id) lower_mentions
FROM `ccnr-success.cohorts.expanded_papers_lower` ep
GROUP BY cohort_name
-- LEFT JOIN `ccnr-success.cohorts.expanded_cohorts`

ORDER BY lower_mentions DESC)
,
local_mentions AS (

SELECT
ep.cohort_name,
COUNT(DISTINCT id) local_mentions
FROM `ccnr-success.cohorts.expanded_papers_mentions` ep
GROUP BY cohort_name
-- LEFT JOIN `ccnr-success.cohorts.expanded_cohorts`

ORDER BY local_mentions DESC)
,
unique_mentions AS (

SELECT
ep.cohort_name,
COUNT(DISTINCT ep.id) unique_mentions

FROM `ccnr-success.cohorts.expanded_papers` ep
LEFT JOIN (
  SELECT
  id,
  COUNT(DISTINCT cohort_name) counter
  FROM `ccnr-success.cohorts.expanded_papers` ep
  GROUP BY id
) um
ON ep.id = um.id

WHERE um.counter = 1
GROUP BY cohort_name


ORDER BY unique_mentions DESC)
,
pmed_mentions AS (

SELECT
ep.cohort_name,
COUNT(DISTINCT ep.id) pmed_mentions

FROM `ccnr-success.cohorts.expanded_papers` ep
LEFT JOIN `dimensions-ai.data_analytics.publications` p
ON ep.id = p.id

WHERE
(
'Cohort Studies' IN UNNEST(p.mesh_headings)
OR 'Prospective Studies' IN UNNEST(p.mesh_headings)
OR 'Follow-Up Studies' IN UNNEST(p.mesh_headings)
OR 'Cross-Sectional Studies' IN UNNEST(p.mesh_headings)
OR 'Longitudinal Studies' IN UNNEST(p.mesh_headings)
OR 'Retrospective Studies' IN UNNEST(p.mesh_headings)
OR 'Biological Specimen Banks' IN UNNEST(p.mesh_headings)
OR 'Blood Banks' IN UNNEST(p.mesh_headings)
OR 'Milk Banks' IN UNNEST(p.mesh_headings)
OR 'Tissue Banks' IN UNNEST(p.mesh_headings)
OR 'Eye Banks' IN UNNEST(p.mesh_headings)
OR 'Bone Banks' IN UNNEST(p.mesh_headings)
OR 'Sperm Banks' IN UNNEST(p.mesh_headings)
)

GROUP BY cohort_name


ORDER BY pmed_mentions DESC)

SELECT
im.cohort_name,
cited_mention_citations search_mentions,
lm.local_mentions related_mentions,
tm.mentions,
lom.lower_mentions,
pm.pmed_mentions,
kind,


FROM `ccnr-success.cohorts.expanded_cohorts` im
LEFT JOIN local_mentions lm
ON im.cohort_name = lm.cohort_name
LEFT JOIN total_mentions tm
ON im.cohort_name = tm.cohort_name
LEFT JOIN lower_mentions lom
ON im.cohort_name = lom.cohort_name
LEFT JOIN unique_mentions um
ON im.cohort_name = um.cohort_name
LEFT JOIN pmed_mentions pm
ON im.cohort_name = pm.cohort_name

ORDER BY mentions DESC
