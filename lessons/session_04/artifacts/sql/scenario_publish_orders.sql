-- Scenario v1 only. Require successful notebook checks, steward approval, and copy first.
-- Replaces the entire current teaching snapshot; not a production incremental load.
DECLARE @BatchId varchar(64) = 's04-lab-orders-001';

BEGIN TRY
    BEGIN TRANSACTION;

    IF (SELECT COUNT_BIG(*) FROM stg.s04_lab_order_line
        WHERE batch_id = @BatchId) <> 14391
        THROW 51201, 'Expected 14391 staged accepted order lines.', 1;

    IF EXISTS
    (
        SELECT order_id, line_number
        FROM stg.s04_lab_order_line
        WHERE batch_id = @BatchId
        GROUP BY order_id, line_number
        HAVING COUNT_BIG(*) > 1
    )
        THROW 51202, 'Staged order-line keys must be unique.', 1;

    IF EXISTS
    (
        SELECT 1 FROM stg.s04_lab_order_line
        WHERE batch_id = @BatchId
          AND (TRIM(order_id) = '' OR TRIM(customer_id) = ''
               OR TRIM(customer_name) = '' OR TRIM(sku) = ''
               OR customer_region NOT IN ('NORTH', 'SOUTH', 'EAST', 'WEST')
               OR product_category NOT IN ('PUMPS', 'FILTERS', 'VALVES', 'PARTS')
               OR order_status NOT IN ('NEW', 'PROCESSING', 'SHIPPED', 'CANCELLED')
               OR order_date < CAST('2026-10-01' AS date)
               OR order_date > CAST('2026-10-14' AS date)
               OR line_number <= 0 OR quantity <= 0 OR unit_price < 0
               OR line_amount <> CAST(quantity * unit_price AS decimal(18,2)))
    )
        THROW 51203, 'Staged accepted-line contract failed.', 1;

    IF (SELECT SUM(line_amount) FROM stg.s04_lab_order_line
        WHERE batch_id = @BatchId) <> 5643227.95
        THROW 51204, 'Unexpected scenario accepted-line amount.', 1;

    DELETE FROM gold.s04_lab_order_line;

    INSERT INTO gold.s04_lab_order_line
    (
        batch_id, order_id, line_number, order_date, order_status,
        customer_id, customer_name, customer_region, sku, product_category,
        quantity, unit_price, line_amount, published_at_utc
    )
    SELECT
        batch_id, order_id, line_number, order_date, order_status,
        customer_id, customer_name, customer_region, sku, product_category,
        quantity, unit_price, line_amount, SYSUTCDATETIME()
    FROM stg.s04_lab_order_line
    WHERE batch_id = @BatchId;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;

SELECT batch_id, COUNT_BIG(*) AS accepted_lines,
       SUM(line_amount) AS accepted_line_amount
FROM gold.s04_lab_order_line
GROUP BY batch_id;

SELECT order_date, customer_region, product_category, order_status,
       COUNT_BIG(*) AS accepted_lines, SUM(line_amount) AS accepted_line_amount
FROM gold.s04_lab_order_line
GROUP BY order_date, customer_region, product_category, order_status
ORDER BY order_date, customer_region, product_category, order_status;
