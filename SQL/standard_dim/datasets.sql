    
    CREATE TABLE `ccnr-success.biobanks.datasets` AS (
    SELECT
    id,
    REGEXP_REPLACE(REGEXP_REPLACE(title, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS title,
    REGEXP_REPLACE(REGEXP_REPLACE(description, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS description
    --REGEXP_REPLACE(REGEXP_REPLACE(brief_title, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS brief_title

    FROM `dimensions-ai.data_analytics.datasets`
    WHERE
    title IS NOT NULL)