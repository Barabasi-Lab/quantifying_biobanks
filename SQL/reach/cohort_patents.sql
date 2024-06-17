SELECT
p.id,
m.cohort_name_lower

FROM `dimensions-ai.data_analytics.patents` AS p,
UNNEST(p.publication_ids) pub
JOIN `ccnr-success.cohorts_expanded.cohort_papers` m
ON pub = m.id