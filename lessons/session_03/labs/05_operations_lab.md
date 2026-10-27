# Lab 5: Operations and GCC High findings

**Session 3 | October 28, 2026 | 15 minutes**  
**Lesson output:** An ordered operating checklist, a scoped environment finding, and a separate learning action.

## Before you begin

Use the [setup runbook](README.md) and your actual evidence from Labs 2-4. This lab combines monitoring inspection with a tabletop failure scenario. Do not break a shared connection, remove a real permission, or disrupt production to demonstrate failure.

## Task 1: Inspect one known run

1. Open the completed Dataflow refresh history and identify the intended source pair.
2. Record successful destination counts and the source-completion gate.
3. Inspect the SQL check result, batch label, and publication time.
4. Inspect model/report freshness evidence using the actual mode.
5. Identify the last successful publication and where an operator finds it after a later failure.

**Checkpoint:** Technical activity status, business checks, and consumer evidence are three different kinds of proof. If only prepared evidence is available, label it.

## Task 2: Write the ordered runbook

For each gate, write an executable instruction or a specific supervised check, not just a check mark.

| Order | Gate | Actual instruction/evidence | Owner and failure response |
| --- | --- | --- | --- |
| 1 | Source pair ready | Complete | Complete |
| 2 | Both ingestion outputs successful | Complete | Complete |
| 3 | Source alignment, counts, and quality checked | Complete | Complete |
| 4 | SQL publication and result checks pass | Complete | Complete |
| 5 | Model's freshness requirement met | Complete | Complete |
| 6 | Intended consumer sees expected publication | Complete | Complete |
| 7 | Run outcome and findings recorded | Complete | Complete |

If a pipeline was verified, record the actual activities and success dependencies. If not, name the person supervising SQL/model steps. Separate schedules with estimated time gaps are not successful dependency orchestration.

## Task 3: Respond to a failed source

Use this scenario:

> System A finished today. System B failed. Yesterday's report still opens and looks reasonable.

1. State which work must stop and what published result remains valid.
2. State what users should be told about freshness.
3. Identify evidence required before retrying.
4. Explain why a SQL transaction protecting Gold does not repair partially refreshed Bronze tables.
5. Explain how the response differs if Gold succeeded but only model refresh failed.

**Expected response:** Do not compare mismatched snapshots. Preserve and identify the last successful Gold/report state, record the failure and owner, and resume only after a matching complete pair is verified. If only the model stage failed, investigate/retry that stage rather than automatically reloading everything.

## Task 4: Separate three issue types

Classify these observations:

1. A participant cannot explain why a duplicate key is an exception.
2. A source contains A006's `not provided` amount.
3. A pipeline invocation using the approved connection returns an authentication error.

Expected categories: learning need, source-data exception, environment finding. The third observation does not establish a Government-wide unsupported capability.

Record one learning action:

| Skill | Evidence | Focused next practice | Owner |
| --- | --- | --- | --- |
| Complete | Complete | Complete | Agree |

Record an environment finding, using a real observed failure or clearly labeling the tabletop case as **simulated**:

| Field | Your entry |
| --- | --- |
| Observation and investigation status | Complete |
| Tenant/workspace/item scope and tested role | Complete; no secrets |
| Timestamp and sanitized run/error evidence | Complete or mark simulated |
| Reproduction, expected behavior, actual behavior | Complete |
| Blocked stage and operating impact | Complete |
| Owner and next diagnostic/support action | Agree |
| Approved interim approach, manual effort, and review condition | Complete |

## Task 5: Assign support and change responsibilities

1. Name the source, connection, ingestion, SQL/data, model/report, and support owners, with backup coverage.
2. Confirm the minimum appropriate workspace/artifact permissions instead of assigning broad edit roles to readers.
3. Apply existing naming conventions. Explain why `test` in a name does not provide isolation.
4. Describe review, known-result checks, promotion approval, and recovery if the business changes invalid amounts from exceptions to publication blockers.
5. Record owner-approved schedule retention and artifact cleanup. Do not delete shared items as a lab exercise.

**Completion check:** A second operator can follow your gate sequence, identify the failure boundary, and find an accountable owner without the original presenter.

**Submit:** Runbook, evidence, separate issue records, and agreed owners.

**Previous:** [Lab 4](04_consumption_lab.md)  
**Next:** [Lab 6: Exit review](06_exit_review_lab.md)
