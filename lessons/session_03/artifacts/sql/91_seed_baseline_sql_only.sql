DECLARE @Confirmation varchar(80) = 'NO';

IF @Confirmation <> 'LOAD SESSION 03 SQL ONLY BASELINE'
    THROW 50191, 'Confirm the isolated training Warehouse and edit the confirmation phrase.', 1;

BEGIN TRY
    BEGIN TRANSACTION;
    DELETE FROM gold.reconciliation;
    DELETE FROM bronze.system_a;
    DELETE FROM bronze.system_b;

    INSERT INTO bronze.system_a (RecordId, Amount, Status)
    VALUES
        ('A001', '100.00', 'Active'),
        ('A002', '200.00', 'Active'),
        ('A003', '300.00', 'Active'),
        ('A005', '500.00', 'Active'),
        ('A005', '500.00', 'Active'),
        ('A006', 'not provided', 'Active');

    INSERT INTO bronze.system_b (Reference, Total, State)
    VALUES
        (' a001 ', '100.00', 'ACTIVE'),
        ('A002', '250.00', 'ACTIVE'),
        ('A004', '400.00', 'ACTIVE'),
        ('A005', '500.00', 'ACTIVE'),
        ('A006', '600.00', 'ACTIVE');

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    THROW;
END CATCH;

SELECT 'SQL-only fixture loaded; this does not validate Dataflow ingestion' AS result;
