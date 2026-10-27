# Lab 2: Repeatable ingestion

**Session 3 | October 28, 2026 | 18 minutes**  
**Lesson output:** A verified replace-mode ingestion and a documented source, destination, and scheduling contract.

## Before you begin

Follow the [setup runbook](README.md). Required: an isolated Warehouse with the two Bronze tables, an approved SharePoint training folder containing only the active baseline files, and permission to author/run Dataflow Gen2.

Paths, connection names, and UI labels depend on the tenant. Use the approved connector and connection route; do not enter a commercial endpoint or create a gateway merely to bypass a Government connection failure.

## Task 1: Inspect the source contract

1. Confirm the active files are `system_a.csv` and `system_b.csv`, copied from `artifacts/data/baseline/`.
2. Record the approved site/folder, comparison scope, source owner, and how the pair is confirmed complete.
3. Confirm that corrected/expected CSVs are not in the selected ingestion path.
4. Confirm that the connection's execution identity can read the files, not only your interactive browser identity.

**Checkpoint:** You can identify the exact pair and execution context before creating a query.

## Task 2: Create or inspect the two queries

1. Open the approved training workspace and create or edit the prepared Dataflow Gen2.
2. Connect to the approved SharePoint source using the preflighted connection.
3. Filter the file list to the intended folder and exact System A file before reading its content.
4. Parse the CSV with a comma delimiter, promote the first row to headers, and inspect the three columns.
5. Remove or adjust automatic numeric conversions. Keep `RecordId`, `Amount`, and `Status` as text. Do not remove errors/duplicates to hide source problems.
6. Create the equivalent query for System B, retaining text `Reference`, `Total`, and `State`.
7. Inspect A005 twice in A and `not provided` for A006. Retain the spaces in B's first identifier until Silver normalization.

**Checkpoint:** System A preview has six rows; System B has five. Preview is not yet destination-load evidence.

## Task 3: Configure and run destinations

1. Select the existing `bronze.system_a` table in the correct Warehouse for System A.
2. Map all three text columns explicitly.
3. Select `bronze.system_b` for System B and map its text columns.
4. Inspect the supported destination settings and select validated **replace** behavior for these complete snapshots. Do not assume settings for another destination apply.
5. Save/publish using the available experience and run the dataflow.
6. Wait for both destination loads to succeed; inspect refresh history and record the run evidence.
7. Execute this read-only query in the Warehouse:

```sql
SELECT 'A' AS source_system, COUNT(*) AS row_count
FROM bronze.system_a
UNION ALL
SELECT 'B', COUNT(*) FROM bronze.system_b;
```

Expect A = 6 and B = 5. Inspect the actual tables to confirm A005 remains duplicated and A006's raw amount remains `not provided`.

## Task 4: Prove unchanged reload behavior

1. Run the unchanged ingestion again.
2. Wait for both loads and repeat the count/evidence checks.
3. Explain why the result is still six and five, rather than twelve and ten.
4. Explain why append alone would not correctly handle updates, deletes, or late arrivals in an incremental design.

**Completion check:** Two successful runs retain the same intended source state and evidence. If only one run was observed, record the rerun as unverified.

## Task 5: Record the trigger and dependency boundary

1. Inspect the available direct scheduling configuration. Record its execution identity, time zone, owner, and intended time.
2. Enable a lab schedule only with owner approval. A configured schedule is not proof of a successful scheduled run; retain actual run evidence if already preflighted, or mark it pending.
3. If a pipeline is available and preflighted, inspect its Dataflow activity and downstream SQL success dependency. Do not start SQL on a separate estimated time delay.
4. If pipeline invocation is blocked, document direct ingestion scheduling plus supervised SQL/model steps.
5. Decide whether a copy job would satisfy these file-selection/Power Query requirements. Record source/destination availability as an assumption until verified.

Complete the contract:

| Item | Your evidence or decision |
| --- | --- |
| Exact source pair and scope | Complete |
| Execution connection/owner and any approved gateway dependency | Complete |
| Destination names, column mappings, and update method | Complete |
| First and second run IDs/status/counts | Complete |
| Trigger and scheduled-execution evidence/state | Complete |
| What stops downstream work if either input fails | Complete |
| Full versus incremental choice and rationale | Complete |

**Failure branch:** If one source fails, stop publication and record the finding. With facilitator approval, the SQL-only seed in the setup runbook can support later labs, but ingestion remains blocked or demonstrated, not participant-completed.

**Submit:** Contract and sanitized run/count evidence. Leave the complete baseline pair loaded; do not publish Gold yet.

**Previous:** [Lab 1](01_architecture_lab.md)  
**Next:** [Lab 3: SQL engineering](03_sql_engineering_lab.md)
