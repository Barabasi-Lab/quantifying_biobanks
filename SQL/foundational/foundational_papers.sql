CREATE OR REPLACE TABLE `ccnr-success.cohorts_expanded.foundational` AS (

WITH pub_cit_inner AS (

SELECT
p.id,
p.citations_count,
cp.cohort_name_lower,
p.title,
p.year,
pc.id cit_id,
pc.title cit_title,
pc.year AS cit_year



FROM
`ccnr-success.cohorts_expanded.papers` p,
UNNEST(citations) as cit
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cp
ON p.id = cp.id
LEFT JOIN
`ccnr-success.cohorts_expanded.cohorts` c 
ON cp.cohort_name_lower = c.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cpc
ON cit.id = cpc.id AND cp.cohort_name_lower = cpc.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.papers` pc
ON pc.id = cit.id
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_mentions` m
ON p.id = m.id AND cp.cohort_name_lower = m.cohort_name_lower

WHERE c.pubs >= 20
AND
cpc.cohort_name_lower IS NOT NULL
AND
(m.source = 'abstract' OR m.source = 'title'))
,
pub_cit_inner_other_cohort AS (

SELECT
p.id,
p.citations_count,
cp.cohort_name_lower,
p.title,
p.year,
pc.id cit_id,
pc.title cit_title,
pc.year AS cit_year



FROM
`ccnr-success.cohorts_expanded.papers` p,
UNNEST(citations) as cit
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cp
ON p.id = cp.id
LEFT JOIN
`ccnr-success.cohorts_expanded.cohorts` c 
ON cp.cohort_name_lower = c.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cpc
ON cit.id = cpc.id AND cp.cohort_name_lower = cpc.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.papers` pc
ON pc.id = cit.id
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_mentions` m
ON p.id = m.id AND cp.cohort_name_lower != m.cohort_name_lower

WHERE c.pubs >= 20
AND
cpc.cohort_name_lower IS NOT NULL
AND
(m.source = 'abstract' OR m.source = 'title'))
,


mention_time AS (
    SELECT
    cp.cohort_name_lower,
    MIN(year) AS first_mention_year,
    AVG(year) AS mean_mention_year,
    MAX(year) AS last_mention_year
    FROM
    `ccnr-success.cohorts_expanded.papers` p
    LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cp
    ON p.id = cp.id
    GROUP BY 1
)
,
mention_refs AS (

SELECT
p.id,
p.title,
cp.cohort_name_lower,
p.year,
ref,
pr.year AS ref_year,
CASE 
  WHEN pr.id IS NOT NULL THEN 1
  ELSE 0
  END AS is_ref_mention

FROM `ccnr-success.cohorts_expanded.papers` p,
UNNEST(p.reference_ids) ref
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cp
ON p.id = cp.id
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cpr
ON ref = p.id AND cp.cohort_name_lower = cpr.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.papers` pr
ON ref = pr.id


ORDER BY is_ref_mention DESC)
,
ref_data AS (

SELECT
id,
cohort_name_lower,
title,
SUM(is_ref_mention) num_ref_mentions,
ROUND(SUM(is_ref_mention) / COUNT(DISTINCT ref), 2) AS prop_ref_mentions,
MIN(ref_year) AS first_ref_year,
CAST(FLOOR(AVG(ref_year)) AS INT64) AS mean_ref_year,
MAX(ref_year) AS last_ref_year

FROM
mention_refs
GROUP BY 1,2,3
ORDER BY num_ref_mentions DESC)
,
cit_data AS (

SELECT
pci.id,
pci.title,
pci.cohort_name_lower,
pci.year,
mt.first_mention_year,
CAST(FLOOR(mt.mean_mention_year) AS INT64) mean_mention_year,
mt.last_mention_year,
COUNT(DISTINCT cit_id) AS inner_citations,
ROUND(COUNT(DISTINCT cit_id) / c.pubs, 2) AS inner_citation_prop,
MIN(cit_year) AS first_cit_year,
CAST(FLOOR(AVG(cit_year)) AS INT64) AS mean_cite_year,
MAX(cit_year) AS last_cite_year


FROM pub_cit_inner pci
LEFT JOIN mention_time mt
ON pci.cohort_name_lower = mt.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.cohorts` c
ON pci.cohort_name_lower = c.cohort_name_lower


GROUP BY 1,2,3,4,5,6,7,c.pubs

ORDER BY inner_citations DESC)
,

ref_and_cit_data AS (
SELECT
cd.id,
cd.title,
cd.cohort_name_lower,
cd.inner_citations,
cd.inner_citation_prop prop_inner_citations,
rd.num_ref_mentions inner_references,
rd.prop_ref_mentions prop_inner_references,
cd.year,
cd.mean_cite_year mean_citation_year,
rd.mean_ref_year mean_reference_year,
cd.year - cd.first_mention_year years_after_first_mention,
cd.year - cd.mean_mention_year years_diff_mean_mention,


FROM cit_data cd
LEFT JOIN ref_data rd
ON cd.id = rd.id AND cd.cohort_name_lower = rd.cohort_name_lower

ORDER BY inner_citations DESC)
,

citing_mentions AS (

SELECT
p.id,
cp.cohort_name_lower,
COUNT(DISTINCT pm.id) post_mentions_citing

FROM `ccnr-success.cohorts_expanded.papers` p
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cp
ON p.id = cp.id
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` m
ON m.cohort_name_lower = cp.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.papers` pm
ON pm.id = m.id,
UNNEST(pm.reference_ids) ref_m

WHERE pm.year > p.year
AND
ref_m = p.id

GROUP BY 1,2)
,
post_mentions AS (
SELECT
p.id,
cp.cohort_name_lower,
COUNT(DISTINCT pm.id) post_mentions

FROM `ccnr-success.cohorts_expanded.papers` p
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` cp
ON p.id = cp.id
LEFT JOIN `ccnr-success.cohorts_expanded.cohort_papers` m
ON m.cohort_name_lower = cp.cohort_name_lower
LEFT JOIN `ccnr-success.cohorts_expanded.papers` pm
ON pm.id = m.id,
UNNEST(pm.reference_ids) ref_m

GROUP BY 1,2)
,

hidden_citations AS (
SELECT
pm.*,
cm.post_mentions_citing,
pm.post_mentions - cm.post_mentions_citing AS hidden_citations,
ROUND((pm.post_mentions - cm.post_mentions_citing) / pm.post_mentions, 2) prop_hidden_citations

FROM post_mentions pm
LEFT JOIN citing_mentions cm
ON cm.id = pm.id AND pm.cohort_name_lower = cm.cohort_name_lower
)

SELECT
rc.*,
hc.hidden_citations,
hc.prop_hidden_citations,
hc.post_mentions,
hc.post_mentions_citing

FROM ref_and_cit_data rc
LEFT JOIN hidden_citations hc
ON rc.id = hc.id AND rc.cohort_name_lower = hc.cohort_name_lower

ORDER BY post_mentions_citing DESC)