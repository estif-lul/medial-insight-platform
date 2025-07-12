SELECT *
FROM {{ ref('fct_messages') }}
WHERE text IS NULL OR TRIM(text) = ''