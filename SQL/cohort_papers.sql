CREATE TABLE `ccnr-success.biobanks.cohort_pubs` AS (

SELECT
  p.id,
  p.title.preferred AS title,
  p.abstract.preferred AS abstract,
  p.acknowledgements.preferred AS acknowledgements,


FROM
`dimensions-ai.data_analytics.publications` p

WHERE 


-- MESH HEADINGS
('D015331' IN UNNEST(p.pubmed.mesh.ui)
OR 'D011446' IN UNNEST(p.pubmed.mesh.ui)
OR 'D005500' IN UNNEST(p.pubmed.mesh.ui)
OR 'D003430' IN UNNEST(p.pubmed.mesh.ui)
OR 'D008137' IN UNNEST(p.pubmed.mesh.ui)
OR 'D012189' IN UNNEST(p.pubmed.mesh.ui)
)

OR
-- Biobanks
('D018070' IN UNNEST(p.pubmed.mesh.ui)
OR 'D001771' IN UNNEST(p.pubmed.mesh.ui)
OR 'D017784' IN UNNEST(p.pubmed.mesh.ui)
OR 'D013074' IN UNNEST(p.pubmed.mesh.ui)
OR 'D014015' IN UNNEST(p.pubmed.mesh.ui)
OR 'D018586' IN UNNEST(p.pubmed.mesh.ui)
OR 'D005125' IN UNNEST(p.pubmed.mesh.ui)
)

OR

-- GWAS
('D056726' IN UNNEST(p.pubmed.mesh.ui)
OR 'D055106' IN UNNEST(p.pubmed.mesh.ui)
)

AND
-- HUMAN

(
  'D006801' IN UNNEST(p.pubmed.mesh.ui)

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
p.year <= 2020)