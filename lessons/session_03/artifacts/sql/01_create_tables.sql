IF OBJECT_ID('bronze.system_a', 'U') IS NULL
BEGIN
    CREATE TABLE bronze.system_a
    (
        RecordId varchar(100),
        Amount varchar(100),
        Status varchar(100)
    );
END;

IF OBJECT_ID('bronze.system_b', 'U') IS NULL
BEGIN
    CREATE TABLE bronze.system_b
    (
        Reference varchar(100),
        Total varchar(100),
        State varchar(100)
    );
END;

IF OBJECT_ID('gold.reconciliation', 'U') IS NULL
BEGIN
    CREATE TABLE gold.reconciliation
    (
        batch_id varchar(64) NOT NULL,
        published_at_utc datetime2(6) NOT NULL,
        record_id varchar(100) NOT NULL,
        a_row_count int NOT NULL,
        b_row_count int NOT NULL,
        a_amount decimal(18,2),
        b_amount decimal(18,2),
        a_status varchar(100),
        b_status varchar(100),
        classification varchar(40) NOT NULL
    );
END;
