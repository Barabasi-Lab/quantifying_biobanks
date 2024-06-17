EXPORT DATA
  OPTIONS (
    uri = 'gs://biobanks_dim/cohort_titles_abstracts/*.json.gzip',
    format = 'JSON',
    compression = 'GZIP') AS

SELECT
  p.id,
  p.title.preferred AS title,
  p.abstract.preferred AS abstract,


FROM
`dimensions-ai.data_analytics.publications` p

WHERE 


-- MESH HEADINGS
('Cohort Studies' IN UNNEST(p.mesh_headings)
OR 'Prospective Studies' IN UNNEST(p.mesh_headings)
OR 'Follow-Up Studies' IN UNNEST(p.mesh_headings)
OR 'Cross-Sectional Studies' IN UNNEST(p.mesh_headings)
OR 'Longitudinal Studies' IN UNNEST(p.mesh_headings)
OR 'Retrospective Studies' IN UNNEST(p.mesh_headings)
)

AND

(
  'Humans' IN UNNEST(p.mesh_headings)

)

AND

('Clinical Protocols' NOT IN UNNEST(p.mesh_headings) AND
'Clinical Trials as Topic' NOT IN UNNEST(p.mesh_headings) AND
'Pragmatic Clinical Trials as Topic' NOT IN UNNEST(p.mesh_headings) AND
'Clinical Decision Rules' NOT IN UNNEST(p.mesh_headings) AND
'Clinical Decision-Making' NOT IN UNNEST(p.mesh_headings) AND
'Clinical Trials, Phase II as Topic' NOT IN UNNEST(p.mesh_headings) AND
'Clinical Trials, Phase I as Topic' NOT IN UNNEST(p.mesh_headings) AND
'Randomized Controlled Trials as Topic' NOT IN UNNEST(p.mesh_headings)
)

-- TITLES
AND

(
  NOT REGEXP_CONTAINS(LOWER(p.title.preferred), r'.*\btrial\b.*')
  AND NOT REGEXP_CONTAINS(LOWER(p.title.preferred), r'.*\brandom.*')

)


-- ABSTRACTS

AND

(p.abstract.preferred IS NOT NULL
AND NOT REGEXP_CONTAINS(LOWER(p.abstract.preferred), r'.*\btrials?\b.*')
AND NOT REGEXP_CONTAINS(LOWER(p.abstract.preferred), r'.*\brandom.*')
)

-- YEAR
AND
p.year <= 2020