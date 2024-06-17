SELECT
p.id,
g.cohort_name_lower

FROM `ccnr-success.biobanks.google_patents_uncased_ex` g
LEFT JOIN `dimensions-ai.data_analytics.patents` p
ON g.application_number = p.application_reference_id
GROUP BY 1,2