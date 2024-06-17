WITH paper2clinical AS (
SELECT
cli id,
p.id paper_id,
'p2c' AS dir


FROM
`ccnr-success.cohorts_expanded.papers` p,
UNNEST(p.clinical_trial_ids) as cli
LEFT JOIN `dimensions-ai.data_analytics.clinical_trials` AS c
ON cli = c.id
WHERE c.id IS NOT NULL)
,

clinical2paper AS (
SELECT
c.id,
p.id paper_id,
'c2p' AS dir

FROM `dimensions-ai.data_analytics.clinical_trials` AS c,
UNNEST(c.publication_ids) pub
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` p
ON pub = p.id
WHERE p.id IS NOT NULL)
,
both AS (
SELECT * FROM clinical2paper
UNION ALL
SELECT * FROM paper2clinical
GROUP BY id, paper_id, dir
)


SELECT 
both.id,
cp.cohort_name_lower,
dir
FROM both
JOIN `ccnr-success.cohorts_expanded.cohort_papers` cp
ON both.paper_id = cp.id