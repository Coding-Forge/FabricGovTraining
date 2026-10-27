EXEC gold.usp_refresh_reconciliation
    @BatchId = 'training-2026-10-28-baseline';

SELECT *
FROM gold.reconciliation
ORDER BY record_id;
