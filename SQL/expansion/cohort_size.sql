SELECT

bp.id,
REGEXP_EXTRACT_ALL(LOWER(p.abstract.preferred), r'(?:[\d,]+)\d\d\d (?:men|women|adults|individuals|participants|patients|children|female|male|mothers|fathers|people|subjects)') size

FROM `ccnr-success.cohorts_expanded.cohort_papers` bp
LEFT JOIN `dimensions-ai.data_analytics.publications` p
ON bp.id = p.id

WHERE
REGEXP_CONTAINS(LOWER(p.abstract.preferred), r'(?:[\d,]+)\d\d\d (?:men|women|adults|individuals|participants|patients|children|female|male|mothers|fathers|people|subjects)')