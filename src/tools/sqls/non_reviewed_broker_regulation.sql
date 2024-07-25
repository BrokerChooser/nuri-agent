SELECT
    regulation,
    category
FROM not_reviewed_providers
WHERE
    name = '{broker_name}'
    OR slug = '{broker_slug}'
