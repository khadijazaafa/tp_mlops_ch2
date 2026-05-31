SELECT
    COUNT(*)      AS total_clients,
    AVG(age)      AS age_moyen,
    SUM(montant)  AS montant_total,
    AVG(montant)  AS montant_moyen,
    MAX(montant)  AS montant_max,
    MIN(montant)  AS montant_min
FROM {{ ref('stg_source') }}