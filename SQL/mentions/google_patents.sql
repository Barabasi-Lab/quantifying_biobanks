CREATE TABLE `ccnr-success.biobanks.google_patents_uncased` AS (

WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn, d.text AS description_text
    FROM `patents-public-data.patents.publications`,
    UNNEST(description_localized) AS d
),
TotalRows AS (
    SELECT MAX(rn) as total_rows
    FROM RowNumberedPublications
),
FirstHalfPublications AS (
    SELECT description_text AS input,
    publication_number AS id,
    application_number,
    country_code
    FROM RowNumberedPublications, TotalRows
    WHERE 
    rn <= total_rows
)
SELECT 
    publications_subset.id,
    publications_subset.application_number,
    publications_subset.country_code,
    cohort_names.cohort_name,
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(LOWER(publications_subset.input), cohort_names.cohort_name_lower)
)

CREATE TABLE `ccnr-success.biobanks.google_patents_no_the` AS (

WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn, d.text AS description_text
    FROM `patents-public-data.patents.publications`,
    UNNEST(description_localized) AS d
),
TotalRows AS (
    SELECT MAX(rn) as total_rows
    FROM RowNumberedPublications
),
FirstHalfPublications AS (
    SELECT description_text AS input,
    publication_number AS id,
    application_number,
    country_code
    FROM RowNumberedPublications, TotalRows
    WHERE 
    rn <= total_rows
)
SELECT 
    publications_subset.id,
    publications_subset.application_number,
    publications_subset.country_code,
    cohort_names.cohort_name,
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(publications_subset.input, SUBSTR(cohort_names.cohort_name, 8))
)

CREATE TABLE `ccnr-success.biobanks.google_patents` AS (

WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn, d.text AS description_text
    FROM `patents-public-data.patents.publications`,
    UNNEST(description_localized) AS d
),
TotalRows AS (
    SELECT MAX(rn) as total_rows
    FROM RowNumberedPublications
),
FirstHalfPublications AS (
    SELECT description_text AS input,
    publication_number AS id,
    application_number,
    country_code
    FROM RowNumberedPublications, TotalRows
    WHERE 
    rn <= total_rows
)
SELECT 
    publications_subset.id,
    publications_subset.application_number,
    publications_subset.country_code,
    cohort_names.cohort_name,
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(publications_subset.input, cohort_names.cohort_name)
)

CREATE TABLE `ccnr-success.biobanks.google_patents_no_apost` AS (

WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn, d.text AS description_text
    FROM `patents-public-data.patents.publications`,
    UNNEST(description_localized) AS d
    WHERE d.language = 'en'
),
TotalRows AS (
    SELECT MAX(rn) as total_rows
    FROM RowNumberedPublications
),
FirstHalfPublications AS (
    SELECT description_text AS input,
    publication_number AS id,
    application_number,
    country_code
    FROM RowNumberedPublications, TotalRows
    WHERE 
    rn <= total_rows
)
SELECT 
    publications_subset.id,
    publications_subset.application_number,
    publications_subset.country_code,
    cohort_names.cohort_name,
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(LOWER(publications_subset.input), REGEXP_REPLACE(cohort_names.cohort_name_lower, "'", "&#39;"))
)

WITH RowNumberedPublications AS (
    SELECT *, ROW_NUMBER() OVER() as rn
    FROM `ccnr-success.biobanks.patents`
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
    cohort_name_lower
FROM `ccnr-success.biobanks.cohort-names` AS cohort_names
JOIN FirstHalfPublications AS publications_subset
ON REGEXP_CONTAINS(LOWER(publications_subset.input), cohort_names.cohort_name_lower)