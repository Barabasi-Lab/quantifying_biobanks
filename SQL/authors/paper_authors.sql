SELECT
DISTINCT

author.researcher_id,
CONCAT(r.first_name, ' ', r.last_name) author_name,
r.current_research_org org_id,
g.name org_name,
g.address.country org_country,
g.address.country_code org_country_code

FROM `ccnr-success.cohorts_expanded.papers` b
LEFT JOIN `dimensions-ai.data_analytics.publications` p
ON b.id = p.id,
UNNEST(p.authors) author
LEFT JOIN `dimensions-ai.data_analytics.researchers` r
ON author.researcher_id = r.id
LEFT JOIN `dimensions-ai.data_analytics.grid` g
ON r.current_research_org = g.id
