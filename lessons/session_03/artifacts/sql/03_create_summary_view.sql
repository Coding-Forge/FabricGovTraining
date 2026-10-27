CREATE VIEW silver.record_summary
AS
SELECT
    source_system,
    record_id,
    COUNT(*) AS source_row_count,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)
        AS invalid_amount_count,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END)
        AS invalid_status_count,
    CASE WHEN COUNT(*) = 1 THEN MAX(amount) END AS amount,
    CASE WHEN COUNT(*) = 1 THEN MAX(status) END AS status
FROM silver.normalized_records
WHERE record_id IS NOT NULL
GROUP BY source_system, record_id;
