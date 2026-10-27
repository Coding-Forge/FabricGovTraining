# Session 3 facilitator guide: Low-code Fabric Data Engineering

**Delivery:** October 28, 2026, 11:00 AM-2:00 PM ET  
**Audience:** Power BI, SQL, and Power Query practitioners  
**Duration:** 180 minutes  
**Status:** Draft teaching material; tenant preflight and supporting lab assets still required  
**Source outline:** [lesson_plan.md](lesson_plan.md)

## Session purpose

Move from the Session 2 demonstration to an explainable, repeatable, supportable reconciliation workload:

`SharePoint files -> Dataflow Gen2 -> Warehouse landing tables -> T-SQL curation -> reconciliation table -> shared semantic model -> Power BI`

Warehouse is the proposed starting point for this workload, not a universal Fabric recommendation. Participants should justify it using their data, transformation needs, and operating skills.

This is not an introductory Fabric tour, a Python class, or a production deployment. Notebooks enter the discussion only when a requirement justifies a different engineering tool. Deeper incremental loading, dimensional modeling, and notebook development belong in follow-up sessions.

### Opening script

> Last time, we showed that this workload could be delivered with familiar Power Query and SQL skills. Today, we will make the decisions and operating steps explicit. By the end, you should be able to explain where each transformation belongs, reconcile two differently structured extracts, and describe how the next refresh can run without duplicating data or publishing incomplete results.
>
> We will distinguish skills we are learning from environment issues we encounter. A connection failure is not evidence that you failed the exercise.

### Evidence and availability boundary

The lesson plan records successful SharePoint ingestion through Dataflow Gen2 and an interim direct-scheduling approach. It also records authentication or permissions problems when pipelines invoked Dataflow Gen2. These are historical observations, not proof of current tenant behavior or a universal GCC High limitation.

General Microsoft Learn documentation describes product behavior; it does not establish availability in the target Government tenant. Validate each live path before delivery. Do not promise commercial-cloud parity, release dates, or resolution of an existing support issue.

## Delivery plan

| Time, ET | Module | Participant evidence |
| --- | --- | --- |
| 11:00-11:25 | 1. Architecture decision framework | Workload-specific Warehouse/Lakehouse decision |
| 11:25-12:00 | 2. Repeatable ingestion | Source-to-destination mapping and refresh contract |
| 12:00-12:50 | 3. Curated SQL engineering | Explained reconciliation results and safe rerun behavior |
| 12:50-1:25 | 4. Consumption architecture | Selected semantic-model and access pattern |
| 1:25-1:50 | 5. Operations and GCC High findings | Ordered runbook, ownership, and separate issue logs |
| 1:50-2:00 | 6. Exit review | Teach-back, artifacts, and named follow-ups |

Module 3 includes a five-minute break. Keep other transitions inside their module allocations.

**Scheduling decision required:** The source outline flags an overlapping commitment from 1:30-2:00 PM. Confirm whether it remains a conflict. Preserve the full agenda until an explicit change is agreed. If Brandon must leave at 1:30, arrange a facilitator handoff for the remainder of Module 5 and the exit review; do not silently omit them.

### Facilitation rules

- Explain the business question before navigating the UI.
- Demonstrate one small step, ask participants to predict its result, then inspect the evidence.
- Use a two-minute troubleshooting limit for an unexpected environment failure. Capture it and switch to a prepared artifact rather than using the class as a support session.
- Label demonstrations, participant-executed steps, and prepared evidence distinctly.
- Do not change production roles, tenant settings, credentials, or schedules to rescue a lab.
- Place out-of-scope questions in the follow-up backlog with an owner.

## Preparation and readiness

### Assets to prepare before delivery

This guide specifies the teaching flow; the following files and tenant artifacts are not supplied by this document.

| Asset | Required preparation |
| --- | --- |
| Synthetic source files | Create the two CSV files defined below in an approved SharePoint location |
| Training workspace | Confirm capacity, permitted artifact creation, connections, and participant access |
| Dataflow Gen2 | Prepare source queries, explicit Warehouse destinations, and a known-good refresh |
| Warehouse | Prepare isolated training tables, normalization views, reconciliation procedure, and result queries |
| Power BI artifacts | Prepare a semantic model, a small reconciliation report, and a consumer test identity |
| Recovery evidence | Capture successful refresh history, expected SQL outputs, and report screenshots using synthetic data |
| Delivery package | Agree an approved location for scripts, guide, and participant outputs independent of recording access |

Use the 30-45 minute readiness gate from the lesson plan. Do not treat these items as completed until the target environment has been checked.

### Preflight record

For each path, record **tested date/time, tenant/workspace, test identity or role, result, evidence location, owner, and fallback**. Never include credentials or access tokens.

| Path | Evidence required | Fallback if blocked |
| --- | --- | --- |
| SharePoint -> Dataflow Gen2 -> Warehouse | Successful refresh and destination row counts | Previously loaded synthetic tables; ingestion becomes a walkthrough |
| Dataflow Gen2 direct schedule | Visible configuration and successful scheduled execution | Manual refresh for the lesson; automation remains unverified |
| Warehouse SQL | Successful view queries and two executions of the training procedure | Prepared SQL and result walkthrough |
| Pipeline -> Dataflow -> SQL | Successful dependency-controlled run using approved connections | Direct ingestion schedule plus explicitly supervised downstream execution |
| Semantic model -> Power BI | Observed storage mode, current data, and consumer access | Prepared report and comparison; do not claim live-path completion |
| Copy job | Relevant connector, destination, and capability available in this tenant | Conceptual comparison only |

Check source-file access as well as workspace access. Test the connections and identities used at execution time, not just the presenter's authoring permissions. Confirm any gateway dependency instead of assuming that a gateway is always or never required.

### Synthetic teaching scenario

**Business question:** Do two system extracts describe the same records and amounts? Which exceptions need investigation before a migration is accepted?

Use fictional record IDs only. The files are complete snapshots of one logical extract batch, not change feeds. Both belong to the same batch and comparison scope.

**System A: `system_a.csv`**

```csv
RecordId,Amount,Status
A001,100.00,Active
A002,200.00,Active
A003,300.00,Active
A005,500.00,Active
A005,500.00,Active
A006,not provided,Active
```

**System B: `system_b.csv`**

```csv
Reference,Total,State
 a001 ,100.00,ACTIVE
A002,250.00,ACTIVE
A004,400.00,ACTIVE
A005,500.00,ACTIVE
A006,600.00,ACTIVE
```

Preserve identifiers and amounts as text in the landing layer. Remove or adjust automatic Power Query type-conversion steps so the intentionally invalid amount reaches the quality checks rather than failing ingestion or disappearing.

### Comparison contract

Establish these rules before showing reconciliation SQL:

- Grain: one output row per normalized record ID for the current snapshot pair.
- Key normalization: trim surrounding whitespace and uppercase identifiers; do not remove significant characters or leading zeros.
- Status normalization: trim and uppercase; these sample statuses are equivalent.
- Amount normalization: convert to a fixed-precision decimal with two decimal places. Failed conversion is invalid data, not zero.
- Duplicate rule: more than one row for a normalized key within either source is an exception. Do not arbitrarily select a winner.
- Classification precedence: duplicate key, invalid amount, source-only record, then comparison of amount and status.
- Missing or blank keys: quarantine and count separately before joining. They cannot safely become a shared business key.
- Publishing rule: report quality exceptions explicitly; do not represent them as matches or silently discard them.

For this small lab, quality exceptions are published as labeled exceptions. A production owner must separately decide which conditions block publication.

| Record ID | Expected classification | Reason |
| --- | --- | --- |
| A001 | MATCH | Whitespace/case normalize; amount and status agree |
| A002 | AMOUNT_MISMATCH | 200.00 versus 250.00 |
| A003 | ONLY_IN_A | No corresponding System B row |
| A004 | ONLY_IN_B | No corresponding System A row |
| A005 | DUPLICATE_KEY | Two System A rows; no arbitrary deduplication |
| A006 | INVALID_AMOUNT | System A amount cannot convert to decimal |

Expected baseline: **6 System A landing rows, 5 System B landing rows, 6 distinct comparison keys, and 6 reconciliation rows**. Each listed classification has one row. There are no blank-key rows in the supplied example.

## Module 1: Architecture decision framework

**Time:** 11:00-11:25, 25 minutes  
**Outcome:** Participants can defend the simplest architecture that meets this workload.

### Teaching notes and flow

**0-5 minutes: Reconnect to Session 2.** Use the opening script. Ask participants to identify the source, business key, comparison, and consumer. Draw the source-to-report path without opening Fabric.

**5-13 minutes: Compare choices.** Use the following distinctions:

| Decision factor | Warehouse starting point | Lakehouse starting point |
| --- | --- | --- |
| Primary engineering work | Relational curation using T-SQL | File/Delta engineering, often using Spark |
| Current workload | Structured extracts and SQL reconciliation | Useful if requirements justify file-oriented or Spark processing |
| SQL write behavior | Warehouse supports supported T-SQL DDL/DML | Lakehouse SQL analytics endpoint queries Delta tables but does not provide T-SQL table-data writes |
| Team fit | Builds on this cohort's SQL skills | Requires an appropriate write/transformation path and operating skills |
| Storage foundation | OneLake and Delta | OneLake and Delta |

A Lakehouse SQL analytics endpoint can expose views and procedures; that does not make it a Warehouse or permit SQL writes to its underlying Delta tables. Conversely, a Warehouse is not a SQL Server instance with every SQL Server feature.

**13-20 minutes: Demo.** Show the prepared Warehouse and its landing/curated objects. If available, show a Lakehouse and its SQL analytics endpoint only long enough to make the distinction concrete. Do not build a second solution.

Explain bronze/silver/gold as responsibilities: source-aligned landing, validated normalization, and consumer-ready results. For this lab they can be schemas inside one training Warehouse. They do not inherently require three workspaces, three capacities, or three physical copies of every object.

**20-25 minutes: Participant decision.** Have pairs complete this short record:

> Workload and consumer: ___. Chosen starting point: ___. Required write/transform operations: ___. Team fit: ___. Rejected alternative and reason: ___. Condition that would make us revisit the decision: ___.

### Discussion prompts

- "What requirement would justify introducing Spark here?"
- "If both choices use OneLake, what are we actually choosing?"
- "Does a SQL endpoint mean every SQL Server operation will work?"

**Checkpoint:** The rationale connects requirements and skills, not "Warehouse is always better."  
**Transition:** "Now that we know where the data belongs, what must ingestion guarantee?"

## Module 2: Repeatable ingestion

**Time:** 11:25-12:00, 35 minutes  
**Outcome:** Participants can describe a repeatable snapshot load and distinguish transformation from orchestration.

### Teaching notes and flow

**0-5 minutes: Assign tool responsibilities.**

| Tool | Role in this lesson |
| --- | --- |
| Dataflow Gen2 | Connect, select the intended files, shape columns, and land data using Power Query |
| Pipeline | Coordinate ordered activities, dependencies, and outcomes when validated |
| Copy job | Consider for supported movement-oriented requirements; not assumed to replace this Power Query transformation |
| Warehouse SQL | Apply reusable relational normalization, quality rules, and reconciliation |
| Notebook | Separate engineering option when requirements exceed the chosen SQL/Power Query pattern |

**5-20 minutes: Demo one controlled load.**

1. Show the approved SharePoint site and the two synthetic files.
2. Inspect folder/file filters. Explain how to exclude unrelated files and prevent an unexpectedly broad folder combine.
3. Show each query's source columns and text-preserving type choices.
4. Inspect the explicit Warehouse destination and its replace/append behavior.
5. Run the prepared dataflow and wait for successful completion.
6. Query destination counts and inspect A005 and A006. A successful refresh must not hide the duplicate or invalid value.
7. Repeat the same snapshot load, using prepared evidence if runtime exceeds the allocation. Counts must remain 6 and 5, not 12 and 10.

For this teaching snapshot, use a validated replace strategy. "Refresh succeeded" is not proof that append/replace settings are correct. Do not claim the two destination tables update atomically; downstream publication must wait until both represent the intended completed batch.

**20-28 minutes: Contrast full and incremental loading.** Full replacement is simple for a small complete extract. An incremental design needs a reliable change indicator, update/delete handling, late-arriving-data rules, and rerun semantics. A folder timestamp or an append setting alone does not establish correct incremental processing.

**28-35 minutes: Participant refresh contract.** Record source scope, snapshot-pair identification, destinations, load mode, expected counts, execution identity, refresh method, and what prevents downstream execution after a partial load.

### Discussion prompts

- "What happens if the same files are loaded twice?"
- "What happens if System A finishes but System B fails?"
- "If the connector works interactively, have we proved scheduled execution works?"

**Checkpoint:** Participants explain why the baseline remains 6/5 and why SQL must not start against a mixed snapshot pair.  
**Fallback:** Use preloaded tables and label ingestion as demonstrated through prepared evidence, not executed by participants.

## Module 3: Curated SQL engineering

**Time:** 12:00-12:50, 50 minutes including a five-minute break  
**Outcome:** Participants explain every exception and distinguish a safe rerun from an append-only reload.

### Teaching notes and flow

**0-7 minutes: Inspect landing data.** Show the 6/5 counts. Ask participants to predict the join result for A005 and the conversion result for A006 before running any curation.

**7-17 minutes: Normalize into Silver views.** Walk through prepared T-SQL that maps both schemas to `record_id`, `amount`, and `status`, retaining raw values for investigation. Explain `TRIM`, `UPPER`, and `TRY_CONVERT(decimal(18,2), ...)` in business terms. An unsuccessful conversion produces a quality flag; it must not become a legitimate zero.

Show duplicate detection grouped by normalized key, separately per source. Separate invalid/duplicate keys from eligible comparison rows before joining. A naive join can multiply duplicates; `DISTINCT`, `MAX`, or selecting an arbitrary row is not a business-approved resolution.

**17-22 minutes: Break.**

**22-35 minutes: Build Gold reconciliation.** Walk through the prepared procedure in this order:

1. Confirm both source loads completed for the intended snapshot pair. A manual lab check is acceptable but must be labeled as manual.
2. Identify blank keys, duplicates, and invalid values without losing their evidence.
3. Produce one quality-exception row per affected nonblank key, following the classification precedence.
4. Use a full outer join of eligible unique keys to retain source-only records.
5. Classify matched rows using explicit amount and status rules. Include a status-mismatch rule even though the baseline has none.
6. Publish the current result only after validation succeeds. For the small Warehouse example, prepare and preflight an explicit transaction around the result-table replacement so a failed write does not leave an empty or partial published result.

Keep the demonstration in an isolated training schema. An atomic Gold replacement does not make upstream dataflows atomic or establish that both extracts belong to the same batch.

**35-42 minutes: Introduce stored procedures.** Explain a procedure as a named, repeatable unit of SQL work. Contrast defining it with executing it. Show its inputs if used, ordered steps, validation, failure behavior, and result queries. Do not turn this into a general stored-procedure syntax lecture.

Execute the procedure twice against unchanged sources. Both runs should produce the six expected results, not append another six. Explain that idempotency means the same intended business state after retry; operational timestamps or run identifiers may differ.

**42-50 minutes: Participant prediction and inspection.** Let participants explain one row each. If time permits, change System B A002 to 200.00 in the synthetic file, reload, and rerun. Predict **2 MATCH and 0 AMOUNT_MISMATCH**, with the other four classifications unchanged; total output remains six. Restore the baseline through the same ingestion path before later demonstrations, or explicitly label the changed state.

### Discussion prompts

- "Why is A005 not a match even though its amounts agree?"
- "Why is an invalid amount not zero?"
- "Would an inner join answer the business question?"
- "Which checks protect business correctness, and which only prove SQL execution succeeded?"

**Checkpoint:** Six output rows agree with the comparison contract; participants can explain duplicate handling, source-only records, and reruns.  
**Fallback:** Walk through prepared SQL and labeled baseline results. Do not report an unexecuted rerun or failure-recovery path as proven.

## Module 4: Consumption architecture

**Time:** 12:50-1:25, 35 minutes  
**Outcome:** Participants choose a consumption path and identify where shared definitions and access controls live.

### Teaching notes and flow

**0-8 minutes: Separate the decisions.** A shared semantic model provides reusable measures, relationships, and governance. Direct Lake, Import, and DirectQuery describe storage/query behavior; they are not alternatives to having a semantic model. Direct SQL is a separate consumption route for SQL-capable clients.

| Route | Teaching point | Verify before demonstrating |
| --- | --- | --- |
| Shared semantic model using Direct Lake | Reuse business definitions over supported curated tables | Available variant, supported objects, identity behavior, freshness/framing, and any fallback behavior |
| Shared semantic model using Import | Reusable model with a separately refreshed imported copy | Model refresh dependencies and data freshness |
| Shared semantic model using DirectQuery | Queries the source through the configured connection | Source performance and access behavior |
| Direct SQL | Useful for approved SQL analysis/integration | Object permissions, consumer identity, and consistent use of curated definitions |

Do not assume a SQL view is a Direct Lake table source. Use the prepared physical Gold reconciliation table for the proposed Direct Lake demonstration and validate the exact model path. If an alternative mode is used, name it explicitly.

**8-23 minutes: Demo the prepared model and report.**

1. Inspect the curated table and show the semantic model's actual storage mode.
2. Show a total-record measure, exception count, classification breakdown, and record-level exception detail.
3. Define an exception as any classification other than `MATCH`. The baseline is 6 total records, 1 match, and 5 exceptions.
4. Trace A002 from report to Gold result and back to the two source amounts.
5. Explain dataflow completion, SQL publication, model freshness, and report visibility as separate checkpoints. Direct Lake does not mean "no freshness management."
6. Use the preflighted consumer identity to show the intended access path. Do not infer consumer access from the presenter's workspace role.

**23-30 minutes: Participant design choice.** Ask each pair to select a primary route, name its owner, identify where measures are maintained, and explain how it avoids conflicting report-specific reconciliation definitions.

**30-35 minutes: Review tradeoffs.** Distinguish permissions on the workspace, data item, SQL objects, semantic model, and report. Do not claim that semantic-model row-level security automatically protects direct SQL access or every OneLake access route.

### Discussion prompts

- "If three reports calculate exceptions differently, where should the definition move?"
- "What changes if a consumer bypasses the semantic model and queries SQL?"
- "How would you prove that the report contains the newly published snapshot?"

**Checkpoint:** Participants name both the reuse strategy and the actual storage/query mode.  
**Fallback:** Show prepared model/report evidence, explain the unvalidated live dependency, and retain it as an open item.

## Module 5: Operations and GCC High findings

**Time:** 1:25-1:50, 25 minutes  
**Outcome:** Participants can order the run, identify failure boundaries, and route issues without confusing them with learning needs.

### Teaching notes and flow

**0-8 minutes: Build the operational sequence.**

1. Confirm the intended source pair is ready and belongs to the same comparison scope.
2. Refresh ingestion and inspect completion for both destinations.
3. Verify batch alignment, row counts, and source-quality evidence.
4. Execute SQL curation/reconciliation and validate the published result.
5. Perform the model refresh/framing or other freshness step required by the chosen mode.
6. Confirm report visibility and expected business totals.
7. Record outcome, run evidence, and any exception requiring an owner.

A schedule triggers work; orchestration coordinates dependencies. Separate schedules with estimated time gaps do not prove upstream completion. If pipeline invocation remains blocked, direct Dataflow scheduling covers ingestion only. Present downstream SQL/model execution as supervised steps until a validated dependency mechanism exists.

**8-15 minutes: Demo monitoring and a failure boundary.** Inspect a prepared successful refresh and its counts, a SQL execution result, and model/report freshness evidence. Use a prepared failure example or a controlled training-only test to ask what must stop when System B fails. Do not deliberately break shared connections or introduce a live tenant incident.

Record start/end time, source snapshot identity, object names, expected/actual counts, status, last successful publication, error evidence, and responsible owner. Protect existing published output when a new run fails.

**15-20 minutes: Assign ownership and lifecycle.** Identify the source owner, connection owner, transformation owner, semantic-model owner, and support contact. Use existing approved workspace/naming conventions; the bronze/silver/gold schema names are teaching examples, not a new tenant standard.

Ask who updates connection credentials, approves business-rule changes, reviews access, promotes artifacts, and authorizes cleanup of training assets. Do not introduce a deployment tool or lifecycle feature that has not been validated in this environment.

**20-25 minutes: Separate the logs.**

| Log | Example | Minimum useful entry |
| --- | --- | --- |
| Learning | Participant cannot yet explain procedure execution versus definition | Skill, exercise evidence, next practice, owner |
| Environment finding | An approved pipeline connection cannot invoke the dataflow | Timestamp, scope, execution role, steps, expected/actual behavior, sanitized error/run ID, impact, owner, next action |

Classify an environment issue as observed, under investigation, or confirmed with supporting evidence. Authentication failure alone does not establish a product defect or a Government-wide unsupported feature. Record any approved workaround and its manual effort, dependency gaps, and expiry/review condition.

### Discussion prompts

- "At which exact point is this run safe to publish?"
- "If ingestion is scheduled but SQL is manual, what has actually been automated?"
- "Who responds tomorrow if this fails, and what evidence do they need?"

**Checkpoint:** The operating sequence has explicit success gates and owners; an unresolved pipeline issue is not presented as resolved.

## Module 6: Exit review

**Time:** 1:50-2:00, 10 minutes  
**Outcome:** Participants demonstrate understanding and leave with owned next steps.

**0-5 minutes: Teach-back.** Ask participants, not the presenter, to explain:

1. Why Warehouse was selected and what could change that decision.
2. Why an unchanged reload and SQL rerun do not duplicate the published results.
3. How A005 and A006 are handled without hiding source problems.
4. What separates an ingestion schedule from an end-to-end controlled refresh.
5. Which consumption route was used and how consumer access/freshness were verified.

**5-8 minutes: Inspect the evidence.**

| Exit artifact | Completion evidence |
| --- | --- |
| Architecture decision | Workload, selected option, rejected alternative, revisit condition |
| Ingestion contract | Sources, destinations, snapshot pair, load mode, identity, counts |
| Curated result | Explained baseline classifications and observed rerun result |
| Consumption decision | Semantic-model strategy, actual mode, access and freshness checks |
| Operating checklist | Ordered gates, failure handling, and named owners |
| Two logs | Learning needs separated from environment findings |

Mark each as **participant completed**, **presenter demonstrated**, **prepared evidence reviewed**, or **blocked**. Attendance or a screenshot alone is not evidence that a participant can repeat the workload.

**8-10 minutes: Close.** Assign owners and next actions for unresolved items. Capture interest in SQL/Warehouse follow-up versus the separate notebook/Spark track without teaching either now.

### Closing script

> The goal was not to add every Fabric component. It was to make one workload understandable and repeatable with tools this team can support. We now have a decision trail, explicit comparison rules, and a way to distinguish a data exception, a learning need, and an environment issue. The remaining work is recorded with owners rather than hidden inside the demonstration.

## Facilitator reference

The following general product documentation was consulted while drafting. It does not verify tenant-specific GCC High availability:

- [Fabric Data Warehouse and the Lakehouse SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)
- [Dataflow Gen2 overview and comparison with Gen1](https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-overview)
- [Transactions in Fabric Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/transactions)

Use the [source lesson plan](lesson_plan.md) for engagement history and prior observations. Before delivery, confirm current Government capability guidance and run the target-tenant preflight; unresolved capability checks remain open, not assumed.
