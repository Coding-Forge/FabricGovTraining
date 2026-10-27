DECLARE @Scenario varchar(10) = 'baseline';
DECLARE @DifferenceCount int;

IF @Scenario IS NULL OR @Scenario NOT IN ('baseline', 'corrected')
    THROW 50100, 'Scenario must be baseline or corrected.', 1;

IF (SELECT COUNT(*) FROM bronze.system_a) <> 6
   OR (SELECT COUNT(*) FROM bronze.system_b) <> 5
    THROW 50101, 'Expected six A rows and five B rows.', 1;

IF (SELECT COUNT(*) FROM gold.reconciliation) <> 6
    THROW 50102, 'Expected six published business keys.', 1;

IF EXISTS
(
    SELECT record_id
    FROM gold.reconciliation
    GROUP BY record_id
    HAVING COUNT(*) <> 1
)
    THROW 50103, 'Published business keys must be unique.', 1;

IF EXISTS
(
    SELECT 1
    FROM gold.reconciliation
    WHERE batch_id <> 'training-2026-10-28-' + @Scenario
)
    THROW 50104, 'Unexpected publication batch label.', 1;

;WITH expected AS
(
    SELECT
        record_id, a_row_count, b_row_count,
        a_amount, b_amount, a_status, b_status, classification
    FROM
    (
        VALUES
        ('A001', 1, 1, CAST(100 AS decimal(18,2)), CAST(100 AS decimal(18,2)),
            CAST('ACTIVE' AS varchar(100)), CAST('ACTIVE' AS varchar(100)), 'MATCH'),
        ('A002', 1, 1, 200, CASE WHEN @Scenario = 'corrected' THEN 200 ELSE 250 END,
            'ACTIVE', 'ACTIVE',
            CASE WHEN @Scenario = 'corrected' THEN 'MATCH' ELSE 'AMOUNT_MISMATCH' END),
        ('A003', 1, 0, 300, NULL, 'ACTIVE', NULL, 'ONLY_IN_A'),
        ('A004', 0, 1, NULL, 400, NULL, 'ACTIVE', 'ONLY_IN_B'),
        ('A005', 2, 1, NULL, 500, NULL, 'ACTIVE', 'DUPLICATE_KEY'),
        ('A006', 1, 1, NULL, 600, 'ACTIVE', 'ACTIVE', 'INVALID_AMOUNT')
    ) AS expected_rows
    (
        record_id, a_row_count, b_row_count,
        a_amount, b_amount, a_status, b_status, classification
    )
),
missing_rows AS
(
    SELECT * FROM expected
    EXCEPT
    SELECT record_id, a_row_count, b_row_count,
        a_amount, b_amount, a_status, b_status, classification
    FROM gold.reconciliation
),
unexpected_rows AS
(
    SELECT record_id, a_row_count, b_row_count,
        a_amount, b_amount, a_status, b_status, classification
    FROM gold.reconciliation
    EXCEPT
    SELECT * FROM expected
)
SELECT @DifferenceCount =
    (SELECT COUNT(*) FROM missing_rows) + (SELECT COUNT(*) FROM unexpected_rows);

IF @DifferenceCount <> 0
    THROW 50105, 'Published values differ from the expected scenario.', 1;

SELECT 'PASS' AS check_result, @Scenario AS scenario;
SELECT classification, COUNT(*) AS record_count
FROM gold.reconciliation
GROUP BY classification
ORDER BY classification;
