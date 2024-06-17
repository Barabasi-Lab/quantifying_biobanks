WITH biobanks AS (

SELECT

REGEXP_EXTRACT(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Bio[Bb]ank)\b") cohort_name,
'biobank' AS kind,
COUNT(id) papers,
FROM `dimensions-ai.data_analytics.publications`
WHERE
(

REGEXP_CONTAINS(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Bio[Bb]ank)\b")
AND
year < 2020

)
GROUP BY 1
ORDER BY 2 DESC

),
biorepositories AS (

SELECT

REGEXP_EXTRACT(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Biorepository)\b(?:\s(?:(?:[A-Z][a-z\dA-Z]+|for|at|of|and|the))){0,5}") cohort_name,
'biorepository' AS kind,
COUNT(id) papers
FROM `dimensions-ai.data_analytics.publications`
WHERE
(

REGEXP_CONTAINS(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Biorepository)\b(\s(([A-Z][a-z\dA-Z]+|for|at|of|and|the))){0,5}")
AND
year < 2020

)
GROUP BY 1
ORDER BY 2 DESC
),
studies AS (

SELECT

REGEXP_EXTRACT(title.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Study)\b") cohort_name,
'study' AS kind,
COUNT(id) papers
FROM `dimensions-ai.data_analytics.publications`
WHERE
(

REGEXP_CONTAINS(title.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(Study)\b")
AND
REGEXP_CONTAINS(LOWER(abstract.preferred), r"(prospective|longitudinal|retrospective|cross[\-\s]?sectional)\scohort")
AND
year < 2020

)
GROUP BY 1
ORDER BY 2 DESC
),

health_studies AS (
SELECT

REGEXP_EXTRACT(title.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Health Study)\b") cohort_name,
'health_study' AS kind,
COUNT(id) papers
FROM `dimensions-ai.data_analytics.publications`
WHERE
(

REGEXP_CONTAINS(title.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(Health Study)\b")
AND
REGEXP_CONTAINS(LOWER(abstract.preferred), r"(prospective|longitudinal|retrospective|cross[\-\s]?sectional)\scohort")
AND
year < 2020

)
GROUP BY 1
ORDER BY 2 DESC
),

cohort_studies AS (
SELECT

REGEXP_EXTRACT(title.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Cohort Study)\b") cohort_name,
'cohort_study' AS kind,
COUNT(id) papers
FROM `dimensions-ai.data_analytics.publications`
WHERE
(

REGEXP_CONTAINS(title.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Cohort Study)\b")
AND
REGEXP_CONTAINS(LOWER(abstract.preferred), r"(prospective|longitudinal|retrospective|cross[\-\s]?sectional)\scohort")
AND
year < 2020
)
GROUP BY 1
ORDER BY 2 DESC),

biobanks_of AS (
SELECT

REGEXP_EXTRACT(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Bio[bB]ank)\b\sof(?:\s(?:[A-Z][a-z\-\'’]+)){1,3}"),
'biobank_of' AS kind,
COUNT(id) papers
FROM `dimensions-ai.data_analytics.publications`
WHERE
(

REGEXP_CONTAINS(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Bio[Bb]ank)\b\sof(\s([A-Z][a-z\-\'’]+)){1,3}")


)
GROUP BY 1
ORDER BY 2 DESC
),
biobanks_at AS (
SELECT

REGEXP_EXTRACT(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Bio[bB]ank)\b\sof(?:\s(?:[A-Z][a-z\-\'’]+)){1,3}"),
'biobank_of' AS kind,
COUNT(id) papers
FROM `dimensions-ai.data_analytics.publications`
WHERE
(

REGEXP_CONTAINS(abstract.preferred, r"[Tt]he\s[A-Z](?:[\w\-\']+\s){1,7}(?:Bio[Bb]ank)\b\sof(\s([A-Z][a-z\-\'’]+)){1,3}")


)
GROUP BY 1
ORDER BY 2 DESC
)

-- concatenate the results
SELECT * FROM biobanks
UNION ALL
SELECT * FROM biobanks_of
UNION ALL
SELECT * FROM biobanks_at
UNION ALL
SELECT * FROM biorepositories
UNION ALL
SELECT * FROM studies
UNION ALL
SELECT * FROM health_studies
UNION ALL
SELECT * FROM cohort_studies
