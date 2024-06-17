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

SET biobank = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]io[bB]ank))";
SET study = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Study))";
SET bank =  r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:(?:Tissue|Blood|Brain|Specimen|Milk)\sBank))";
SET biorepo = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]iorepository(?:\sNetwork)?))";
SET programme = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Programme))";
SET cohort_project = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Project))";
SET survey = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Survey))";
SET registry = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Registry))";
SET research = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Cohort))";
SET program = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Program))";
SET consortium = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Consortium))";  
SET network = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Network))";


SET biobank_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]io[bB]ank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET study_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Study)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET bank_of =  r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:(?:Tissue|Blood|Brain|Specimen|Milk)\sBank)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET biorepo_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]iorepository(?:\sNetwork)?)(?:(?:(?:\s(?:of|of the)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3})(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1})?)?)";
SET programme_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Programme)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET cohort_project_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Project)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET survey_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Survey)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET registry_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Registry)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET research_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Cohort)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET program_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Program)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET consortium_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Consortium)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";  
SET network_of = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Network)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z'’]+(?:\s|:|\.|$))){1,3}))?)";

CREATE OR REPLACE TABLE  `ccnr-success.cohorts.expanded_papers_mentions` AS (

WITH
expanded_papers AS (
  SELECT
      CASE
      WHEN REGEXP_CONTAINS(acknowledgements, study) THEN REGEXP_EXTRACT_ALL(acknowledgements, study)
      WHEN REGEXP_CONTAINS(title, study) THEN REGEXP_EXTRACT_ALL(title, study)
      WHEN REGEXP_CONTAINS(abstract, study) THEN REGEXP_EXTRACT_ALL(abstract, study)
      WHEN REGEXP_CONTAINS(title, biobank) THEN REGEXP_EXTRACT_ALL(title, biobank)
      WHEN REGEXP_CONTAINS(abstract, biobank) THEN REGEXP_EXTRACT_ALL(abstract, biobank)
      WHEN REGEXP_CONTAINS(acknowledgements, biobank) THEN REGEXP_EXTRACT_ALL(acknowledgements, biobank)
      WHEN REGEXP_CONTAINS(title, bank) THEN REGEXP_EXTRACT_ALL(title, bank)
      WHEN REGEXP_CONTAINS(abstract, bank) THEN REGEXP_EXTRACT_ALL(abstract, bank)
      WHEN REGEXP_CONTAINS(acknowledgements, bank) THEN REGEXP_EXTRACT_ALL(acknowledgements, bank)
      WHEN REGEXP_CONTAINS(title, biorepo) THEN REGEXP_EXTRACT_ALL(title, biorepo)
      WHEN REGEXP_CONTAINS(abstract, biorepo) THEN REGEXP_EXTRACT_ALL(abstract, biorepo)
      WHEN REGEXP_CONTAINS(acknowledgements, biorepo) THEN REGEXP_EXTRACT_ALL(acknowledgements, biorepo)
      WHEN REGEXP_CONTAINS(title, programme) THEN REGEXP_EXTRACT_ALL(title, programme)
      WHEN REGEXP_CONTAINS(abstract, programme) THEN REGEXP_EXTRACT_ALL(abstract, programme)
      WHEN REGEXP_CONTAINS(acknowledgements, programme) THEN REGEXP_EXTRACT_ALL(acknowledgements, programme)
      WHEN REGEXP_CONTAINS(title, cohort_project) THEN REGEXP_EXTRACT_ALL(title, cohort_project)
      WHEN REGEXP_CONTAINS(abstract, cohort_project) THEN REGEXP_EXTRACT_ALL(abstract, cohort_project)
      WHEN REGEXP_CONTAINS(acknowledgements, cohort_project) THEN REGEXP_EXTRACT_ALL(acknowledgements, cohort_project)
      WHEN REGEXP_CONTAINS(title, survey) THEN REGEXP_EXTRACT_ALL(title, survey)
      WHEN REGEXP_CONTAINS(abstract, survey) THEN REGEXP_EXTRACT_ALL(abstract, survey)
      WHEN REGEXP_CONTAINS(acknowledgements, survey) THEN REGEXP_EXTRACT_ALL(acknowledgements, survey)
      WHEN REGEXP_CONTAINS(title, registry) THEN REGEXP_EXTRACT_ALL(title, registry)
      WHEN REGEXP_CONTAINS(abstract, registry) THEN REGEXP_EXTRACT_ALL(abstract, registry)
      WHEN REGEXP_CONTAINS(acknowledgements, registry) THEN REGEXP_EXTRACT_ALL(acknowledgements, registry)
      WHEN REGEXP_CONTAINS(title, research) THEN REGEXP_EXTRACT_ALL(title, research)
      WHEN REGEXP_CONTAINS(abstract, research) THEN REGEXP_EXTRACT_ALL(abstract, research)
      WHEN REGEXP_CONTAINS(acknowledgements, research) THEN REGEXP_EXTRACT_ALL(acknowledgements, research)
      WHEN REGEXP_CONTAINS(title, program) THEN REGEXP_EXTRACT_ALL(title, program)
      WHEN REGEXP_CONTAINS(abstract, program) THEN REGEXP_EXTRACT_ALL(abstract, program)
      WHEN REGEXP_CONTAINS(acknowledgements, program) THEN REGEXP_EXTRACT_ALL(acknowledgements, program)
      WHEN REGEXP_CONTAINS(title, consortium) THEN REGEXP_EXTRACT_ALL(title, consortium)
      WHEN REGEXP_CONTAINS(abstract, consortium) THEN REGEXP_EXTRACT_ALL(abstract, consortium)
      WHEN REGEXP_CONTAINS(acknowledgements, consortium) THEN REGEXP_EXTRACT_ALL(acknowledgements, consortium)
      WHEN REGEXP_CONTAINS(title, network) THEN REGEXP_EXTRACT_ALL(title, network)
      WHEN REGEXP_CONTAINS(abstract, network) THEN REGEXP_EXTRACT_ALL(abstract, network)
      WHEN REGEXP_CONTAINS(acknowledgements, network) THEN REGEXP_EXTRACT_ALL(acknowledgements, network)
      END
      AS cohort_name,
  id

  FROM `ccnr-success.cohorts.papers_citations` pc

  WHERE
  (
    REGEXP_CONTAINS(acknowledgements, study)
    OR REGEXP_CONTAINS(title, study)
    OR REGEXP_CONTAINS(abstract, study)
    OR REGEXP_CONTAINS(acknowledgements, biobank)
    OR REGEXP_CONTAINS(title, biobank)
    OR REGEXP_CONTAINS(abstract, biobank)
    OR REGEXP_CONTAINS(acknowledgements, bank)
    OR REGEXP_CONTAINS(title, bank)
    OR REGEXP_CONTAINS(abstract, bank)
    OR REGEXP_CONTAINS(acknowledgements, biorepo)
    OR REGEXP_CONTAINS(title, biorepo)
    OR REGEXP_CONTAINS(abstract, biorepo)
    OR REGEXP_CONTAINS(acknowledgements, programme)
    OR REGEXP_CONTAINS(title, programme)
    OR REGEXP_CONTAINS(abstract, programme)
    OR REGEXP_CONTAINS(acknowledgements, registry)
    OR REGEXP_CONTAINS(title, registry)
    OR REGEXP_CONTAINS(abstract, registry)
    OR REGEXP_CONTAINS(acknowledgements, cohort_project)
    OR REGEXP_CONTAINS(title, cohort_project)
    OR REGEXP_CONTAINS(abstract, cohort_project)
    OR REGEXP_CONTAINS(acknowledgements, survey)
    OR REGEXP_CONTAINS(title, survey)
    OR REGEXP_CONTAINS(abstract, survey)
    OR REGEXP_CONTAINS(acknowledgements, program)
    OR REGEXP_CONTAINS(title, program)
    OR REGEXP_CONTAINS(abstract, program)
    OR REGEXP_CONTAINS(acknowledgements, consortium)
    OR REGEXP_CONTAINS(title, consortium)
    OR REGEXP_CONTAINS(abstract, consortium)
    OR REGEXP_CONTAINS(acknowledgements, network)
    OR REGEXP_CONTAINS(title, network)
    OR REGEXP_CONTAINS(abstract, network)
  )
  AND
  (
    NOT REGEXP_CONTAINS(acknowledgements, study_of)
    AND NOT REGEXP_CONTAINS(title, study_of)
    AND NOT REGEXP_CONTAINS(abstract, study_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, biobank_of)
    AND NOT REGEXP_CONTAINS(title, biobank_of)
    AND NOT REGEXP_CONTAINS(abstract, biobank_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, bank_of)
    AND NOT REGEXP_CONTAINS(title, bank_of)
    AND NOT REGEXP_CONTAINS(abstract, bank_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, biorepo_of)
    AND NOT REGEXP_CONTAINS(title, biorepo_of)
    AND NOT REGEXP_CONTAINS(abstract, biorepo_of)
    AND NOT REGEXP_CONTAINS(acknowledgements,programme_of)
    AND NOT REGEXP_CONTAINS(title,programme_of)
    AND NOT REGEXP_CONTAINS(abstract,programme_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, registry_of)
    AND NOT REGEXP_CONTAINS(title, registry_of)
    AND NOT REGEXP_CONTAINS(abstract, registry_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, cohort_project_of)
    AND NOT REGEXP_CONTAINS(title, cohort_project_of)
    AND NOT REGEXP_CONTAINS(abstract, cohort_project_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, survey_of)
    AND NOT REGEXP_CONTAINS(title, survey_of)
    AND NOT REGEXP_CONTAINS(abstract, survey_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, program_of)
    AND NOT REGEXP_CONTAINS(title, program_of)
    AND NOT REGEXP_CONTAINS(abstract, program_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, consortium_of)
    AND NOT REGEXP_CONTAINS(title, consortium_of)
    AND NOT REGEXP_CONTAINS(abstract, consortium_of)
    AND NOT REGEXP_CONTAINS(acknowledgements, network_of)
    AND NOT REGEXP_CONTAINS(title, network_of)
    AND NOT REGEXP_CONTAINS(abstract, network_of)
  )
  -- end of where
), -- end of expanded_papers

expanded_papers_of AS (
  SELECT
    CASE
      WHEN REGEXP_CONTAINS(acknowledgements, study_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, study_of)
      WHEN REGEXP_CONTAINS(title, study_of) THEN REGEXP_EXTRACT_ALL(title, study_of)
      WHEN REGEXP_CONTAINS(abstract, study_of) THEN REGEXP_EXTRACT_ALL(abstract, study_of)
      WHEN REGEXP_CONTAINS(title, biobank_of) THEN REGEXP_EXTRACT_ALL(title, biobank_of)
      WHEN REGEXP_CONTAINS(abstract, biobank_of) THEN REGEXP_EXTRACT_ALL(abstract, biobank_of)
      WHEN REGEXP_CONTAINS(acknowledgements, biobank_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, biobank_of)
      WHEN REGEXP_CONTAINS(title, bank_of) THEN REGEXP_EXTRACT_ALL(title, bank_of)
      WHEN REGEXP_CONTAINS(abstract, bank_of) THEN REGEXP_EXTRACT_ALL(abstract, bank_of)
      WHEN REGEXP_CONTAINS(acknowledgements, bank_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, bank_of)
      WHEN REGEXP_CONTAINS(title, biorepo_of) THEN REGEXP_EXTRACT_ALL(title, biorepo_of)
      WHEN REGEXP_CONTAINS(abstract, biorepo_of) THEN REGEXP_EXTRACT_ALL(abstract, biorepo_of)
      WHEN REGEXP_CONTAINS(acknowledgements, biorepo_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, biorepo_of)
      WHEN REGEXP_CONTAINS(title, programme_of) THEN REGEXP_EXTRACT_ALL(title, programme_of)
      WHEN REGEXP_CONTAINS(abstract, programme_of) THEN REGEXP_EXTRACT_ALL(abstract, programme_of)
      WHEN REGEXP_CONTAINS(acknowledgements, programme_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, programme_of)
      WHEN REGEXP_CONTAINS(title, cohort_project_of) THEN REGEXP_EXTRACT_ALL(title, cohort_project_of)
      WHEN REGEXP_CONTAINS(abstract, cohort_project_of) THEN REGEXP_EXTRACT_ALL(abstract, cohort_project_of)
      WHEN REGEXP_CONTAINS(acknowledgements, cohort_project_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, cohort_project_of)
      WHEN REGEXP_CONTAINS(title, survey_of) THEN REGEXP_EXTRACT_ALL(title, survey_of)
      WHEN REGEXP_CONTAINS(abstract, survey_of) THEN REGEXP_EXTRACT_ALL(abstract, survey_of)
      WHEN REGEXP_CONTAINS(acknowledgements, survey_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, survey_of)
      WHEN REGEXP_CONTAINS(title, registry_of) THEN REGEXP_EXTRACT_ALL(title, registry_of)
      WHEN REGEXP_CONTAINS(abstract, registry_of) THEN REGEXP_EXTRACT_ALL(abstract, registry_of)
      WHEN REGEXP_CONTAINS(acknowledgements, registry_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, registry_of)
      WHEN REGEXP_CONTAINS(title, research_of) THEN REGEXP_EXTRACT_ALL(title, research_of)
      WHEN REGEXP_CONTAINS(abstract, research_of) THEN REGEXP_EXTRACT_ALL(abstract, research_of)
      WHEN REGEXP_CONTAINS(acknowledgements, research_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, research_of)
      WHEN REGEXP_CONTAINS(title, program_of) THEN REGEXP_EXTRACT_ALL(title, program_of)
      WHEN REGEXP_CONTAINS(abstract, program_of) THEN REGEXP_EXTRACT_ALL(abstract, program_of)
      WHEN REGEXP_CONTAINS(acknowledgements, program_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, program_of)
      WHEN REGEXP_CONTAINS(title, consortium_of) THEN REGEXP_EXTRACT_ALL(title, consortium_of)
      WHEN REGEXP_CONTAINS(abstract, consortium_of) THEN REGEXP_EXTRACT_ALL(abstract, consortium_of)
      WHEN REGEXP_CONTAINS(acknowledgements, consortium_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, consortium_of)
      WHEN REGEXP_CONTAINS(title, network_of) THEN REGEXP_EXTRACT_ALL(title, network_of)
      WHEN REGEXP_CONTAINS(abstract, network_of) THEN REGEXP_EXTRACT_ALL(abstract, network_of)
      WHEN REGEXP_CONTAINS(acknowledgements, network_of) THEN REGEXP_EXTRACT_ALL(acknowledgements, network_of)
      END
      AS cohort_name,
  id

  FROM `ccnr-success.cohorts.papers_citations` pc

  WHERE
  (
    REGEXP_CONTAINS(acknowledgements, study_of)
    OR REGEXP_CONTAINS(title, study_of)
    OR REGEXP_CONTAINS(abstract, study_of)
    OR REGEXP_CONTAINS(acknowledgements, biobank_of)
    OR REGEXP_CONTAINS(title, biobank_of)
    OR REGEXP_CONTAINS(abstract, biobank_of)
    OR REGEXP_CONTAINS(acknowledgements, bank_of)
    OR REGEXP_CONTAINS(title, bank_of)
    OR REGEXP_CONTAINS(abstract, bank_of)
    OR REGEXP_CONTAINS(acknowledgements, biorepo_of)
    OR REGEXP_CONTAINS(title, biorepo_of)
    OR REGEXP_CONTAINS(abstract, biorepo_of)
    OR REGEXP_CONTAINS(acknowledgements,programme_of)
    OR REGEXP_CONTAINS(title,programme_of)
    OR REGEXP_CONTAINS(abstract,programme_of)
    OR REGEXP_CONTAINS(acknowledgements, registry_of)
    OR REGEXP_CONTAINS(title, registry_of)
    OR REGEXP_CONTAINS(abstract, registry_of)
    OR REGEXP_CONTAINS(acknowledgements, cohort_project_of)
    OR REGEXP_CONTAINS(title, cohort_project_of)
    OR REGEXP_CONTAINS(abstract, cohort_project_of)
    OR REGEXP_CONTAINS(acknowledgements, survey_of)
    OR REGEXP_CONTAINS(title, survey_of)
    OR REGEXP_CONTAINS(abstract, survey_of)
    OR REGEXP_CONTAINS(acknowledgements, program_of)
    OR REGEXP_CONTAINS(title, program_of)
    OR REGEXP_CONTAINS(abstract, program_of)
    OR REGEXP_CONTAINS(acknowledgements, consortium_of)
    OR REGEXP_CONTAINS(title, consortium_of)
    OR REGEXP_CONTAINS(abstract, consortium_of)
    OR REGEXP_CONTAINS(acknowledgements, network_of)
    OR REGEXP_CONTAINS(title, network_of)
    OR REGEXP_CONTAINS(abstract, network_of)
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
ON ec.cohort_name = ep.cohort_name
) -- end of create or replace table