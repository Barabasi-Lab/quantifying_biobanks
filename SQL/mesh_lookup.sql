SELECT
  p.id,
  p.year,
  p.title.preferred AS title,
  p.doi,
  p.abstract.preferred AS abstract,
  p.mesh_headings,
  p.patent_ids,
  p.citations,
  p.citations_count,
  p.journal.title,
  p.authors,
  p.metrics.relative_citation_ratio AS relative_citation_ratio

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

AND

(
  REGEXP_CONTAINS(LOWER(p.abstract.preferred), r'[ia]s an? (prospective|observational|longitudinal|restrospective)( \w+)? study.*')
  OR
  REGEXP_CONTAINS(LOWER(p.abstract.preferred), r'is an?\s?(\w+)? biobank\b')
)
)

ORDER BY p.citations_count DESC
