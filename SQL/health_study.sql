SELECT
  p.id,
  p.year,
  p.title.preferred AS title,



FROM
`dimensions-ai.data_analytics.publications` p

WHERE
(REGEXP_CONTAINS(p.title.preferred, r'^The.+\b[hH]ealth [sS]tudy\b:.+\w.+')
       )
  AND (p.type = 'article')