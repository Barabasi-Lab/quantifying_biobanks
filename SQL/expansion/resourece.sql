CREATE OR REPLACE TABLE `ccnr-success.cohorts_expanded.resource_google` AS (

WITH potential AS (

SELECT
publication_number AS id,
application_number,
country_code,
REGEXP_EXTRACT_ALL(d.text, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)") matches

    FROM `patents-public-data.patents.publications`,
    UNNEST(description_localized) AS d
    WHERE d.language = 'en'
    AND
    REGEXP_CONTAINS(d.text, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)")
)
,
resources AS (
SELECT
REGEXP_EXTRACT(pc.acknowledgements, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)") cohort_name,
COUNT(DISTINCT p.id) papers
FROM `ccnr-success.cohorts.papers_citations` pc
JOIN `dimensions-ai.data_analytics.publications` p
ON pc.id = p.id
WHERE REGEXP_CONTAINS(pc.acknowledgements, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)")
AND 'Humans' IN UNNEST(p.mesh_headings)
GROUP BY 1
ORDER BY 2 DESC
)

SELECT
id,
CONCAT('the ', LOWER(match)) cohort_name_lower,

FROM potential p,
UNNEST(matches) match
JOIN resources
ON match = resources.cohort_name
WHERE resources.papers >= 3

)

CREATE OR REPLACE TABLE `ccnr-success.cohorts_expanded.resource_papers` AS (

WITH potential AS (

SELECT
id,
REGEXP_EXTRACT_ALL(acknowledgements.preferred, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)") matches

FROM `dimensions-ai.data_analytics.publications`
WHERE REGEXP_CONTAINS(acknowledgements.preferred, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)")
)
,
resources AS (
SELECT
REGEXP_EXTRACT(pc.acknowledgements, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)") cohort_name,
COUNT(DISTINCT p.id) papers
FROM `ccnr-success.cohorts.papers_citations` pc
JOIN `dimensions-ai.data_analytics.publications` p
ON pc.id = p.id
WHERE REGEXP_CONTAINS(pc.acknowledgements, r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Resource)(?:\s[A-Z][a-z]+)?)")
AND 'Humans' IN UNNEST(p.mesh_headings)
GROUP BY 1
ORDER BY 2 DESC

)

SELECT
id,
CONCAT('the ', LOWER(match)) cohort_name_lower,

FROM potential p,
UNNEST(matches) match
JOIN resources
ON match = resources.cohort_name
WHERE resources.papers >= 3

)