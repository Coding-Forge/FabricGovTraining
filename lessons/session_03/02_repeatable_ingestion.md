# Lesson 2: Repeatable ingestion

**Session 3 | October 28, 2026 | 35 minutes**  
**Blueprint:** [Module 2](../session_3_blueprint.md#module-2-repeatable-ingestion---35-minutes)  
**Lesson output:** A repeatable ingestion pattern with its scheduling method documented.

## What this lesson teaches

Ingestion is the controlled movement of source data into a location where it can be processed reliably. A successful connection is only the beginning. We must also know which files were selected, how their values were interpreted, where their rows were written, and what another execution will do.

This lesson uses Dataflow Gen2 because it builds on familiar Power Query skills. We will preserve source evidence, select explicit destinations, distinguish full replacement from incremental processing, and separate scheduling from orchestration.

Allocate approximately five minutes to the source contract, fifteen minutes to the dataflow walkthrough, seven minutes to load strategies, and eight minutes to scheduling and the participant output.

## 1. Establish a source contract

A SharePoint folder is a storage location, not a complete definition of a dataset. It may contain current files, previous extracts, temporary files, or unrelated documents. If a query combines everything it can see, its results can change when someone adds a file that was never intended to participate.

For this lesson, define two exact inputs in an approved training folder: `system_a.csv` and `system_b.csv`. They are synthetic, complete snapshots of the same comparison scope. They are not employee data and do not contain personal information.

Use the following content when preparing the files.

### System A

```csv
RecordId,Amount,Status
A001,100.00,Active
A002,200.00,Active
A003,300.00,Active
A005,500.00,Active
A005,500.00,Active
A006,not provided,Active
```

### System B

```csv
Reference,Total,State
 a001 ,100.00,ACTIVE
A002,250.00,ACTIVE
A004,400.00,ACTIVE
A005,500.00,ACTIVE
A006,600.00,ACTIVE
```

System A contains six rows. System B contains five. The duplicate A005 and invalid A006 amount are intentional. They are not errors to remove before the exercise; they are evidence the reconciliation must explain.

The surrounding spaces and lowercase characters in System B's first identifier are also intentional. They let us distinguish a harmless representation difference from a business difference.

A source contract should state the file location and selection rules, expected columns, value formats, snapshot scope, source owner, and the condition that means the extract is ready. If two files are intended to represent the same reporting period, their presence alone does not prove they represent the same period. The source owner must provide that assurance through a controlled delivery convention or explicit batch metadata.

## 2. Build or inspect the Dataflow Gen2 ingestion

Dataflow Gen2 uses Power Query to connect, select, shape, and load data. This is useful when practitioners want a visible sequence of transformation steps rather than a custom program.

For this workload, keep ingestion focused on a small set of responsibilities: select the intended files, read their tabular structure, preserve their source values, and write them to explicit landing tables.

### Connect with the intended execution identity

Use an approved connection to the SharePoint site. Confirm that the connection can read the intended location and that the account or identity used for scheduled execution has the necessary access.

The presenter's ability to open a file in a browser is not proof that a scheduled dataflow can read it. Interactive access and service execution may use different connections, identities, policies, or gateway paths.

Do not add a gateway simply because a connection fails. Establish whether the actual source and network configuration require one. If a gateway is part of the approved path, validate its availability and connection visibility before class.

### Filter deliberately

Inspect the file list before combining or opening content. Filter by the intended folder path and file name, and exclude irrelevant or temporary files. Select the expected sheet or table if the real workload uses Excel.

The goal is deterministic input selection: adding an unrelated file to SharePoint must not silently change the dataset.

### Preserve text in the landing layer

Power Query often adds type-conversion steps automatically. Inspect them rather than accepting them without review.

For this lesson, all three source columns should land as text. The value `not provided` must reach the Warehouse so SQL can classify it as an invalid amount. If ingestion converts the column to a number too early, the refresh might fail, or a later error-removal step might discard the record.

Removing the row would make the dataset look cleaner while making the reconciliation less truthful. Bronze is the place to preserve evidence, not conceal quality problems.

Retaining raw text does not mean that everything stays text forever. It means that type conversion is performed deliberately in the next layer, where both the converted value and the quality outcome can be inspected.

### Select explicit destinations and mappings

Use the prepared Warehouse landing tables from Lesson 3, created before the walkthrough:

| Source | Destination | Mapping |
| --- | --- | --- |
| System A | `bronze.system_a` | `RecordId`, `Amount`, `Status` to matching text columns |
| System B | `bronze.system_b` | `Reference`, `Total`, `State` to matching text columns |

A preview in the Power Query editor is not the same as a completed load. Inspect the destination configuration for each output query. Confirm the Warehouse, schema, table, column mapping, and update method.

For these complete snapshots, use the validated **replace** behavior for the existing landing tables. Do not assume a managed-settings option described for another destination applies to Warehouse. Inspect the actual settings available in the target environment.

Publish or save the dataflow using the available tenant experience, run it, and inspect the actual destination data after successful completion. Expected counts are six rows in System A and five in System B.

## 3. Understand full replacement, append, and incremental loading

These terms describe different behaviors and should not be used interchangeably.

**Full replacement** treats the incoming dataset as the current complete state. Each successful load replaces the previous snapshot. Loading the unchanged files again should leave six and five landing rows.

**Append** adds incoming rows to the rows already present. Appending the same complete snapshots twice would produce twelve System A rows and ten System B rows. That is not incremental correctness; it is duplicated input.

**Incremental processing** identifies and handles changes relative to a previously processed state. It needs more than an append switch. It requires a reliable change indicator or change feed, a key, update/delete handling, a durable checkpoint, and a policy for retries and late arrivals.

Consider an amount changing from 200.00 to 250.00. An append-only load now has both values unless another rule determines which is current. If a record is deleted from the source, a change feed containing only inserts will never tell the destination to remove it. If two changes share a timestamp and a watermark advances too early, a record can be missed.

For small complete reconciliation extracts, full replacement is a reasonable teaching choice because it makes the current-state contract clear. It is not a recommendation to reload every enterprise source indefinitely.

### Why two completed loads matter

Replacing each destination independently does not make the pair atomic. System A can finish while System B fails. Running reconciliation at that moment could compare today's System A against yesterday's System B.

The SQL publication step must therefore wait until both sources have completed for the intended snapshot pair. In this lab, that gate can be an explicit supervised check. In production, use a verified control mechanism and durable batch evidence. Do not infer a matched pair merely because both tables contain rows.

## 4. Separate scheduling from orchestration

A schedule answers, "When should this activity start?" Orchestration answers, "What depends on it, and what happens when it succeeds or fails?"

A direct Dataflow Gen2 schedule may be enough to start ingestion. It does not, by itself, prove that downstream SQL ran, that the semantic model observed the new publication, or that a report displays the intended snapshot.

A pipeline can coordinate a dataflow, a SQL activity, and downstream steps using supported activities and success dependencies. Its value is the explicit dependency chain, not merely providing another clock.

```text
Source pair ready
    -> ingestion succeeds for both destinations
    -> source-pair checks pass
    -> reconciliation succeeds
    -> model freshness step succeeds
    -> publication is verified
```

Scheduling SQL fifteen minutes after ingestion is not equivalent to waiting for ingestion success. Runtime can vary, credentials can fail, and a source can be unavailable.

The lesson plan records a previous pipeline-to-Dataflow authentication or permissions issue and an interim direct-scheduling approach. Retest the actual path before delivery. If the pipeline remains blocked, document ingestion as scheduled and the SQL/model steps as supervised. Do not describe that partial automation as a completed end-to-end orchestration.

### Where copy jobs fit

A copy job is worth considering when the primary requirement is supported data movement with limited transformation. Dataflow Gen2 is appropriate here because file selection and Power Query shaping are part of the requirement. A pipeline coordinates activities; a copy job moves supported data; a dataflow shapes and loads data.

The exact source, destination, load mode, and Government availability must be checked before selecting a copy job. Do not replace the working SharePoint/Power Query design based on a product label alone.

## 5. Document the ingestion pattern

Complete the following contract for the actual training environment.

| Contract item | Required answer |
| --- | --- |
| Source scope | Approved site, folder, exact files, and comparison period |
| Readiness | How the source owner identifies a complete, matching snapshot pair |
| Connection | Approved connection owner and execution identity; no credentials in the document |
| Query behavior | File filters, expected columns, and text-preserving type rules |
| Destinations | Warehouse, schemas, tables, and mappings |
| Load strategy | Replace for the complete lab snapshots |
| Rerun expectation | Unchanged inputs leave six and five rows |
| Trigger | Verified direct schedule, pipeline trigger, or explicit manual execution |
| Downstream gate | Both destinations completed for the intended pair |
| Failure behavior | Stop downstream publication and retain the last known-good published result |

### Practice and expected explanation

Run the unchanged load twice if the environment and available time permit. Inspect counts after each run. Explain why the duplicate A005 must still exist in Bronze but why a second refresh must not add another copy of the entire file.

If System B fails, the correct response is not to proceed because System A succeeded. Record the failure, stop downstream publication, and restore a complete matching source pair before continuing.

## Lesson conclusion

Repeatable ingestion is defined by a contract, not by the presence of a refresh button. We now know what data is selected, how it is preserved, what a rerun means, and what must happen before curation begins.

**Previous:** [Lesson 1](01_architecture_decision_framework.md)  
**Next:** [Lesson 3: Curated SQL engineering](03_curated_sql_engineering.md)

**Product reference:** [Dataflow Gen2 destinations and managed settings](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-data-destinations-and-managed-settings). Confirm the applicable destination behavior and scheduling/orchestration paths in the target GCC High tenant.
