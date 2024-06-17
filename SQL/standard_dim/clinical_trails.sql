    
    CREATE TABLE `ccnr-success.biobanks.clinical_trials` AS (
    SELECT
    id,
    REGEXP_REPLACE(REGEXP_REPLACE(title, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS title,
    REGEXP_REPLACE(REGEXP_REPLACE(abstract, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS abstract,
    REGEXP_REPLACE(REGEXP_REPLACE(brief_title, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS brief_title

    FROM `dimensions-ai.data_analytics.clinical_trials`
    WHERE
    abstract IS NOT NULL)