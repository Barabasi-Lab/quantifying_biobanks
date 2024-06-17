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
DECLARE health STRING;
DECLARE initiative STRING;
DECLARE biocenter STRING;
DECLARE bioresource STRING;
DECLARE repo STRING;
DECLARE consortium STRING;

SET biobank = r"\bBio[bB]ank\b";
SET study = r"\bStudy\b";
SET bank =  r"\bTissue|Blood|Brain|Specimen|Milk\b\sBank)";
SET biorepo = r"\bBiorepository\b";
SET programme = r"\bProgramme\b";
SET cohort_project = r"\bProject\b";
SET survey = r"\bSurvey\b";
SET registry = r"\bRegistry\b";
SET research = r"\bCohort\b";
SET program = r"\bProgram\b";
SET health = r"\bHealth\b";
SET initiative = r"\bInitiative\b";
SET biocenter = r"\bBiocenter\b";
SET bioresource = r"\bBioresource\b";
SET repo = r"\bRepository\b";
SET consortium = r"\bConsortium\b";

SET biobank = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]io[bB]ank)\b";
SET study = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Study)\b";
SET bank =  r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:(?:Tissue|Blood|Brain|Specimen|Milk)\sBank)\b";
SET biorepo = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:[bB]iorepository)\b";
SET programme = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Programme)\b";
SET program = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Program)\b";
SET cohort_project = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Project)\b";
SET survey = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Survey)\b";
SET registry = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Registry)\b";
SET research = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Cohort)\b";  
SET health = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Health)\b";
SET initiative = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Initiative)\b";
SET biocenter = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Biocenter)\b";
SET bioresource = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Bioresource)\b";
SET repo = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Repository)\b";
SET consortium = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Consortium)\b"; 



CREATE TABLE  `ccnr-success.cohorts.potential_papers` AS (

WITH
expanded_papers AS (
  SELECT

  id,
  year,
  title.preferred title,
  abstract.preferred abstract,
  acknowledgements.preferred acknowledgements

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
    OR REGEXP_CONTAINS(title.preferred,bioresource)
    OR REGEXP_CONTAINS(title.preferred,repo)
    OR REGEXP_CONTAINS(title.preferred,consortium)
    OR REGEXP_CONTAINS(title.preferred,biocenter)
    OR REGEXP_CONTAINS(abstract.preferred,biocenter)
    OR REGEXP_CONTAINS(abstract.preferred,bioresource)
    OR REGEXP_CONTAINS(abstract.preferred,repo)
    OR REGEXP_CONTAINS(abstract.preferred,consortium)
    OR REGEXP_CONTAINS(acknowledgements.preferred,consortium)
    OR REGEXP_CONTAINS(acknowledgements.preferred,biocenter)
    OR REGEXP_CONTAINS(acknowledgements.preferred,bioresource)
    OR REGEXP_CONTAINS(acknowledgements.preferred,repo)
    OR REGEXP_CONTAINS(title.preferred,health)
    OR REGEXP_CONTAINS(title.preferred,initiative)
    OR REGEXP_CONTAINS(abstract.preferred,initiative)
    OR REGEXP_CONTAINS(abstract.preferred,health)
    OR REGEXP_CONTAINS(acknowledgements.preferred,initiative)
    OR REGEXP_CONTAINS(acknowledgements.preferred,health)
  )
WHERE year BETWEEN 1940 AND 2023
AND p.type = 'article'

  -- end of where
), -- end of expanded_papers



CREATE OR REPLACE TABLE  `ccnr-success.cohorts.potential_papers` AS (
  SELECT
  m.id,
  year,
  title,
  abstract,
  acknowledgements
  FROM expanded_papers
)