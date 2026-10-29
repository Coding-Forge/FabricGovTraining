-- Scenario tier only. Run once in a fresh, isolated training Warehouse.
-- Do not automatically drop/alter existing targets or run this in the Lakehouse endpoint.
IF SCHEMA_ID('stg') IS NULL EXEC('CREATE SCHEMA stg');
IF SCHEMA_ID('gold') IS NULL EXEC('CREATE SCHEMA gold');

CREATE TABLE stg.s04_lab_order_line
(
    batch_id varchar(64) NOT NULL,
    order_id varchar(20) NOT NULL,
    line_number int NOT NULL,
    order_date date NOT NULL,
    order_status varchar(20) NOT NULL,
    customer_id varchar(20) NOT NULL,
    customer_name varchar(100) NOT NULL,
    customer_region varchar(20) NOT NULL,
    sku varchar(30) NOT NULL,
    product_category varchar(20) NOT NULL,
    quantity int NOT NULL,
    unit_price decimal(18,2) NOT NULL,
    line_amount decimal(18,2) NOT NULL
);

CREATE TABLE gold.s04_lab_order_line
(
    batch_id varchar(64) NOT NULL,
    order_id varchar(20) NOT NULL,
    line_number int NOT NULL,
    order_date date NOT NULL,
    order_status varchar(20) NOT NULL,
    customer_id varchar(20) NOT NULL,
    customer_name varchar(100) NOT NULL,
    customer_region varchar(20) NOT NULL,
    sku varchar(30) NOT NULL,
    product_category varchar(20) NOT NULL,
    quantity int NOT NULL,
    unit_price decimal(18,2) NOT NULL,
    line_amount decimal(18,2) NOT NULL,
    published_at_utc datetime2(6) NOT NULL
);

CREATE TABLE stg.s04_lab_device_daily
(
    batch_id varchar(64) NOT NULL,
    reading_date date NOT NULL,
    device_id varchar(20) NOT NULL,
    site_id varchar(20) NOT NULL,
    device_type varchar(20) NOT NULL,
    reading_count bigint NOT NULL,
    min_temperature_c decimal(8,2) NOT NULL,
    max_temperature_c decimal(8,2) NOT NULL,
    avg_temperature_c decimal(8,2) NOT NULL
);

CREATE TABLE gold.s04_lab_device_daily
(
    batch_id varchar(64) NOT NULL,
    reading_date date NOT NULL,
    device_id varchar(20) NOT NULL,
    site_id varchar(20) NOT NULL,
    device_type varchar(20) NOT NULL,
    reading_count bigint NOT NULL,
    min_temperature_c decimal(8,2) NOT NULL,
    max_temperature_c decimal(8,2) NOT NULL,
    avg_temperature_c decimal(8,2) NOT NULL,
    published_at_utc datetime2(6) NOT NULL
);
