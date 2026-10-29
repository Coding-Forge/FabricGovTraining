# Fabric Notebook survival guide

**Session 04 | Keep beside the notebook**  
Use only your assigned training workspace/Lakehouse. Confirm
[prerequisites](prerequisites.md) before class.

## Before Run all

Check **language, default Lakehouse, inputs, write targets, and approval flags**.
Read Markdown instructions first. Starters intentionally stop at unfinished
practice cells; the main lab also stops at its write-approval gate.
Saving code does not persist data, and visible old output is not proof of a
current successful run.

## Where am I reading or writing?

| Reference | Meaning |
| --- | --- |
| `Files/session_04/scenario/...` | Relative Spark path in the attached default Lakehouse |
| Path copied from Lakehouse UI | Explicit resource address; verify item/cloud and the copied path type |
| ADLS endpoint + container/prefix | External source used by the prepared ingestion pipeline |
| `s04_lab_device_silver` | Spark table in the current Lakehouse/catalog context |
| `gold.s04_lab_device_daily` | Warehouse table for Warehouse SQL, not an automatically shared Spark table |
| Laptop Downloads folder | Not directly readable by the hosted notebook |

Use the prepared folder and actual tenant path; do not guess endpoints or
collect files from a different Lakehouse to make a cell green.

## If it stops, classify before changing anything

| Symptom | First check |
| --- | --- |
| `NotImplementedError` / labeled safety stop | Complete the task or obtain write approval; not a service outage |
| `NameError` | Defining/import cells and execution order; if `spark` is missing, check PySpark/session |
| Syntax/indentation error | Code cell language, spelling, brackets, and indentation |
| Column cannot be resolved | `printSchema()` and the DataFrame being queried |
| File/table not found | Default Lakehouse, path/name/case, prepared source, and current catalog/schema |
| Access denied | Which resource and execution identity? Ask the owner; do not weaken controls |
| Package/module missing | Approved runtime/environment; do not install random fixes during delivery |
| Cell pending/slow | Session startup versus an active job; inspect progress before retrying |

Record the useful error, failing cell, input/target, and run reference.
Never include tokens/keys in screenshots. Opening a notebook does not grant
Lakehouse, ADLS connection/source, or Warehouse permissions.

## Everyday habits

Use completion and `help(F.trim)` instead of memorizing APIs. Add Markdown
describing the question, source scope, grain, and expected result.
Prefer built-in Spark expressions; a Spark Column is not a Python scalar.
Profile full batches, label samples, and aggregate/bound data before collecting
to pandas or the driver.

## Before declaring success

Verify counts, rejection reasons, grain, and actual persisted output.
Spark exports can be folders of part files; a Delta table has data files and a
transaction log. Do not manually edit underlying table files.
`append` can duplicate reruns; `overwrite` replaces a target; warm-up uses
`errorifexists` and needs a new approved target for a second creation.
Restart clears variables/temp views, not persisted tables.
Notebook success is not proof of Warehouse copy, Gold publication, or model
freshness. End your own session according to customer guidance.

**Practice:** [Notebook 101](00_notebook_101.md) -> [main lab](09_realistic_data_lab.md)
-> [independent challenge](10_independent_challenge.md).
