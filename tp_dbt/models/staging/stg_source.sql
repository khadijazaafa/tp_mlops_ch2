SELECT
    id,
    UPPER(TRIM(nom))       AS nom,
    age,
    COALESCE(montant, 0.0) AS montant
FROM {{ source('raw', 'csv_data') }}
WHERE id IS NOT NULL