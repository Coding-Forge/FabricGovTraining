# Lab 1: Architecture decision framework

**Session 3 | October 28, 2026 | 8 minutes**  
**Lesson output:** An architecture decision record, layer responsibilities, and a justified tool selection.

## Before you begin

Read the [setup and safety runbook](README.md). This is a paired design exercise; no service access is required. Refer to Lesson 1 for the teaching narrative.

Use the packaged synthetic files in `artifacts/data/baseline/`. System A has six rows, System B has five, and the combined sources contain six distinct normalized business keys.

## Task 1: State the business question and grain

1. Open both CSVs in a text editor so spaces and duplicate rows remain visible.
2. Write the question the business needs answered without naming a Fabric product.
3. Define what one published row represents.
4. Identify which rows might create a misleading result if you joined the files without preparation.

**Checkpoint:** Your question compares records, amounts, and statuses. Your grain is one normalized record ID per comparison of the two complete snapshots. A005 is a duplicate-source ambiguity, not permission to publish extra business records.

## Task 2: Choose the storage and transformation path

1. List the required operations: ingest the intended files, preserve evidence, normalize representations, evaluate quality, reconcile, and publish.
2. Compare a Warehouse/T-SQL path with a Lakehouse/notebook path.
3. Choose a starting point and explain how the team will support it.
4. Assign each layer a responsibility. Explain whether a view or a physical table is appropriate.
5. Identify why the Lakehouse SQL analytics endpoint is not a substitute for Warehouse T-SQL data writes.

Record the decision:

| Field | Your answer |
| --- | --- |
| Business question and grain | Complete |
| Chosen starting point and required write operations | Complete |
| SQL/Power Query versus Spark skill fit | Complete |
| Bronze responsibility and evidence | Complete |
| Silver responsibility and object type | Complete |
| Gold responsibility and publication object | Complete |
| Rejected alternative and rationale | Complete |
| Assumptions requiring tenant validation | Complete |
| Revisit condition | Complete |

**Expected reasoning:** Warehouse is a justified starting point for the relational, SQL-owned baseline. Both options use OneLake. Bronze preserves evidence; Silver normalizes and checks quality; Gold publishes business results. Three layers do not inherently require three workspaces.

## Task 3: Match tools to work

Assign a responsibility or a reason not to use each tool:

| Tool | Your decision |
| --- | --- |
| Dataflow Gen2 | Complete |
| Pipeline | Complete |
| Copy job | Complete |
| Warehouse T-SQL | Complete |
| Notebook | Complete |

**Checkpoint:** Dataflow shapes/loads; a pipeline coordinates dependencies; a copy job is considered for supported movement-oriented work; SQL performs relational curation. Notebooks require a justified capability need, not a desire to use every product.

## Task 4: Revisit one assumption

The source now includes documents requiring custom Python extraction.

1. Identify the new operation.
2. State which part of the design might change and which parts can remain.
3. Name the capability and ownership assumptions you would verify before selecting a notebook/Lakehouse path.

**Completion check:** Another pair can understand your selected option, rejected alternative, and revisit condition without asking what you meant.

**Submit:** The completed decision and tool tables with your completion state. No environment cleanup is needed.

**Next:** [Lab 2: Repeatable ingestion](02_ingestion_lab.md)
