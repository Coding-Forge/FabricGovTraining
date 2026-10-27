# Lesson 3: Curated SQL engineering

**Session 3 | October 28, 2026 | 50 minutes**  
**Blueprint:** [Module 3](../../session_3_blueprint.md#module-3-curated-sql-engineering---50-minutes)  
**Lesson output:** Curated Warehouse objects and explainable reconciliation results.

## What this lesson teaches

SQL curation turns source data into a business result that can be inspected, repeated, and trusted. The important work is not writing a join as quickly as possible. It is deciding what values mean, which records are eligible for comparison, and how an exception remains visible.

We will use the two synthetic extracts from Lesson 2. The examples deliberately retain a duplicate key and an invalid amount. A correct solution explains these conditions instead of deleting them to make the result appear successful.

Allocate five minutes to landing data, ten to normalization, ten to quality and comparison logic, fifteen to the procedure walkthrough, and ten to execution and interpretation. Prepare the objects before class; do not spend the lesson typing every statement. The SQL blocks below are reference material for the walkthrough.

**Execution boundary:** These examples target an isolated Fabric **Warehouse**, not the Lakehouse SQL analytics endpoint. Run each object-definition block separately. Preflight the SQL in the target tenant. The examples replace only the named training result table, but must not be redirected to production objects.

## 1. Land source-aligned tables

The landing layer should preserve what the sources supplied. If System A calls a column `RecordId`, retaining that name makes it easier to trace the data back to the file. We will align the names in Silver.

Create the three schemas once, executing each statement separately. If a schema already exists, do not recreate it.

```sql
CREATE SCHEMA bronze;
```

```sql
CREATE SCHEMA silver;
```

```sql
CREATE SCHEMA gold;
```

Create the landing tables before configuring the Dataflow Gen2 destinations in Lesson 2. These are setup statements, not refresh statements; do not run them again against existing objects.

```sql
CREATE TABLE bronze.system_a
(
    RecordId varchar(100),
    Amount varchar(100),
    Status varchar(100)
);

CREATE TABLE bronze.system_b
(
    Reference varchar(100),
    Total varchar(100),
    State varchar(100)
);
```

The lengths and text types are suitable for the controlled synthetic inputs, not a universal source schema. Real data requires explicit length, encoding, precision, and schema-drift decisions.

Load the files through the dataflow, then inspect the evidence:

```sql
SELECT 'A' AS source_system, COUNT(*) AS row_count
FROM bronze.system_a
UNION ALL
SELECT 'B', COUNT(*)
FROM bronze.system_b;

SELECT RecordId, Amount, Status
FROM bronze.system_a
ORDER BY RecordId;
```

Expect six System A rows and five System B rows. A005 must appear twice in System A, and A006 must retain `not provided` as its amount. If these conditions are missing, investigate ingestion before continuing.

## 2. Normalize mismatched structures

Normalization creates a common vocabulary without pretending the sources were originally identical.

Both sources will expose `record_id`, `amount`, and `status`. We will trim identifier whitespace, uppercase identifiers and statuses, and convert amounts to `decimal(18,2)`. These are business rules for this controlled example. In another domain, identifier case may be significant and must not be changed.

Using a decimal makes monetary comparison explicit. Floating-point approximation is unnecessary for the two-decimal amounts in this lesson. For real sources, define currency, locale, scale, rounding, and tolerance rules before conversion. A conversion to two decimal places is not itself validation that a source had exactly two decimal places.

```sql
CREATE VIEW silver.normalized_records
AS
SELECT
    CAST('A' AS varchar(1)) AS source_system,
    RecordId AS raw_record_id,
    Amount AS raw_amount,
    Status AS raw_status,
    NULLIF(UPPER(TRIM(RecordId)), '') AS record_id,
    TRY_CONVERT(decimal(18,2), NULLIF(TRIM(Amount), '')) AS amount,
    NULLIF(UPPER(TRIM(Status)), '') AS status
FROM bronze.system_a
UNION ALL
SELECT
    CAST('B' AS varchar(1)),
    Reference,
    Total,
    State,
    NULLIF(UPPER(TRIM(Reference)), ''),
    TRY_CONVERT(decimal(18,2), NULLIF(TRIM(Total), '')),
    NULLIF(UPPER(TRIM(State)), '')
FROM bronze.system_b;
```

`TRY_CONVERT` returns a null when a nonblank value cannot be converted. We also explicitly turn blank text into null before conversion. A null amount means that a usable number is unavailable; it does not mean zero.

Raw values remain available beside their normalized counterparts. This is what lets an investigator see that A006 came from `not provided` rather than guessing why a numeric value is missing.

A view stores a query definition, not a separately loaded snapshot of its result. Views are useful here because the small normalization can be reused without another physical table. They will reflect changes in Bronze, which is another reason to control ingestion while reconciliation runs.

```sql
SELECT
    source_system, raw_record_id, record_id,
    raw_amount, amount, raw_status, status
FROM silver.normalized_records
ORDER BY record_id, source_system;
```

The System B value ` a001 ` should now be `A001`. Both source status values should normalize to `ACTIVE`.

## 3. Detect quality problems before joining

Suppose a key occurs twice in System A and once in System B. A direct join produces two joined rows for that key. If both sides contain duplicates, the multiplication can be larger. Counting those joined rows as business records would change the output grain.

We must therefore evaluate uniqueness before comparison. For this lesson, a duplicate is an exception, even if the duplicate rows have identical amounts. The source owner, not the join implementation, decides whether a duplicate can be ignored.

Create a summary with one row per source and normalized key:

```sql
CREATE VIEW silver.record_summary
AS
SELECT
    source_system,
    record_id,
    COUNT(*) AS source_row_count,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)
        AS invalid_amount_count,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END)
        AS invalid_status_count,
    CASE WHEN COUNT(*) = 1 THEN MAX(amount) END AS amount,
    CASE WHEN COUNT(*) = 1 THEN MAX(status) END AS status
FROM silver.normalized_records
WHERE record_id IS NOT NULL
GROUP BY source_system, record_id;
```

The use of `MAX` does not choose a winning duplicate. It exposes a value only when exactly one source row exists. For duplicate keys, those projected values remain null and the row count records the ambiguity.

Blank keys are excluded from this summary because an absent identifier cannot serve as a comparable business key. They remain visible in `silver.normalized_records`. Our teaching procedure will block publication when they exist rather than silently losing them.

```sql
SELECT *
FROM silver.record_summary
WHERE source_row_count > 1
   OR invalid_amount_count > 0
   OR invalid_status_count > 0;

SELECT *
FROM silver.normalized_records
WHERE record_id IS NULL;
```

Expect a duplicate summary for System A A005 and an invalid-amount summary for System A A006. The blank-key query should return no rows for the supplied files.

## 4. Define reconciliation and exception rules

The business result must distinguish at least three ideas: a comparable match, a comparable difference, and a record that cannot safely be compared.

For this lesson, each nonblank key receives one classification in the following order:

1. `DUPLICATE_KEY`: either source has more than one row for the key.
2. `INVALID_AMOUNT`: an existing source row has no usable amount.
3. `INVALID_STATUS`: an existing source row has no usable status.
4. `ONLY_IN_A` or `ONLY_IN_B`: the other source has no record.
5. `AMOUNT_AND_STATUS_MISMATCH`, `AMOUNT_MISMATCH`, or `STATUS_MISMATCH`: both records are usable but differ.
6. `MATCH`: both usable records agree.

Order matters. If a duplicated record also contains an invalid amount, the published primary classification is `DUPLICATE_KEY`. The Silver evidence still exposes the other problem. A single classification is a reporting choice, not a claim that only one issue can exist.

A full outer join retains keys that occur in only one source. An inner join would omit those exceptions entirely and therefore answer a different business question.

## 5. Publish through a stored procedure

A stored procedure is a named unit of SQL work that can be executed repeatedly. Creating it defines the work; `EXEC` performs the work.

This is useful because the transformation sequence no longer depends on a person remembering which query to run next. It can later be invoked by a validated orchestration activity. A procedure does not create a schedule, repair credentials, or guarantee that the upstream sources are complete.

First create the physical Gold table. We use a table rather than only a view so there is an explicit publication step and a stable object for downstream consumption.

```sql
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
```

The procedure below publishes the current snapshot result. It is not a historical store: each successful execution replaces the previous Gold rows.

```sql
CREATE PROCEDURE gold.usp_refresh_reconciliation
    @BatchId varchar(64)
AS
BEGIN
    SET NOCOUNT ON;

    IF @BatchId IS NULL OR TRIM(@BatchId) = ''
        THROW 50001, 'A comparison batch identifier is required.', 1;

    BEGIN TRY
        BEGIN TRANSACTION;

        IF NOT EXISTS (SELECT 1 FROM bronze.system_a)
           OR NOT EXISTS (SELECT 1 FROM bronze.system_b)
            THROW 50002, 'Both teaching snapshots must contain rows.', 1;

        IF EXISTS
        (
            SELECT 1
            FROM silver.normalized_records
            WHERE record_id IS NULL
        )
            THROW 50003, 'Blank record keys require investigation.', 1;

        DELETE FROM gold.reconciliation;

        ;WITH a AS
        (
            SELECT *
            FROM silver.record_summary
            WHERE source_system = 'A'
        ),
        b AS
        (
            SELECT *
            FROM silver.record_summary
            WHERE source_system = 'B'
        )
        INSERT INTO gold.reconciliation
        (
            batch_id, published_at_utc, record_id,
            a_row_count, b_row_count, a_amount, b_amount,
            a_status, b_status, classification
        )
        SELECT
            @BatchId,
            SYSUTCDATETIME(),
            COALESCE(a.record_id, b.record_id),
            COALESCE(a.source_row_count, 0),
            COALESCE(b.source_row_count, 0),
            a.amount,
            b.amount,
            a.status,
            b.status,
            CASE
                WHEN a.source_row_count > 1 OR b.source_row_count > 1
                    THEN 'DUPLICATE_KEY'
                WHEN COALESCE(a.invalid_amount_count, 0) > 0
                  OR COALESCE(b.invalid_amount_count, 0) > 0
                    THEN 'INVALID_AMOUNT'
                WHEN COALESCE(a.invalid_status_count, 0) > 0
                  OR COALESCE(b.invalid_status_count, 0) > 0
                    THEN 'INVALID_STATUS'
                WHEN b.record_id IS NULL THEN 'ONLY_IN_A'
                WHEN a.record_id IS NULL THEN 'ONLY_IN_B'
                WHEN a.amount <> b.amount AND a.status <> b.status
                    THEN 'AMOUNT_AND_STATUS_MISMATCH'
                WHEN a.amount <> b.amount THEN 'AMOUNT_MISMATCH'
                WHEN a.status <> b.status THEN 'STATUS_MISMATCH'
                ELSE 'MATCH'
            END
        FROM a
        FULL OUTER JOIN b ON a.record_id = b.record_id;

        IF EXISTS
        (
            SELECT record_id
            FROM gold.reconciliation
            GROUP BY record_id
            HAVING COUNT(*) > 1
        )
            THROW 50004, 'Published record keys must be unique.', 1;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
```

The transaction groups the Gold replacement and its uniqueness check. If an error occurs, the replacement must not leave a committed empty or partial Gold result. The error is rethrown so a caller can detect failure rather than interpreting it as success.

This is a deliberately small teaching pattern. It rejects empty inputs because the lab expects two populated snapshots; a production contract must distinguish a legitimate empty extract from a failed delivery. It publishes duplicates and invalid amounts as visible exceptions but blocks blank keys. These policies must be approved by the business owner for a real workload.

The supplied `@BatchId` labels the publication; it does **not** prove that both sources belong to that batch. Before executing, a supervisor must confirm that the intended source pair is fully loaded and that no refresh is running. Keep source loading and reconciliation serialized in the lab. Production requires durable source/batch control and an appropriate concurrency policy.

## 6. Execute, inspect, and repeat

After confirming the completed source pair, execute:

```sql
EXEC gold.usp_refresh_reconciliation
    @BatchId = 'training-2026-10-28-baseline';

SELECT record_id, a_amount, b_amount, classification
FROM gold.reconciliation
ORDER BY record_id;

SELECT classification, COUNT(*) AS record_count
FROM gold.reconciliation
GROUP BY classification
ORDER BY classification;
```

The expected baseline is:

| Record ID | Classification | Explanation |
| --- | --- | --- |
| A001 | MATCH | Identifier formatting and status case normalize; amounts agree |
| A002 | AMOUNT_MISMATCH | System A has 200.00; System B has 250.00 |
| A003 | ONLY_IN_A | No System B record |
| A004 | ONLY_IN_B | No System A record |
| A005 | DUPLICATE_KEY | System A contains two rows; neither is selected as a winner |
| A006 | INVALID_AMOUNT | System A cannot supply a usable decimal amount |

There are six result rows, one match, and five exceptions. The eleven input rows do not imply eleven business records. The published grain is one row per distinct normalized nonblank key across both sources.

Execute the same procedure again without changing the sources. The same six business classifications should remain. The publication timestamp can change; the result must not grow to twelve rows.

This illustrates **idempotency**: repeating work for the same intended input state yields the same intended business state. It does not mean every operational field must remain byte-for-byte identical.

### Practice: follow a correction through the layers

Predict the result if System B A002 changes from 250.00 to 200.00. Then, if time and access permit, make that change in the synthetic source file, reload the complete source pair, and rerun the procedure.

The expected result is still six rows, now with two matches and four exceptions. A002 becomes `MATCH`; the other classifications remain unchanged.

Restore the baseline file and reload it before later lessons if they will use the baseline totals. Do not patch the Gold result directly: that would bypass the transformation and erase the connection between source evidence and published output.

## Lesson conclusion

We have moved from source-shaped text to consistent values, explicit quality rules, and a repeatable business result. The most important lesson is that data quality and reconciliation are part of the transformation contract, not cleanup activities to hide before a report is shown.

**Previous:** [Lesson 2](02_repeatable_ingestion.md)  
**Next:** [Lesson 4: Consumption architecture](04_consumption_architecture.md)

**Product references:** [T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area) and [Warehouse transactions](https://learn.microsoft.com/en-us/fabric/data-warehouse/transactions). The examples require target-tenant preflight; this document does not claim they have been executed in GCC High.
