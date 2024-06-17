DECLARE study STRING;
DECLARE study_of STRING;
DECLARE biobank STRING;
DECLARE biobank_of STRING;
DECLARE bank STRING;
DECLARE bank_of STRING;
DECLARE biorepo STRING;
DECLARE biorepo_of STRING;
DECLARE cohort_project STRING;
DECLARE cohort_project_of STRING;
DECLARE survey STRING;
DECLARE survey_of STRING;
DECLARE registry STRING;
DECLARE registry_of STRING;
DECLARE programme STRING;
DECLARE programme_of STRING;
DECLARE research STRING;
DECLARE research_of STRING;
DECLARE program STRING;
DECLARE program_of STRING;
DECLARE consortium STRING;
DECLARE consortium_of STRING;
DECLARE network STRING;
DECLARE network_of STRING;

SET biobank = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]io[bB]ank))";
SET study = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Study))";
SET bank =  r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:(?:Tissue|Blood|Brain|Specimen|Milk)\sBank))";
SET biorepo = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]iorepository(?:\sNetwork)?))";
SET programme = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Programme))";
SET cohort_project = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Project))";
SET survey = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Survey))";
SET registry = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Registry))";
SET research = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Cohort))";
SET program = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Program))";
SET consortium = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Consortium))";  
SET network = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Network))";

SET biobank_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]io[bB]ank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET study_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Study)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET bank_of =  r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:(?:Tissue|Blood|Brain|Specimen|Milk)\sBank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET biorepo_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]iorepository(?:\sNetwork)?)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET programme_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Programme)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET cohort_project_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Project)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET survey_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Survey)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET registry_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Registry)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET research_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Cohort)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET program_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Program)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET consortium_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Consortium)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";  
SET network_of = r"(?i)\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Network)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z'’]+(?:\s|:|\.|$))){1,3}))?)";

CREATE OR REPLACE TABLE  `ccnr-success.cohorts.expanded_papers_lower` AS (

WITH
expanded_papers AS (
  SELECT
      CASE
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, study) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, study)
      WHEN REGEXP_CONTAINS(title.preferred, study) THEN REGEXP_EXTRACT_ALL(title.preferred, study)
      WHEN REGEXP_CONTAINS(abstract.preferred, study) THEN REGEXP_EXTRACT_ALL(abstract.preferred, study)
      WHEN REGEXP_CONTAINS(title.preferred, biobank) THEN REGEXP_EXTRACT_ALL(title.preferred, biobank)
      WHEN REGEXP_CONTAINS(abstract.preferred, biobank) THEN REGEXP_EXTRACT_ALL(abstract.preferred, biobank)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, biobank) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, biobank)
      WHEN REGEXP_CONTAINS(title.preferred, bank) THEN REGEXP_EXTRACT_ALL(title.preferred, bank)
      WHEN REGEXP_CONTAINS(abstract.preferred, bank) THEN REGEXP_EXTRACT_ALL(abstract.preferred, bank)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, bank) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, bank)
      WHEN REGEXP_CONTAINS(title.preferred, biorepo) THEN REGEXP_EXTRACT_ALL(title.preferred, biorepo)
      WHEN REGEXP_CONTAINS(abstract.preferred, biorepo) THEN REGEXP_EXTRACT_ALL(abstract.preferred, biorepo)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, biorepo) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, biorepo)
      WHEN REGEXP_CONTAINS(title.preferred, programme) THEN REGEXP_EXTRACT_ALL(title.preferred, programme)
      WHEN REGEXP_CONTAINS(abstract.preferred, programme) THEN REGEXP_EXTRACT_ALL(abstract.preferred, programme)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, programme) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, programme)
      WHEN REGEXP_CONTAINS(title.preferred, cohort_project) THEN REGEXP_EXTRACT_ALL(title.preferred, cohort_project)
      WHEN REGEXP_CONTAINS(abstract.preferred, cohort_project) THEN REGEXP_EXTRACT_ALL(abstract.preferred, cohort_project)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, cohort_project) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, cohort_project)
      WHEN REGEXP_CONTAINS(title.preferred, survey) THEN REGEXP_EXTRACT_ALL(title.preferred, survey)
      WHEN REGEXP_CONTAINS(abstract.preferred, survey) THEN REGEXP_EXTRACT_ALL(abstract.preferred, survey)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, survey) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, survey)
      WHEN REGEXP_CONTAINS(title.preferred, registry) THEN REGEXP_EXTRACT_ALL(title.preferred, registry)
      WHEN REGEXP_CONTAINS(abstract.preferred, registry) THEN REGEXP_EXTRACT_ALL(abstract.preferred, registry)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, registry) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, registry)
      WHEN REGEXP_CONTAINS(title.preferred, research) THEN REGEXP_EXTRACT_ALL(title.preferred, research)
      WHEN REGEXP_CONTAINS(abstract.preferred, research) THEN REGEXP_EXTRACT_ALL(abstract.preferred, research)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, research) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, research)
      WHEN REGEXP_CONTAINS(title.preferred, program) THEN REGEXP_EXTRACT_ALL(title.preferred, program)
      WHEN REGEXP_CONTAINS(abstract.preferred, program) THEN REGEXP_EXTRACT_ALL(abstract.preferred, program)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, program) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, program)
      WHEN REGEXP_CONTAINS(title.preferred, consortium) THEN REGEXP_EXTRACT_ALL(title.preferred, consortium)
      WHEN REGEXP_CONTAINS(abstract.preferred, consortium) THEN REGEXP_EXTRACT_ALL(abstract.preferred, consortium)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, consortium) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, consortium)
      WHEN REGEXP_CONTAINS(title.preferred, network) THEN REGEXP_EXTRACT_ALL(title.preferred, network)
      WHEN REGEXP_CONTAINS(abstract.preferred, network) THEN REGEXP_EXTRACT_ALL(abstract.preferred, network)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, network) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, network)
      END
      AS cohort_name,
  id

  FROM `dimensions-ai.data_analytics.publications` pc

  WHERE
  (
    REGEXP_CONTAINS(acknowledgements.preferred, study)
    OR REGEXP_CONTAINS(title.preferred, study)
    OR REGEXP_CONTAINS(abstract.preferred, study)
    OR REGEXP_CONTAINS(acknowledgements.preferred, biobank)
    OR REGEXP_CONTAINS(title.preferred, biobank)
    OR REGEXP_CONTAINS(abstract.preferred, biobank)
    OR REGEXP_CONTAINS(acknowledgements.preferred, bank)
    OR REGEXP_CONTAINS(title.preferred, bank)
    OR REGEXP_CONTAINS(abstract.preferred, bank)
    OR REGEXP_CONTAINS(acknowledgements.preferred, biorepo)
    OR REGEXP_CONTAINS(title.preferred, biorepo)
    OR REGEXP_CONTAINS(abstract.preferred, biorepo)
    OR REGEXP_CONTAINS(acknowledgements.preferred, programme)
    OR REGEXP_CONTAINS(title.preferred, programme)
    OR REGEXP_CONTAINS(abstract.preferred, programme)
    OR REGEXP_CONTAINS(acknowledgements.preferred, registry)
    OR REGEXP_CONTAINS(title.preferred, registry)
    OR REGEXP_CONTAINS(abstract.preferred, registry)
    OR REGEXP_CONTAINS(acknowledgements.preferred, cohort_project)
    OR REGEXP_CONTAINS(title.preferred, cohort_project)
    OR REGEXP_CONTAINS(abstract.preferred, cohort_project)
    OR REGEXP_CONTAINS(acknowledgements.preferred, survey)
    OR REGEXP_CONTAINS(title.preferred, survey)
    OR REGEXP_CONTAINS(abstract.preferred, survey)
    OR REGEXP_CONTAINS(acknowledgements.preferred, program)
    OR REGEXP_CONTAINS(title.preferred, program)
    OR REGEXP_CONTAINS(abstract.preferred, program)
    OR REGEXP_CONTAINS(acknowledgements.preferred, consortium)
    OR REGEXP_CONTAINS(title.preferred, consortium)
    OR REGEXP_CONTAINS(abstract.preferred, consortium)
    OR REGEXP_CONTAINS(acknowledgements.preferred, network)
    OR REGEXP_CONTAINS(title.preferred, network)
    OR REGEXP_CONTAINS(abstract.preferred, network)
  )
  AND
  (
    NOT REGEXP_CONTAINS(acknowledgements.preferred, study_of)
    AND NOT REGEXP_CONTAINS(title.preferred, study_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, study_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, biobank_of)
    AND NOT REGEXP_CONTAINS(title.preferred, biobank_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, biobank_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, bank_of)
    AND NOT REGEXP_CONTAINS(title.preferred, bank_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, bank_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, biorepo_of)
    AND NOT REGEXP_CONTAINS(title.preferred, biorepo_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, biorepo_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred,programme_of)
    AND NOT REGEXP_CONTAINS(title.preferred,programme_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred,programme_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, registry_of)
    AND NOT REGEXP_CONTAINS(title.preferred, registry_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, registry_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, cohort_project_of)
    AND NOT REGEXP_CONTAINS(title.preferred, cohort_project_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, cohort_project_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, survey_of)
    AND NOT REGEXP_CONTAINS(title.preferred, survey_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, survey_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, program_of)
    AND NOT REGEXP_CONTAINS(title.preferred, program_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, program_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, consortium_of)
    AND NOT REGEXP_CONTAINS(title.preferred, consortium_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, consortium_of)
    AND NOT REGEXP_CONTAINS(acknowledgements.preferred, network_of)
    AND NOT REGEXP_CONTAINS(title.preferred, network_of)
    AND NOT REGEXP_CONTAINS(abstract.preferred, network_of)
  )
  -- end of where
), -- end of expanded_papers

expanded_papers_of AS (
  SELECT
    CASE
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, study_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, study_of)
      WHEN REGEXP_CONTAINS(title.preferred, study_of) THEN REGEXP_EXTRACT_ALL(title.preferred, study_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, study_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, study_of)
      WHEN REGEXP_CONTAINS(title.preferred, biobank_of) THEN REGEXP_EXTRACT_ALL(title.preferred, biobank_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, biobank_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, biobank_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, biobank_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, biobank_of)
      WHEN REGEXP_CONTAINS(title.preferred, bank_of) THEN REGEXP_EXTRACT_ALL(title.preferred, bank_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, bank_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, bank_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, bank_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, bank_of)
      WHEN REGEXP_CONTAINS(title.preferred, biorepo_of) THEN REGEXP_EXTRACT_ALL(title.preferred, biorepo_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, biorepo_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, biorepo_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, biorepo_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, biorepo_of)
      WHEN REGEXP_CONTAINS(title.preferred, programme_of) THEN REGEXP_EXTRACT_ALL(title.preferred, programme_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, programme_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, programme_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, programme_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, programme_of)
      WHEN REGEXP_CONTAINS(title.preferred, cohort_project_of) THEN REGEXP_EXTRACT_ALL(title.preferred, cohort_project_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, cohort_project_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, cohort_project_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, cohort_project_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, cohort_project_of)
      WHEN REGEXP_CONTAINS(title.preferred, survey_of) THEN REGEXP_EXTRACT_ALL(title.preferred, survey_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, survey_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, survey_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, survey_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, survey_of)
      WHEN REGEXP_CONTAINS(title.preferred, registry_of) THEN REGEXP_EXTRACT_ALL(title.preferred, registry_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, registry_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, registry_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, registry_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, registry_of)
      WHEN REGEXP_CONTAINS(title.preferred, research_of) THEN REGEXP_EXTRACT_ALL(title.preferred, research_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, research_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, research_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, research_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, research_of)
      WHEN REGEXP_CONTAINS(title.preferred, consortium_of) THEN REGEXP_EXTRACT_ALL(title.preferred, consortium_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, consortium_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, consortium_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, consortium_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, consortium_of)
      WHEN REGEXP_CONTAINS(title.preferred, network_of) THEN REGEXP_EXTRACT_ALL(title.preferred, network_of)
      WHEN REGEXP_CONTAINS(abstract.preferred, network_of) THEN REGEXP_EXTRACT_ALL(abstract.preferred, network_of)
      WHEN REGEXP_CONTAINS(acknowledgements.preferred, network_of) THEN REGEXP_EXTRACT_ALL(acknowledgements.preferred, network_of)
      END
      AS cohort_name,
  id

  FROM `dimensions-ai.data_analytics.publications` pc

  WHERE
  (
    REGEXP_CONTAINS(acknowledgements.preferred, study_of)
    OR REGEXP_CONTAINS(title.preferred, study_of)
    OR REGEXP_CONTAINS(abstract.preferred, study_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, biobank_of)
    OR REGEXP_CONTAINS(title.preferred, biobank_of)
    OR REGEXP_CONTAINS(abstract.preferred, biobank_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, bank_of)
    OR REGEXP_CONTAINS(title.preferred, bank_of)
    OR REGEXP_CONTAINS(abstract.preferred, bank_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, biorepo_of)
    OR REGEXP_CONTAINS(title.preferred, biorepo_of)
    OR REGEXP_CONTAINS(abstract.preferred, biorepo_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred,programme_of)
    OR REGEXP_CONTAINS(title.preferred,programme_of)
    OR REGEXP_CONTAINS(abstract.preferred,programme_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, registry_of)
    OR REGEXP_CONTAINS(title.preferred, registry_of)
    OR REGEXP_CONTAINS(abstract.preferred, registry_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, cohort_project_of)
    OR REGEXP_CONTAINS(title.preferred, cohort_project_of)
    OR REGEXP_CONTAINS(abstract.preferred, cohort_project_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, survey_of)
    OR REGEXP_CONTAINS(title.preferred, survey_of)
    OR REGEXP_CONTAINS(abstract.preferred, survey_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, consortium_of)
    OR REGEXP_CONTAINS(title.preferred, consortium_of)
    OR REGEXP_CONTAINS(abstract.preferred, consortium_of)
    OR REGEXP_CONTAINS(acknowledgements.preferred, network_of)
    OR REGEXP_CONTAINS(title.preferred, network_of)
    OR REGEXP_CONTAINS(abstract.preferred, network_of)
  ) -- end of where
), -- end of expanded_papers_of

expanded_papers_all AS (
  SELECT 
    *
    FROM
      (
      SELECT *  
      FROM expanded_papers
      UNION ALL
      SELECT *
      FROM expanded_papers_of
      )
), -- end of expanded_papers_all

papers AS (
  SELECT
  REGEXP_REPLACE(REGEXP_REPLACE(cohort_name_ex, "’", "'"), r"\s$|\.$|:$", "") cohort_name,
  id
  FROM expanded_papers_all,
  UNNEST(cohort_name) cohort_name_ex
  GROUP BY 1,2
)
-- end of aliases

SELECT
ec.cohort_name,
ep.id

FROM
`ccnr-success.cohorts.expanded_cohorts` ec
LEFT JOIN papers ep
ON LOWER(ec.cohort_name) = ep.cohort_name
) -- end of create or replace table