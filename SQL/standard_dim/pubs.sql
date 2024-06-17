CREATE TABLE `ccnr-success.biobanks.pubs` AS (
SELECT
id,
REGEXP_REPLACE(REGEXP_REPLACE(title.preferred, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+|', r''), r'\s{2,}', r' ') AS title,
REGEXP_REPLACE(REGEXP_REPLACE(abstract.preferred, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS abstract,
REGEXP_REPLACE(REGEXP_REPLACE(acknowledgements.preferred, r'\(.*?\)|[.,]|[ \t]+$|^[ \t]+', r''), r'\s{2,}', r' ') AS acknowledgements

FROM `dimensions-ai.data_analytics.publications`
WHERE
title IS NOT NULL)