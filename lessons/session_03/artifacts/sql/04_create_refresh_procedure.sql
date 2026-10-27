CREATE PROCEDURE gold.usp_refresh_reconciliation
    @BatchId varchar(64)
AS
BEGIN
    SET NOCOUNT ON;

    IF @BatchId IS NULL OR TRIM(@BatchId) = ''
        THROW 50001, 'A comparison batch identifier is required.', 1;

    BEGIN TRY
        BEGIN TRANSACTION;

        IF NOT EXISTS (SELECT 1 FROM bronze.system_a)
           OR NOT EXISTS (SELECT 1 FROM bronze.system_b)
            THROW 50002, 'Both teaching snapshots must contain rows.', 1;

        IF EXISTS
        (
            SELECT 1
            FROM silver.normalized_records
            WHERE record_id IS NULL
        )
            THROW 50003, 'Blank record keys require investigation.', 1;

        DELETE FROM gold.reconciliation;

        ;WITH a AS
        (
            SELECT *
            FROM silver.record_summary
            WHERE source_system = 'A'
        ),
        b AS
        (
            SELECT *
            FROM silver.record_summary
            WHERE source_system = 'B'
        )
        INSERT INTO gold.reconciliation
        (
            batch_id, published_at_utc, record_id,
            a_row_count, b_row_count, a_amount, b_amount,
            a_status, b_status, classification
        )
        SELECT
            @BatchId,
            SYSUTCDATETIME(),
            COALESCE(a.record_id, b.record_id),
            COALESCE(a.source_row_count, 0),
            COALESCE(b.source_row_count, 0),
            a.amount,
            b.amount,
            a.status,
            b.status,
            CASE
                WHEN a.source_row_count > 1 OR b.source_row_count > 1
                    THEN 'DUPLICATE_KEY'
                WHEN COALESCE(a.invalid_amount_count, 0) > 0
                  OR COALESCE(b.invalid_amount_count, 0) > 0
                    THEN 'INVALID_AMOUNT'
                WHEN COALESCE(a.invalid_status_count, 0) > 0
                  OR COALESCE(b.invalid_status_count, 0) > 0
                    THEN 'INVALID_STATUS'
                WHEN b.record_id IS NULL THEN 'ONLY_IN_A'
                WHEN a.record_id IS NULL THEN 'ONLY_IN_B'
                WHEN a.amount <> b.amount AND a.status <> b.status
                    THEN 'AMOUNT_AND_STATUS_MISMATCH'
                WHEN a.amount <> b.amount THEN 'AMOUNT_MISMATCH'
                WHEN a.status <> b.status THEN 'STATUS_MISMATCH'
                ELSE 'MATCH'
            END
        FROM a
        FULL OUTER JOIN b ON a.record_id = b.record_id;

        IF EXISTS
        (
            SELECT record_id
            FROM gold.reconciliation
            GROUP BY record_id
            HAVING COUNT(*) > 1
        )
            THROW 50004, 'Published record keys must be unique.', 1;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
