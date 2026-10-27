IF (SELECT COUNT(*) FROM gold.reconciliation) <> 6
    THROW 50120, 'Publish and verify the baseline before the guard test.', 1;

DROP TABLE IF EXISTS #s03_before_guard;
SELECT *
INTO #s03_before_guard
FROM gold.reconciliation;

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO bronze.system_a (RecordId, Amount, Status)
    VALUES (' ', '10.00', 'Active');

    EXEC gold.usp_refresh_reconciliation
        @BatchId = 'training-blank-key-must-not-publish';

    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    THROW 50121, 'Expected blank-key rejection did not occur.', 1;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    IF ERROR_NUMBER() <> 50003
        THROW;
END CATCH;

IF EXISTS (SELECT * FROM gold.reconciliation EXCEPT SELECT * FROM #s03_before_guard)
OR EXISTS (SELECT * FROM #s03_before_guard EXCEPT SELECT * FROM gold.reconciliation)
    THROW 50122, 'Failed publication changed the last successful Gold result.', 1;

IF EXISTS (SELECT 1 FROM silver.normalized_records WHERE record_id IS NULL)
    THROW 50123, 'The temporary blank source row was not rolled back.', 1;

DROP TABLE #s03_before_guard;
SELECT 'PASS: error 50003; source restored; prior publication unchanged' AS check_result;
