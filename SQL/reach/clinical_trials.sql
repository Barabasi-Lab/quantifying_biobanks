WITH paper2clinical AS (
SELECT
cli id,
p.id paper_id,
'paper2clinical' AS direction



FROM
`ccnr-success.cohorts_expanded.papers` p,
UNNEST(p.clinical_trial_ids) as cli
LEFT JOIN `dimensions-ai.data_analytics.clinical_trials` AS c
ON cli = c.id
WHERE cli IS NOT NULL)
,

clinical2paper AS (
SELECT
c.id,
p.id paper_id,
'clinical2paper' AS direction

FROM `dimensions-ai.data_analytics.clinical_trials` AS c,
UNNEST(c.publication_ids) pub
LEFT JOIN `ccnr-success.cohorts_expanded.papers` p
ON pub = p.id
WHERE p.id IS NOT NULL)
,
both AS (
SELECT * FROM clinical2paper
UNION ALL
SELECT * FROM paper2clinical)
,
uboth AS (
SELECT 
DISTINCT id
FROM both
)

SELECT


b.id,
title,
registry,
study_type,
phase,
overall_status,
conditions,
start_year,
end_year,
study_maximum_age,
study_minimum_age,
gender,
ARRAY(SELECT STRUCT(type, name) FROM UNNEST(interventions) WHERE type IS NOT NULL) interventions,
ARRAY(SELECT STRUCT(type, label) FROM UNNEST(study_arms) WHERE type IS NOT NULL) study_arms,
study_participants,
ARRAY(SELECT STRUCT(researcher_id, role) FROM UNNEST(investigators) WHERE researcher_id IS NOT NULL) investigators,
c.category_bra.values AS bra,
c.category_rcdc.values AS rcdc,
c.category_hrcs_hc.values AS hrcs_hc,
mesh_terms,
ARRAY(SELECT STRUCT(grid_id, type) FROM UNNEST(organisation_details) WHERE grid_id IS NOT NULL) organisation_details,
publication_ids


FROM uboth as b
LEFT JOIN `dimensions-ai.data_analytics.clinical_trials` as c
ON b.id = c.id