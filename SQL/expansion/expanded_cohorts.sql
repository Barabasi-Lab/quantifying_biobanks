DECLARE study STRING;
DECLARE biobank STRING;
DECLARE bank STRING;
DECLARE biorepo STRING;
DECLARE cohort_project STRING;
DECLARE survey STRING;
DECLARE registry STRING;
DECLARE programme STRING;
DECLARE research STRING;
DECLARE program STRING;
DECLARE consortium STRING;
DECLARE network STRING;

SET biobank = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]io[bB]ank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET study = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Study)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET bank =  r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:(?:Tissue|Blood|Brain|Specimen|Milk)\sBank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET biorepo = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]iorepository(?:\sNetwork)?)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET programme = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Programme)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET program = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Program)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET cohort_project = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Project)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET survey = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Survey)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET registry = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Registry)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET research = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Cohort)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET consortium = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Consortium)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";  
set network = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Network)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z'’]+(?:\s|:|\.|$))){1,3}))?)";



CREATE OR REPLACE TABLE `ccnr-success.cohorts.expanded_cohorts` AS (
WITH studies AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(title, study) THEN REGEXP_EXTRACT(title, study)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'study' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
REGEXP_CONTAINS(title, study)
)
GROUP BY 1, kind
ORDER BY cited_mention_citations DESC
)
,
biobanks AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, biobank) THEN REGEXP_EXTRACT(acknowledgements, biobank)
    WHEN REGEXP_CONTAINS(title, biobank) THEN REGEXP_EXTRACT(title, biobank)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'biobank' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
REGEXP_CONTAINS(acknowledgements, biobank)
OR
REGEXP_CONTAINS(title, biobank)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
banks AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, bank) THEN REGEXP_EXTRACT(acknowledgements, bank)
    WHEN REGEXP_CONTAINS(title, bank) THEN REGEXP_EXTRACT(title, bank)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'bank' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
  REGEXP_CONTAINS(acknowledgements, bank)
OR
REGEXP_CONTAINS(title, bank)
)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
biorepos AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, biorepo) THEN REGEXP_EXTRACT(acknowledgements, biorepo)
    WHEN REGEXP_CONTAINS(title, biorepo) THEN REGEXP_EXTRACT(title, biorepo)
    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'biorepo' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
  REGEXP_CONTAINS(acknowledgements, biorepo)
OR
REGEXP_CONTAINS(title, biorepo)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
proq AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(title, programme) THEN REGEXP_EXTRACT(title, programme)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'programme' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(

REGEXP_CONTAINS(title, programme)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
proj AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(title, cohort_project) THEN REGEXP_EXTRACT(title, cohort_project)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'project' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(

REGEXP_CONTAINS(title, cohort_project)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
registryq AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, registry) THEN REGEXP_EXTRACT(acknowledgements, registry)
    WHEN REGEXP_CONTAINS(title, registry) THEN REGEXP_EXTRACT(title, registry)
    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'registry' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
REGEXP_CONTAINS(acknowledgements, registry)
OR
REGEXP_CONTAINS(title, registry)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
surveyq AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(title, survey) THEN REGEXP_EXTRACT(title, survey)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'survey' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(

REGEXP_CONTAINS(title, survey)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
researchq AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(title, research) THEN REGEXP_EXTRACT(title, research)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'cohort' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(

REGEXP_CONTAINS(title, research)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
programq AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(title, program) THEN REGEXP_EXTRACT(title, program)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'program' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(

REGEXP_CONTAINS(title, program)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
consortiumq AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(acknowledgements, consortium) THEN REGEXP_EXTRACT(acknowledgements, consortium)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'consortium' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(

REGEXP_CONTAINS(acknowledgements, consortium)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
networkq AS (
SELECT

  CASE

    WHEN REGEXP_CONTAINS(acknowledgements, network) THEN REGEXP_EXTRACT(acknowledgements, network)

    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'network' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(

REGEXP_CONTAINS(acknowledgements, network)

)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)

SELECT 
REGEXP_REPLACE(REGEXP_REPLACE(cohort_name, "’", "'"), r"\s$|\.$|:$", "") cohort_name,
kind,
SUM(cited_mention_citations) cited_mention_citations

FROM
(
SELECT *  
FROM biobanks
UNION ALL
SELECT * FROM studies
UNION ALL
SELECT * FROM banks
UNION ALL
SELECT * FROM biorepos
UNION ALL
SELECT * FROM researchq
UNION ALL
SELECT * FROM surveyq
UNION ALL
SELECT * FROM proj
UNION ALL
SELECT * FROM registryq
UNION ALL
SELECT * FROM proq
UNION ALL
SELECT * FROM programq
UNION ALL
SELECT * FROM consortiumq
UNION ALL
SELECT * FROM networkq
)
GROUP BY 1, 2

ORDER BY 3 DESC)