WITH res_years AS (

SELECT
t.researcher_id,
t.cohort_name_lower,
min(p.year) res_year

FROM `ccnr-success.cohorts_expanded.cohort_papers` cp
LEFT JOIN `dimensions-ai.data_analytics.publications` p
ON cp.id = p.id,
UNNEST(researcher_ids) res
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_team` t
ON res = t.researcher_id AND cp.cohort_name_lower = t.cohort_name_lower


GROUP BY 1,2)

SELECT
t.researcher_id,
t.cohort_name_lower,
COUNT(DISTINCT p.id) publications,
SUM(p.citations_count) citations

FROM `dimensions-ai.data_analytics.publications` p,
UNNEST(researcher_ids) res
LEFT JOIN res_years t
ON res = t.researcher_id

WHERE p.year <= t.res_year

GROUP BY 1,2