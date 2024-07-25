SELECT
	broker_param.value as regulation,
	3 as category
FROM
	brokers
	INNER JOIN broker_param ON brokers.id = broker_param.broker_id
	INNER JOIN params ON params.id = broker_param.param_id
WHERE
	params.id = 536
    AND (brokers.name = '{broker_name}' or brokers.slug = '{broker_slug}')