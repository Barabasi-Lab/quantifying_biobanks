DECLARE study STRING;
DECLARE biobank STRING;
DECLARE bank STRING;
DECLARE biorepo STRING;
DECLARE cohort_project STRING;
DECLARE survey STRING;
DECLARE registry STRING;
DECLARE programme STRING;
DECLARE research STRING;

SET biobank = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]io[bB]ank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";

SET study = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Study)(?:(?:\sof\s)(?:(?:[A-Z][a-z]+(?:\s|:|$))){1,3})?)";
SET bank =  r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:(?:Tissue|Blood|Brain|Specimen|Milk)\sBank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET biorepo = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]iorepository(?:\sNetwork)?)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET programme = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Programme)(?:(?:\sof\s)(?:(?:[A-Z][a-z]+(?:\s|:|$))){1,3})?)";
SET cohort_project = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Project)(?:(?:\sof\s)(?:(?:[A-Z][a-z]+(?:\s|:|$))){1,3})?)";

SET survey = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Survey)(?:(?:\sof\s)(?:(?:[A-Z][a-z]+(?:\s|:|$))){1,3})?)";
SET registry = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Registry)(?:(?:\sof\s)(?:(?:[A-Z][a-z]+(?:\s|:|$))){1,3})?)";
SET research = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Cohort)(?:(?:\sof\s)(?:(?:[A-Z][a-z]+(?:\s|:|$))){1,3})?)";




CREATE OR REPLACE TABLE `ccnr-success.cohorts.expanded_cohorts` AS (
WITH studies AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, study) THEN REGEXP_EXTRACT(acknowledgements, study)
    WHEN REGEXP_CONTAINS(title, study) THEN REGEXP_EXTRACT(title, study)
    WHEN REGEXP_CONTAINS(abstract, study) THEN REGEXP_EXTRACT(abstract, study)
    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'study' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
--   REGEXP_CONTAINS(acknowledgements, study)
-- OR
REGEXP_CONTAINS(title, study)
)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
biobanks AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, biobank) THEN REGEXP_EXTRACT(acknowledgements, biobank)
    WHEN REGEXP_CONTAINS(title, biobank) THEN REGEXP_EXTRACT(title, biobank)
    WHEN REGEXP_CONTAINS(abstract, biobank) THEN REGEXP_EXTRACT(abstract, biobank)
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
-- OR REGEXP_CONTAINS(abstract, biobank)
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
    WHEN REGEXP_CONTAINS(abstract, bank) THEN REGEXP_EXTRACT(abstract, bank)
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
    WHEN REGEXP_CONTAINS(abstract, biorepo) THEN REGEXP_EXTRACT(abstract, biorepo)
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
-- OR REGEXP_CONTAINS(abstract, biorepo)
)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
proq AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, programme) THEN REGEXP_EXTRACT(acknowledgements, programme)
    WHEN REGEXP_CONTAINS(title, programme) THEN REGEXP_EXTRACT(title, programme)
    WHEN REGEXP_CONTAINS(abstract, programme) THEN REGEXP_EXTRACT(abstract, programme)
    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'programme' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
--  REGEXP_CONTAINS(acknowledgements, programme)
-- OR
REGEXP_CONTAINS(title, programme)
--OR REGEXP_CONTAINS(abstract, programme)
)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
proj AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, cohort_project) THEN REGEXP_EXTRACT(acknowledgements, cohort_project)
    WHEN REGEXP_CONTAINS(title, cohort_project) THEN REGEXP_EXTRACT(title, cohort_project)
    WHEN REGEXP_CONTAINS(abstract, cohort_project) THEN REGEXP_EXTRACT(abstract, cohort_project)
    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'project' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
--  REGEXP_CONTAINS(acknowledgements, programme)
-- OR
REGEXP_CONTAINS(title, cohort_project)
--OR REGEXP_CONTAINS(abstract, programme)
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
    WHEN REGEXP_CONTAINS(abstract, registry) THEN REGEXP_EXTRACT(abstract, registry)
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
--OR REGEXP_CONTAINS(abstract, programme)
)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
surveyq AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, survey) THEN REGEXP_EXTRACT(acknowledgements, survey)
    WHEN REGEXP_CONTAINS(title, survey) THEN REGEXP_EXTRACT(title, survey)
    WHEN REGEXP_CONTAINS(abstract, survey) THEN REGEXP_EXTRACT(abstract, survey)
    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'survey' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
-- REGEXP_CONTAINS(acknowledgements, survey)
-- OR
REGEXP_CONTAINS(title, survey)
--OR REGEXP_CONTAINS(abstract, programme)
)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)
,
researchq AS (
SELECT

  CASE
    WHEN REGEXP_CONTAINS(acknowledgements, research) THEN REGEXP_EXTRACT(acknowledgements, research)
    WHEN REGEXP_CONTAINS(title, research) THEN REGEXP_EXTRACT(title, research)
    WHEN REGEXP_CONTAINS(abstract, research) THEN REGEXP_EXTRACT(abstract, research)
    END
    AS cohort_name,

COUNT(id) cited_mention_citations,
'cohort' AS kind

FROM `ccnr-success.cohorts.papers_citations` pc

WHERE

(
-- REGEXP_CONTAINS(acknowledgements, survey)
-- OR
REGEXP_CONTAINS(title, research)
--OR REGEXP_CONTAINS(abstract, programme)
)
GROUP BY 1
ORDER BY cited_mention_citations DESC
)


SELECT 
*

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
)


ORDER BY cited_mention_citations DESC)