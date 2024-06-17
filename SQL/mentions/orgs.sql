SELECT
id,
acronyms,
name,
address.city city,
address.country country,
address.country_code country_code,
address.latitude lat,
address.longitude lon,
external_ids.wikidata.all wikidata_id,
organization_parent_ids parent_ids,
types
FROM
`dimensions-ai.data_analytics.grid`
WHERE
name IS NOT NULL