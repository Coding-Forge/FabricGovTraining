# Lab 3: Curated SQL engineering

**Session 3 | October 28, 2026 | 25 minutes**  
**Lesson output:** Explained reconciliation rows plus baseline, rerun, correction, and rejection evidence.

## Before you begin

Use the [setup runbook](README.md). Confirm both intended baseline snapshots are loaded (A = 6, B = 5), no ingestion is running, and the SQL editor targets your isolated **Warehouse**.

All SQL assets are under `artifacts/sql/`. Each file is a separate execution. If the facilitator already created the views/procedure, inspect those definitions instead of rerunning `CREATE`.

## Task 1: Inspect Bronze and create or inspect Silver

1. Run `02_create_normalized_view.sql` if it is not already installed.
2. Query `silver.normalized_records`, selecting the raw and normalized fields.
3. Explain why B's ` a001 ` becomes A001 and A006's amount becomes null instead of zero.
4. Run `03_create_summary_view.sql` if absent.
5. Query `silver.record_summary`, inspecting `source_row_count`, invalid counts, and projected amounts/statuses.
6. Verify A005 has two A rows and no arbitrarily chosen A amount. Verify A006 has one invalid A amount.
7. Query normalized rows with a null key. The baseline should return none.

**Checkpoint:** Duplicate, invalid-value, and blank-key handling are separate rules. A view does not freeze the underlying Bronze state.

## Task 2: Publish and check the baseline

1. Run `04_create_refresh_procedure.sql` if absent; inspect its validation, transaction, replacement, and error path.
2. Confirm the operator's source-pair readiness check. The batch label does not establish readiness.
3. Run `05_publish_baseline.sql`.
4. Run `06_check_results.sql` with `@Scenario = 'baseline'`.
5. Save the `PASS`, classification counts, and six result rows.

| Key | Expected classification |
| --- | --- |
| A001 | MATCH |
| A002 | AMOUNT_MISMATCH |
| A003 | ONLY_IN_A |
| A004 | ONLY_IN_B |
| A005 | DUPLICATE_KEY |
| A006 | INVALID_AMOUNT |

The full expected business fields are in `artifacts/data/expected/baseline.csv`. Empty CSV cells represent SQL nulls.

**Checkpoint:** Six business keys, one match, five exceptions. Explain why a full outer join is required and why a direct duplicate-to-detail join would change the grain.

## Task 3: Verify an unchanged rerun

1. Do not change or reload the sources while this test runs.
2. Run `07_test_rerun.sql`.
3. Record its result and repeat the baseline checker.
4. Explain why publication time may change while the intended business state does not.

**Pass condition:** Six rows remain, the business fields and batch label match the prior baseline, and the script reports `PASS`. This does not prove unattended orchestration.

## Task 4: Follow a correction through the actual ingestion path

1. Predict the effect of changing B/A002 from 250.00 to 200.00.
2. Replace only the active SharePoint `system_b.csv` with `artifacts/data/corrected/system_b.csv`. Do not add a second file alongside it.
3. Reload both intended snapshots in replace mode and verify completion/counts. Leave System A unchanged.
4. Execute:

```sql
EXEC gold.usp_refresh_reconciliation
    @BatchId = 'training-2026-10-28-corrected';
```

5. In `06_check_results.sql`, change `@Scenario` to `'corrected'` and run it.
6. Compare the published fields with `artifacts/data/expected/corrected.csv`.

**Pass condition:** Six keys remain; A002 is now `MATCH`; totals are two matches and four exceptions. Other rows are unchanged.

**If ingestion is blocked:** Predict the outcome and review expected data. Label this task as prepared evidence reviewed, not an observed end-to-end correction.

## Task 5: Restore baseline and test rejection

1. Follow the baseline reset sequence in the setup runbook: restore B's baseline file, reload both sources, run `05`, and run `06` with `'baseline'`.
2. With no other writers, run `08_test_blank_key_guard.sql` in one complete execution.
3. The script temporarily inserts a blank key in a transaction, expects error 50003, rolls back the insertion, and compares the prior Gold publication including its timestamp.
4. Record the final `PASS` and run the baseline checker again.

**Pass condition:** The blank row is absent, the previous Gold publication remains identical, and baseline checks pass. This verifies the pre-publication guard, not a simulated mid-write failure.

If an unexpected error appears, stop and contact the facilitator. Do not continue with a manually patched result or an open transaction.

## Completion record

| Check | State, evidence, and explanation |
| --- | --- |
| Raw-to-normalized trace for A001/A006 | Complete |
| Duplicate handling and classification precedence | Complete |
| Baseline publication and exact result check | Complete |
| Unchanged rerun | Complete |
| Source correction and corrected check | Complete |
| Baseline restoration and blank-key rejection | Complete |

**Submit:** Results and explanations. Leave the verified baseline published for Lab 4.

**Previous:** [Lab 2](02_ingestion_lab.md)  
**Next:** [Lab 4: Consumption](04_consumption_lab.md)
