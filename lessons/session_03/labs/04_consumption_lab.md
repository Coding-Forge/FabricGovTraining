# Lab 4: Consumption architecture

**Session 3 | October 28, 2026 | 20 minutes**  
**Lesson output:** A reusable model/report and a documented consumption, access, and freshness decision.

## Before you begin

Use the [setup runbook](README.md). Lab 3 must leave a verified baseline in `gold.reconciliation`. You need the approved semantic-model creation route, permission to author a training report, and an approved consumer test identity.

Direct Lake availability and creation experiences depend on the target tenant. Do not assume creating a Warehouse automatically creates the required model.

## Task 1: Select and inspect the actual model mode

1. Open the approved model creation experience for the training Warehouse.
2. Select the physical `gold.reconciliation` table, not a report-specific copy of Bronze.
3. Create or inspect the explicitly named training semantic model. Name the model table `Reconciliation`.
4. Inspect the table's actual mode: Direct Lake, Import, or DirectQuery. Record it and the relevant connection/identity behavior.
5. If Direct Lake is used, identify the available variant and source path. Do not assume a SQL view supports the same behavior as a physical Delta table.
6. If the planned mode is unavailable, use an approved, preflighted alternative and record the deviation. A verified Import model is preferable to an unverified Direct Lake claim.

**Checkpoint:** You can distinguish model reuse from storage/query mode. Record-level reconciliation remains in Gold.

## Task 2: Create the shared measures

1. Open `artifacts/dax/reconciliation_measures.dax`.
2. Create **each measure separately** in the model, in file order. The file is not a DAX query or a bulk-import script.
3. Confirm the model table name is exactly `Reconciliation`.
4. Format `Match Rate` as a percentage with two decimal places.
5. Explain why `Compared Records` counts six Gold keys, not eleven source rows.

**Expected unfiltered baseline:**

| Measure | Expected value |
| --- | --- |
| Compared Records | 6 |
| Matched Records | 1 |
| Exception Records | 5 |
| Match Rate | 16.67% |

An exception is any classification other than `MATCH`, including quality exceptions.

## Task 3: Build an investigable report

1. Create four cards for the measures.
2. Add a classification breakdown using classification and `Compared Records`.
3. Add a detail table with record ID, A/B amounts, A/B statuses, classification, batch ID, and publication time.
4. Trace A002's 200.00 versus 250.00 to the SQL result.
5. Trace A005 to its duplicate-source count; do not imply its missing projected A amount is zero.
6. Filter to `AMOUNT_MISMATCH`. Expect one compared record, zero matched, one exception, and a 0% match rate.
7. Clear filters and verify the baseline again. Explain how `KEEPFILTERS` preserves the selected classification context.

**Checkpoint:** Summary and detail agree with the comparison contract. A timestamp in a current-snapshot table does not create historical data.

## Task 4: Compare direct SQL and test access

1. Query `gold.reconciliation` from the approved SQL editor/client and group by classification.
2. Compare those counts with the unfiltered report.
3. Decide which consumers actually need SQL access.
4. Open the approved report/app as the intended consumer, not as a workspace administrator. Have the facilitator perform this test if a separate approved identity is required.
5. Record whether viewing the report and authoring over the shared model require distinct permissions. Do not grant workspace editing solely to make a reader test pass.
6. Explain why semantic-model RLS and DAX measures do not automatically protect or define direct SQL/OneLake consumption.

If consumer testing is unavailable, mark it blocked. The presenter's successful view is not substitute evidence.

## Task 5: Establish freshness

1. Record the Gold batch label and publication time.
2. Perform the mode-specific refresh/framing step or verify the applicable query/freshness behavior.
3. Compare report metadata and known totals with Gold.
4. Record the four gates: source completion, SQL publication, model freshness, and consumer visibility.

Complete the decision:

| Item | Your answer and evidence |
| --- | --- |
| Audience, model name, source table | Complete |
| Actual mode/variant and rationale | Complete |
| Location of classifications versus reporting measures | Complete |
| Approved direct SQL consumers and permission owner | Complete |
| Consumer test identity role and result | Complete |
| Mode-specific freshness evidence | Complete |
| Model/report support owner | Complete |

**Submit:** Model/report location, unfiltered and filtered results, access/freshness evidence, and decision. Do not attach credentials.

**Previous:** [Lab 3](03_sql_engineering_lab.md)  
**Next:** [Lab 5: Operations](05_operations_lab.md)
