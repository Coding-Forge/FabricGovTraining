# Lesson 5: Operations and GCC High findings

**Session 3 | October 28, 2026 | 25 minutes**  
**Blueprint:** [Module 5](../../session_3_blueprint.md#module-5-operations-and-gcc-high-findings---25-minutes)  
**Lesson output:** An initial operations checklist and findings register.

## What this lesson teaches

A solution is operational when someone other than its original author can determine whether it ran correctly, understand what failed, and take the next approved action. Scheduling is part of that story, but ownership, monitoring, access, and lifecycle are equally important.

This lesson turns the reconciliation flow into an operating agreement. We will also distinguish a skill gap from a data problem or an environment finding. That distinction protects both the learner and the accuracy of the technical record.

Use seven minutes for scheduling and monitoring, five for access and ownership, five for naming and lifecycle, five for findings, and three to complete the operating checklist.

## 1. Schedule the process, not just an activity

The process is a chain of dependent states:

```text
Ready source pair
    -> completed ingestion
    -> validated source pair
    -> completed SQL publication
    -> current semantic model
    -> verified consumer result
```

Each arrow represents a condition that must be met, not merely a delay between clock times.

If ingestion runs at 6:00 AM and SQL runs at 6:15 AM, that schedule assumes ingestion always completes within fifteen minutes. It does not detect an authentication failure, an unusually large file, or the absence of one source. A controlled flow uses success dependencies and data checks wherever the approved tooling supports them.

The engagement previously used direct Dataflow scheduling while pipeline invocation had an authentication or permissions issue. That can be a useful interim ingestion approach. It does not establish that the whole reconciliation process is automated.

If downstream steps remain supervised, write that plainly:

> Ingestion is scheduled. The operator confirms both snapshots and then executes reconciliation and the required model freshness step. End-to-end unattended orchestration remains open.

This statement is more useful than an optimistic diagram because it exposes the actual operating dependency.

## 2. Monitor technical success and business correctness

A green activity status answers a narrow question: the service completed the configured activity without reporting a failure. It does not prove that the correct files were selected, that the comparison period matches, or that the resulting exceptions make sense.

For our baseline, ingestion should produce six System A rows and five System B rows. Gold should contain six keys, one match, and five exceptions. These are expected values for this synthetic example, not permanent thresholds for a changing business source.

A production monitor should distinguish expected volume variation from suspicious changes. A sudden zero-row extract may be legitimate, but it must not be treated as legitimate simply because the query succeeded.

Use three kinds of evidence:

| Evidence | What it establishes | What it does not establish alone |
| --- | --- | --- |
| Activity status and refresh history | Configured work completed or reported an error | Correct source scope or business results |
| Counts and quality checks | Volume, key uniqueness, and exception conditions | Correct permissions or intended comparison period |
| Batch/source evidence and consumer checks | Intended source pair reached the intended audience | Every other control is functioning |

Record a run identifier, source snapshot identifiers or approved source evidence, start/end times, relevant object names, expected/actual counts, outcome, and evidence links. A run record should identify the last successful published comparison as well as the failed attempt.

Do not put passwords, tokens, connection secrets, or sensitive source contents in logs. Error messages and screenshots may need sanitization before they are shared.

### Respond at the correct failure boundary

If System B fails to load, stop before reconciliation. Repair or rerun the approved ingestion path, then confirm both inputs belong to the same intended comparison.

If SQL fails before commit, retain the prior committed Gold result and investigate. The example procedure rolls back its Gold replacement on failure, but that protection does not repair partially refreshed Bronze tables.

If Gold succeeds but the model freshness step fails, the SQL publication and report may describe different states. Record the distinction. Do not rerun all ingestion automatically when the failure is only in model refresh.

If the report loads but totals are unexpected, investigate the business rule, model filters, source scope, and publication metadata before declaring a platform incident.

Retries are safe only when the stage's behavior is understood. Full replacement and an idempotent SQL publication help, but they do not remove the need to verify batch alignment and prevent conflicting concurrent runs.

## 3. Define workspace roles and artifact ownership

Workspace roles govern collaboration over workspace contents. Artifact-specific permissions govern particular items or access paths. They overlap, but they are not interchangeable.

At a high level, workspace Administrators manage the workspace and access, Members have broad collaboration capabilities, Contributors create and modify content, and Viewers consume content. Exact permissions depend on the item and current service behavior; use the approved tenant access design rather than assigning elevated roles to everyone in a lab.

A report consumer generally should not receive workspace write permissions merely to read a report. A report author using a shared model may need model Build permission without becoming an owner of the upstream Warehouse. A connection owner has responsibilities that differ from the author of the SQL procedure.

Power BI row-level security also requires care: users with elevated workspace editing roles are not an appropriate stand-in for testing a restricted consumer. Model-level rules do not automatically govern separate SQL or OneLake access routes.

Assign owners by responsibility:

| Responsibility | Operating question |
| --- | --- |
| Source owner | Who confirms that the intended extracts are complete and comparable? |
| Connection owner | Who maintains the approved authentication and any required gateway dependencies? |
| Ingestion owner | Who supports file selection, mapping, and refresh behavior? |
| SQL/data owner | Who maintains comparison rules and approves quality/publication policy? |
| Model/report owner | Who maintains shared measures, freshness behavior, and consumer access? |
| Support coordinator | Who triages failures and escalates unresolved environment findings? |

One person may hold multiple responsibilities. The important point is that the responsibilities are explicit and have backup coverage. "The person who built it" is not a durable support model.

## 4. Use naming and lifecycle to make the flow understandable

Names should communicate purpose without depending on tribal knowledge. `bronze.system_a`, `silver.normalized_records`, and `gold.reconciliation` make the teaching layers visible. `gold.usp_refresh_reconciliation` makes the procedure's intended action visible.

These are examples, not a new naming standard for the tenant. Use existing approved workspace and artifact conventions when implementing the real workload.

Names alone do not provide isolation. A table called `test_reconciliation` is not protected from production consumers simply because its name contains "test." Establish the appropriate environment, access, and publication boundaries.

Lifecycle means controlling how a change moves from authoring to use. A business-rule change should be reviewed, exercised against known examples, approved by its owner, and accompanied by an understood rollback or recovery path.

For example, suppose the business changes the exception policy so invalid amounts block publication. That is not a harmless visual adjustment. It changes procedure behavior, operating alerts, and the report's freshness during a failed run. The SQL, model documentation, and runbook must remain consistent.

Use version-controlled definitions and the approved promotion mechanism where available. Do not assume a particular Git integration or deployment feature works in Government merely because a commercial demonstration uses it.

Before deleting training artifacts, identify shared dependencies and obtain owner approval. A connection, Warehouse, or model created during a workshop may already be referenced elsewhere.

## 5. Separate learning needs from environment findings

Not every difficulty is a product issue, and not every product issue is a learning failure.

A **learning need** concerns a concept or skill: a participant cannot yet explain an outer join, distinguish procedure creation from execution, or identify why append duplicates a snapshot.

A **data issue** concerns the supplied data: a duplicate business key, an invalid amount, or a missing source extract. An expected quality exception is not necessarily a defect in the platform.

An **environment finding** concerns a reproducible capability, connection, permission, network, gateway, or service behavior in the specific environment.

Maintain a learning log separately from environment findings. Track data exceptions through the reconciliation/data-quality process rather than calling them Government limitations.

### Learning-log example

> **Skill:** Interpreting duplicate keys before a join.  
> **Evidence:** Participant expected A005 to be a match despite two System A rows.  
> **Next practice:** Explain how a two-to-one join changes row count.  
> **Owner:** Named participant and supporting technical lead.

### Environment-finding template

| Field | What to record |
| --- | --- |
| Observation | Narrow description of what failed |
| Scope | Tenant/workspace, relevant item type, connection, and tested execution role |
| Time and evidence | Timestamp, sanitized run/error identifier, approved evidence location |
| Reproduction | Minimal steps, expected behavior, and actual behavior |
| Impact | Which lesson or operating stage is blocked |
| Investigation status | Observed, under investigation, or confirmed with supporting evidence |
| Owner and next action | Named technical/support owner and next diagnostic or escalation |
| Interim approach | Approved alternative, manual effort, dependency gaps, and review condition |

For the prior pipeline/Dataflow issue, do not write "GCC High does not support this" based solely on an authentication error. That error may reflect permissions, connection context, a service defect, or a capability boundary. Record the observed failure and investigation status until the cause is established.

General documentation, prior success in another tenant, and a successful run under a different identity are useful clues. None alone proves the path works for this workload's scheduled execution.

## 6. Complete the initial operations checklist

Write the actual answers rather than checking boxes without evidence.

| Gate | Required operating answer |
| --- | --- |
| Source readiness | How the matching, complete extract pair is identified |
| Ingestion completion | Where refresh status and destination counts are checked |
| Comparison readiness | Who or what prevents mixed snapshots and overlapping runs |
| SQL publication | How the procedure is invoked, validated, and recovered on failure |
| Model freshness | Which mode-specific step or behavior is verified |
| Consumer verification | Which publication and expected business totals are visible |
| Access and ownership | Who supports each stage and approves changes |
| Findings | Where learning needs, data exceptions, and environment issues are routed |

### Practice: reason through an incomplete run

System A loads successfully, System B fails, and the previous day's report remains accessible. Explain the correct operating response.

The answer should stop the new comparison, retain and label the last successful publication, record the failed ingestion, and assign the next action. The accessible report is not evidence that today's run succeeded. After correction, verify a complete matching source pair before resuming.

## Lesson conclusion

We can now describe not only how the solution works, but how it is operated when something goes wrong. The final lesson checks that the decisions, artifacts, evidence, and follow-ups are complete enough to hand to another practitioner.

**Previous:** [Lesson 4](04_consumption_architecture.md)  
**Next:** [Lesson 6: Exit review](06_exit_review.md)

**Environment boundary:** All automation and access paths require target-tenant validation. Do not present a documented interim approach as a verified production control.
