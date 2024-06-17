SELECT
g.id,
cohort_names.cohort_name_lower
FROM
`dimensions-ai.data_analytics.policy_documents` g
CROSS JOIN
UNNEST(g.concepts) AS keyword
JOIN `ccnr-success.biobanks.cohort-names` AS cohort_names
ON SUBSTR(cohort_names.cohort_name_lower, 5) = LOWER(keyword.concept)

-- titles
WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn
    FROM `ccnr-success.biobanks.policy_documents`
),
TotalRows AS (
    SELECT MAX(rn) as total_rows
    FROM RowNumberedPublications
),
FirstHalfPublications AS (
    SELECT title AS input, id
    FROM RowNumberedPublications, TotalRows
    WHERE 
    rn > total_rows / 3
    AND
    rn <= 2 * total_rows / 3
)
SELECT 
    publications_subset.id,
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(LOWER(publications_subset.input), cohort_names.cohort_name_lower)