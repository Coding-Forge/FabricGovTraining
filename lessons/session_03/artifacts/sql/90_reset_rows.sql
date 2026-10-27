DECLARE @Confirmation varchar(80) = 'NO';

IF @Confirmation <> 'RESET SESSION 03 TRAINING ROWS'
    THROW 50190, 'Confirm the isolated training Warehouse and edit the confirmation phrase.', 1;

BEGIN TRY
    BEGIN TRANSACTION;
    DELETE FROM gold.reconciliation;
    DELETE FROM bronze.system_a;
    DELETE FROM bronze.system_b;
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    THROW;
END CATCH;

SELECT 'Training rows cleared; reload both baseline files before publication' AS result;
