EXPORT DATA
  OPTIONS (
    uri = 'gs://biobanks_dim/pubmed_papers/*.json.gzip',
    format = 'JSON',
    compression = 'GZIP') AS


SELECT
p.id,
p.title.preferred title,
p.abstract.preferred abstract,
p.acknowledgements.preferred acknowledgements
FROM
`dimensions-ai.data_analytics.publications` p

WHERE 
p.title.preferred IS NOT NULL
AND p.type = 'article'
AND p.pmid IS NOT NULL