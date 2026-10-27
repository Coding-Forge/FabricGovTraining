IF (SELECT COUNT(*) FROM gold.reconciliation) <> 6
    THROW 50110, 'Publish and verify the baseline before the rerun test.', 1;

DROP TABLE IF EXISTS #s03_before_rerun;
SELECT batch_id, record_id, a_row_count, b_row_count,
    a_amount, b_amount, a_status, b_status, classification
INTO #s03_before_rerun
FROM gold.reconciliation;

EXEC gold.usp_refresh_reconciliation
    @BatchId = 'training-2026-10-28-baseline';

IF (SELECT COUNT(*) FROM gold.reconciliation) <> 6
    THROW 50111, 'A rerun must retain six business keys.', 1;

IF EXISTS
(
    SELECT batch_id, record_id, a_row_count, b_row_count,
        a_amount, b_amount, a_status, b_status, classification
    FROM gold.reconciliation
    EXCEPT
    SELECT * FROM #s03_before_rerun
)
OR EXISTS
(
    SELECT * FROM #s03_before_rerun
    EXCEPT
    SELECT batch_id, record_id, a_row_count, b_row_count,
        a_amount, b_amount, a_status, b_status, classification
    FROM gold.reconciliation
)
    THROW 50112, 'Rerun changed the published business state.', 1;

DROP TABLE #s03_before_rerun;
SELECT 'PASS: business state unchanged; publication time may differ' AS check_result;
