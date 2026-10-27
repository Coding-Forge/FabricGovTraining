# Session 03 lab setup and reset

**Audience:** SQL, Power Query, and Power BI practitioners  
**Scope:** Six labs supporting the existing Session 03 lessons, not additional sessions  
**Execution status:** The package includes offline checks. Fabric, SharePoint, Power BI, and GCC High execution must be verified in the delivery tenant.

## Start here

Use an approved, isolated training **Warehouse**, not a production Warehouse or the Lakehouse SQL analytics endpoint. Assign one Warehouse and one source folder per participant or pair. The scripts use fixed schema/object names, so simultaneous learners must not write to the same Warehouse.

These exercises fit inside the lesson allocations. They are not an additional 96 minutes after the three-hour session.

| Lab | Hands-on allocation | Lesson allocation | Output |
| --- | --- | --- | --- |
| [1. Architecture](01_architecture_lab.md) | 8 minutes | 25 minutes | Decision record and tool responsibilities |
| [2. Ingestion](02_ingestion_lab.md) | 18 minutes | 35 minutes | Verified replace-mode load and ingestion contract |
| [3. SQL engineering](03_sql_engineering_lab.md) | 25 minutes | 50 minutes | Baseline, rerun, correction, and guard-test evidence |
| [4. Consumption](04_consumption_lab.md) | 20 minutes | 35 minutes | Shared model, measures, report, access/freshness decision |
| [5. Operations](05_operations_lab.md) | 15 minutes | 25 minutes | Runbook, finding, learning action, and ownership |
| [6. Exit review](06_exit_review_lab.md) | 10 minutes | 10 minutes | Completion record and accepted follow-ups |

Facilitators should demonstrate the prepared SQL instead of having learners type every definition. Labs 1, 5, and 6 include decision/tabletop work; not every architecture or operating concept requires a new Fabric artifact.

## Package inventory

All asset paths below are relative to `lessons/session_03/`.

| Location | Contents |
| --- | --- |
| `labs/` | This setup/reset runbook and six participant guides |
| `artifacts/data/baseline/` | `system_a.csv` and `system_b.csv` |
| `artifacts/data/corrected/` | Replacement `system_b.csv`; changes only A002 from 250.00 to 200.00 |
| `artifacts/data/expected/` | Baseline/corrected Gold business rows; blank CSV cells represent SQL nulls |
| `artifacts/sql/` | Setup, views, procedure, publication, checks, retry/guard exercises, and guarded reset/seed scripts |
| `artifacts/dax/` | Four measure definitions; create them individually |
| `artifacts/validate_lab_assets.py` | Offline fixture, source-alignment, and package-link checks |
| `artifacts/build_lab_workbook.py` | Rebuild the printable lab workbook using the existing handbook style |
| `pdf/session_03_lab_workbook.pdf` | Printable participant workbook including setup/reset |

Do not upload the entire `artifacts/data/` tree into the ingestion folder. The dataflow must see only the two intended active files, not the corrected and expected-result copies.

## Facilitator readiness gate

Complete this before class using the approved training identities. Write the actual identity role and evidence location, but never credentials.

| Gate | Required evidence | If blocked |
| --- | --- | --- |
| Workspace/capacity | Correct tenant, capacity, item creation, and SQL execution | Use approved prepared evidence; record blocked paths |
| Source | Read access to the isolated SharePoint folder; matching synthetic files | SQL-only seed can support later labs, not prove ingestion |
| Destination | Dataflow can replace both existing text landing tables | Stop live ingestion and capture a scoped finding |
| SQL | Setup, procedure, baseline, checks, rerun, and guard test succeed | Use source/result walkthrough; do not claim live completion |
| Model/report | Verified creation route and actual mode; required refresh/framing | Use an approved alternative mode or label prepared evidence |
| Consumer | Intended read-only identity sees the approved report, not broad edit access | Access remains unverified; do not elevate to bypass it |
| Automation | Direct schedule and optional pipeline invocation tested separately | Explicitly supervise downstream steps |
| Safety | No concurrent writer; no production objects or real employee files | Do not proceed |

If participant access is insufficient, use an approved facilitator demonstration and label it accordingly. Do not change production tenant settings or broad roles to rescue a lab.

## Prepare the environment

1. Record the tenant, workspace, dedicated Warehouse, approved source folder, pair identifier, and technical owner.
2. Stop or disable **only the lab's** conflicting schedules with owner approval. Do not touch shared schedules.
3. Run `artifacts/sql/00_create_schemas.sql`, then `01_create_tables.sql`, in the dedicated Warehouse SQL editor. These create absent objects without clearing existing rows. If the names already contain unknown data or incompatible schemas, stop and use a fresh training Warehouse; the scripts do not repair existing objects.
4. Upload only `artifacts/data/baseline/system_a.csv` and `system_b.csv` to the approved active source folder.
5. Prepare Dataflow Gen2 connections and text-to-text destination mappings. Use Lab 2 for the detailed load instructions.
6. Preflight `02_create_normalized_view.sql`, `03_create_summary_view.sql`, and `04_create_refresh_procedure.sql`, each as a **separate complete execution**. `CREATE VIEW` and `CREATE PROCEDURE` must be the first statement in their batch. The files deliberately contain no `GO`; do not concatenate them.
7. The three `CREATE` definitions are one-time setup. If already installed by the facilitator, learners inspect them rather than rerunning `CREATE`. Record which objects already exist. If they need replacing, use a fresh Warehouse or an explicitly reviewed change, not an automatic drop.
8. Complete baseline ingestion. Confirm both refreshes and source scope before running `05_publish_baseline.sql`. Run `06_check_results.sql`, `07_test_rerun.sql`, and `08_test_blank_key_guard.sql` in separate executions. All should report `PASS` after the expected handled guard error.
9. Prepare the model/report route and a second, approved consumer identity. Refresh/framing and identity behavior depend on the actual mode.
10. Restore the baseline, retain source/refresh evidence, and agree an approved location for participant outputs.

The publication procedure's batch argument is only a label. The facilitator/operator must establish that both completed extracts belong together and prevent concurrent ingestion. This package does not add production-grade batch orchestration.

## SQL script order and scope

| Script | Purpose | When to run |
| --- | --- | --- |
| `00_create_schemas.sql` | Create absent training schemas | Initial setup |
| `01_create_tables.sql` | Create absent Bronze/Gold tables | Initial setup |
| `02_create_normalized_view.sql` | Align names, types, and raw evidence | Once, after tables |
| `03_create_summary_view.sql` | Count rows/quality per source and key | Once, after normalized view |
| `04_create_refresh_procedure.sql` | Publish current Gold transactionally | Once, after views |
| `05_publish_baseline.sql` | Execute with the baseline batch label | After the intended baseline pair completes |
| `06_check_results.sql` | Assert row counts, label, keys, values, and classifications | Baseline by default; edit scenario for corrected data |
| `07_test_rerun.sql` | Compare business state before/after repeat execution | Verified, unchanged baseline only |
| `08_test_blank_key_guard.sql` | Reject a temporary blank key and preserve published data | Verified baseline, no other writers |
| `90_reset_rows.sql` | Clear only the three named training tables, preserving definitions | Optional explicit reset; confirmation required |
| `91_seed_baseline_sql_only.sql` | Replace training rows with the synthetic baseline | Approved SQL-only fallback; confirmation required |

The guard test uses a session-local temporary snapshot and a transaction. The procedure rolls back the temporary source insertion; the test verifies the prior Gold rows, including publication metadata, are unchanged. This tests **pre-publication rejection**, not a simulated failure halfway through writing Gold. If any test reports an unexpected error, stop, inspect transaction state, and restore baseline before continuing.

## Reset to the baseline between exercises

1. Confirm the dedicated Warehouse and stop competing lab writers.
2. Replace the active SharePoint `system_b.csv` with the baseline copy. Restore System A from its baseline copy if it was changed.
3. Run replace-mode ingestion for both files; verify successful completion and counts of six and five.
4. Run `05_publish_baseline.sql`, then `06_check_results.sql` with `@Scenario = 'baseline'`.
5. Perform the chosen model's freshness step and confirm unfiltered report totals of six records, one match, and five exceptions.
6. Record the reset and its evidence. Do not patch Gold rows directly.

If a full row reset is needed, edit the confirmation in `90_reset_rows.sql` to the exact phrase printed in that file, then execute it only after confirming the isolated target. It clears Bronze and Gold data, not schemas, views, the procedure, or external artifacts. Both sources must then be reloaded before publication.

For a SQL-only continuation when SharePoint/Dataflow is blocked, edit the confirmation in `91_seed_baseline_sql_only.sql` and execute it. It clears the current Gold result and seeds both Bronze tables. Follow with `05` and `06`. Mark ingestion as **blocked** or **prepared evidence reviewed**; never claim that a SQL insert validated Dataflow.

## Completion states and evidence

For every lab, record one of: **participant completed**, **presenter demonstrated**, **prepared evidence reviewed**, or **blocked**. Keep screenshots/results in the approved delivery location with the lab number, pair identifier, timestamp, and input scenario. Sanitize connection errors and source locations before wider sharing.

Record live checks honestly. A package passing its offline validator does not prove Fabric SQL compatibility, SharePoint authentication, scheduled execution, Direct Lake availability, or consumer access.

From the training directory, run `python lessons/session_03/artifacts/validate_lab_assets.py` for the offline checks. Run `python lessons/session_03/artifacts/build_lab_workbook.py` to rebuild the workbook after editing its sources. The PDF builder reuses `lessons/build_pdfs.py` and its existing WeasyPrint, MarkdownIt, and Pygments dependencies.

## Cleanup after the workshop

Agree retention with the artifact owner. Disable only approved lab schedules that should not remain active. Review dependencies before deleting a source folder, connection, model, report, or Warehouse through the service. No supplied script drops a Warehouse, schema, connection, or shared item. Preserve participant evidence and unresolved findings before any approved cleanup.
