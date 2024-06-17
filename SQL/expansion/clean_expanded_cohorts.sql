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
SET health = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Health)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET initiative = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Initiative)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET biocenter = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Biocenter)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET bioresource = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Bioresource)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET repo = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){1,7}(?:Repository)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";
SET consortium = r"\b[tT]he\s((?:[A-Z](?:[A-Za-z'’-])+\s?){2,7}(?:Consortium)(?:(?:(?:\s(?:of)\s)(?:(?:[A-Z][a-z]+(?:\s|:|\.|$))){1,3}))?)";  



WITH cohort_title_acknowledgements AS (
    SELECT 
    CASE
        WHEN REGEXP_CONTAINS(title, biobank) THEN REGEXP_EXTRACT(title, biobank)
        WHEN REGEXP_CONTAINS(title, bank) THEN REGEXP_EXTRACT(title, bank)
        WHEN REGEXP_CONTAINS(title, biorepo) THEN REGEXP_EXTRACT(title, biorepo)
        WHEN REGEXP_CONTAINS(title, registry) THEN REGEXP_EXTRACT(title, registry)
        WHEN REGEXP_CONTAINS(title, bioresource) THEN REGEXP_EXTRACT(title, bioresource)
        WHEN REGEXP_CONTAINS(title, repo) THEN REGEXP_EXTRACT(title, repo)
        WHEN REGEXP_CONTAINS(title, consortium) THEN REGEXP_EXTRACT(title, consortium)
        WHEN REGEXP_CONTAINS(title, biocenter) THEN REGEXP_EXTRACT(title, biocenter)
        WHEN REGEXP_CONTAINS(acknowledgements, biobank) THEN REGEXP_EXTRACT(acknowledgements, biobank)
        WHEN REGEXP_CONTAINS(acknowledgements, bank) THEN REGEXP_EXTRACT(acknowledgements, bank)
        WHEN REGEXP_CONTAINS(acknowledgements, biorepo) THEN REGEXP_EXTRACT(acknowledgements, biorepo)
        WHEN REGEXP_CONTAINS(acknowledgements, registry) THEN REGEXP_EXTRACT(acknowledgements, registry)
        WHEN REGEXP_CONTAINS(acknowledgements, bioresource) THEN REGEXP_EXTRACT(acknowledgements, bioresource)
        WHEN REGEXP_CONTAINS(acknowledgements, repo) THEN REGEXP_EXTRACT(acknowledgements, repo)
        WHEN REGEXP_CONTAINS(acknowledgements, consortium) THEN REGEXP_EXTRACT(acknowledgements, consortium)
        WHEN REGEXP_CONTAINS(acknowledgements, biocenter) THEN REGEXP_EXTRACT(acknowledgements, biocenter)
        END AS cohort_name,
      cohort_name, 
      "biobank" AS kind,
      COUNT(id) AS cited_mention_citations
    FROM `ccnr-success.cohorts.papers_citations` pc
    WHERE 
      REGEXP_CONTAINS(title OR acknowledgements,
      biobank
      OR bank
      OR biorepo
      OR registry
      OR bioresource
      OR repo
      OR consortium
      OR biocenter
      )
    GROUP BY 
      cohort_name, kind 
  ),
cohort_title AS (
    SELECT 
    -- do the same case for the where clause here
    CASE
    WHEN REGEXP_CONTAINS(title, study) THEN REGEXP_EXTRACT(title, study)
    WHEN REGEXP_CONTAINS(title, programme) THEN REGEXP_EXTRACT(title, programme)
    WHEN REGEXP_CONTAINS(title, cohort_project) THEN REGEXP_EXTRACT(title, cohort_project)
    WHEN REGEXP_CONTAINS(title, survey) THEN REGEXP_EXTRACT(title, survey)
    WHEN REGEXP_CONTAINS(title, program) THEN REGEXP_EXTRACT(title, program)
    WHEN REGEXP_CONTAINS(title, research) THEN REGEXP_EXTRACT(title, research)
    WHEN REGEXP_CONTAINS(title, health) THEN REGEXP_EXTRACT(title, health)
    WHEN REGEXP_CONTAINS(title, initiative) THEN REGEXP_EXTRACT(title, initiative)
      "other" as kind,
      COUNT(id) AS cited_mention_citations
    FROM `ccnr-success.cohorts.papers_citations` pc
    WHERE 
      REGEXP_CONTAINS(title,
      programme
      OR program
      OR cohort_project
      OR survey
      OR research
      OR study
      OR initiative
      OR health
      )
    GROUP BY 
      cohort_name, kind 
  ),

cohort_data AS (
        SELECT * FROM cohort_title_acknowledgements
        UNION ALL
        SELECT * FROM cohort_title
    )

  SELECT 
    REGEXP_REPLACE(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(cohort_name, "’", "'"),
                    "And", "and"),
                        "Of", "of"),
                            r"\s$|\.$|:$", "")) AS cleaned_cohort_name,
    kind,
    SUM(cited_mention_citations) AS total_citations
  FROM cohort_data
  GROUP BY cleaned_cohort_name, kind
  ORDER BY total_citations DESC