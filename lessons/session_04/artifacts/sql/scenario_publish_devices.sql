-- Scenario v1 only. Require successful notebook checks and copy first.
-- This transaction is independent of the order publication.
DECLARE @BatchId varchar(64) = 's04-lab-devices-001';

BEGIN TRY
    BEGIN TRANSACTION;

    IF (SELECT COUNT_BIG(*) FROM stg.s04_lab_device_daily
        WHERE batch_id = @BatchId) <> 700
        THROW 51301, 'Expected 700 staged device/day rows.', 1;

    IF EXISTS
    (
        SELECT device_id, reading_date
        FROM stg.s04_lab_device_daily
        WHERE batch_id = @BatchId
        GROUP BY device_id, reading_date
        HAVING COUNT_BIG(*) > 1
    )
        THROW 51302, 'Staged device/day keys must be unique.', 1;

    IF EXISTS
    (
        SELECT 1 FROM stg.s04_lab_device_daily
        WHERE batch_id = @BatchId
          AND (device_id NOT LIKE 'D[0-9][0-9][0-9]'
               OR device_id < 'D001' OR device_id > 'D050'
               OR site_id NOT IN ('S01', 'S02', 'S03', 'S04', 'S05')
               OR device_type NOT IN ('AMBIENT', 'COLD_STORE', 'PUMP')
               OR reading_count <= 0 OR reading_count > 288
               OR reading_date < CAST('2026-10-01' AS date)
               OR reading_date > CAST('2026-10-14' AS date)
               OR min_temperature_c < -40 OR max_temperature_c > 85
               OR min_temperature_c > max_temperature_c
               OR avg_temperature_c < min_temperature_c
               OR avg_temperature_c > max_temperature_c)
    )
        THROW 51303, 'Staged device summary contract failed.', 1;

    IF (SELECT SUM(reading_count) FROM stg.s04_lab_device_daily
        WHERE batch_id = @BatchId) <> 194545
        THROW 51304, 'Expected 194545 accepted device readings.', 1;

    DELETE FROM gold.s04_lab_device_daily;

    INSERT INTO gold.s04_lab_device_daily
    (
        batch_id, reading_date, device_id, site_id, device_type,
        reading_count, min_temperature_c, max_temperature_c,
        avg_temperature_c, published_at_utc
    )
    SELECT
        batch_id, reading_date, device_id, site_id, device_type,
        reading_count, min_temperature_c, max_temperature_c,
        avg_temperature_c, SYSUTCDATETIME()
    FROM stg.s04_lab_device_daily
    WHERE batch_id = @BatchId;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;

SELECT batch_id, COUNT_BIG(*) AS device_day_rows,
       SUM(reading_count) AS accepted_readings
FROM gold.s04_lab_device_daily
GROUP BY batch_id;

SELECT reading_date, site_id, device_type,
       SUM(reading_count) AS accepted_readings,
       MIN(min_temperature_c) AS minimum_temperature_c,
       MAX(max_temperature_c) AS maximum_temperature_c
FROM gold.s04_lab_device_daily
GROUP BY reading_date, site_id, device_type
ORDER BY reading_date, site_id, device_type;
