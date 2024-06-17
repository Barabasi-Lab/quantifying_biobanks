SELECT
g.id,
cohort_names.cohort_name_lower
FROM
`dimensions-ai.data_analytics.grants` g
CROSS JOIN
UNNEST(g.keywords) AS keyword
JOIN `ccnr-success.biobanks.cohort-names` AS cohort_names
ON SUBSTR(cohort_names.cohort_name_lower, 5) = LOWER(keyword.value)

WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn
    FROM `ccnr-success.biobanks.grants`
),
TotalRows AS (
    SELECT MAX(rn) as total_rows
    FROM RowNumberedPublications
),
FirstHalfPublications AS (
    SELECT abstract AS input, id
    FROM RowNumberedPublications, TotalRows
    WHERE 
    rn <= total_rows
)
SELECT 
    publications_subset.id,
    cohort_names.cohort_name,
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(LOWER(publications_subset.input), cohort_names.cohort_name_lower)