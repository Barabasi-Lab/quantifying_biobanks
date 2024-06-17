SELECT

m.mesh_id,
m.mesh_name,
COUNT(DISTINCT id) total_papers
FROM
`dimensions-ai.data_analytics.publications` p,
UNNEST(p.pubmed.mesh.ui) mesh_id
LEFT JOIN `ccnr-success.cohorts_expanded.mesh` m
ON m.mesh_id = mesh_id

WHERE m.tree_number LIKE 'C%'

GROUP BY
m.mesh_id, m.mesh_name

ORDER BY total_papers DESC