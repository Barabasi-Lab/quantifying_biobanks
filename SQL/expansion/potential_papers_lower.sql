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

CREATE TABLE  `ccnr-success.cohorts.potential_papers_lower` AS (

WITH
expanded_papers AS (
  SELECT

  id,
  title.preferred,
  abstract.preferred,
  acknowledgements.preferred

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
  )
  -- end of where
), -- end of expanded_papers

expanded_papers_of AS (
  SELECT

  id,
  title.preferred,
  abstract.preferred,
  acknowledgements.preferred

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
    OR REGEXP_CONTAINS(acknowledgements.preferred, program_of)
    OR REGEXP_CONTAINS(title.preferred, program_of)
    OR REGEXP_CONTAINS(abstract.preferred, program_of)
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
  id
  FROM expanded_papers_all
  GROUP BY 1
)
-- end of aliases

SELECT

ep.id

FROM
papers ep

) -- end of create or replace table