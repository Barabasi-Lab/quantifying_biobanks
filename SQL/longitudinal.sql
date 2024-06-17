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
  p.metrics.relative_citation_ratio AS relative_citation_ratio,


FROM
`dimensions-ai.data_analytics.publications` p

WHERE
(REGEXP_CONTAINS(p.title.preferred, r'longitudinal')
       AND (REGEXP_CONTAINS(p.title.preferred, r':'))
       AND (REGEXP_CONTAINS(p.title.preferred, r'\bStudy\b'))
       AND (REGEXP_CONTAINS(p.title.preferred, r'\bdesign\b') OR REGEXP_CONTAINS(p.title.preferred, r'\brationale\b') OR REGEXP_CONTAINS(p.title.preferred, r'\bcharacteristics\b') OR REGEXP_CONTAINS(p.title.preferred, r'\bapproach\b') OR REGEXP_CONTAINS(p.title.preferred, r'\bobjectives\b'))
       )
  AND (p.type = 'article')