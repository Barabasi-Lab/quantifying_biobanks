CREATE TABLE `ccnr-success.cohorts.papers_citations` AS (

SELECT

p.id,
p.title.preferred title,
p.abstract.preferred abstract,
p.acknowledgements.preferred acknowledgements

FROM `ccnr-success.cohorts.papers` pc,
UNNEST(citations) cit
LEFT JOIN `dimensions-ai.data_analytics.publications` p
ON cit.id = p.id

GROUP BY 1,2,3,4

)