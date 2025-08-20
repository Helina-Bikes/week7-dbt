WITH recursive
    date_series AS (
        SELECT DATE('2024-01-01') AS date
        UNION ALL
        SELECT DATE_ADD(date, INTERVAL 1 DAY)
        FROM date_series
        WHERE
            date < '2025-12-31'
    )
SELECT date
FROM date_series