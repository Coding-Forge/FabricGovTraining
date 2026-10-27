IF SCHEMA_ID('bronze') IS NULL
    EXEC('CREATE SCHEMA bronze');

IF SCHEMA_ID('silver') IS NULL
    EXEC('CREATE SCHEMA silver');

IF SCHEMA_ID('gold') IS NULL
    EXEC('CREATE SCHEMA gold');
