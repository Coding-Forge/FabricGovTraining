CREATE VIEW silver.normalized_records
AS
SELECT
    CAST('A' AS varchar(1)) AS source_system,
    RecordId AS raw_record_id,
    Amount AS raw_amount,
    Status AS raw_status,
    NULLIF(UPPER(TRIM(RecordId)), '') AS record_id,
    TRY_CONVERT(decimal(18,2), NULLIF(TRIM(Amount), '')) AS amount,
    NULLIF(UPPER(TRIM(Status)), '') AS status
FROM bronze.system_a
UNION ALL
SELECT
    CAST('B' AS varchar(1)),
    Reference,
    Total,
    State,
    NULLIF(UPPER(TRIM(Reference)), ''),
    TRY_CONVERT(decimal(18,2), NULLIF(TRIM(Total), '')),
    NULLIF(UPPER(TRIM(State)), '')
FROM bronze.system_b;
