WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn
    FROM `ccnr-success.biobanks.datasets`
),
TotalRows AS (
    SELECT MAX(rn) as total_rows
    FROM RowNumberedPublications
),
FirstHalfPublications AS (
    SELECT description AS input, id
    FROM RowNumberedPublications, TotalRows
    WHERE rn <= total_rows -- all rows
)
SELECT 
    publications_subset.id,
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(publications_subset.input, cohort_names.cohort_name)
