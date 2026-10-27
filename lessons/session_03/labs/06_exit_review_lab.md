# Lab 6: Exit review and handoff

**Session 3 | October 28, 2026 | 10 minutes**  
**Lesson output:** An evidence-based completion record, accepted follow-up actions, and participant track alignment.

## Before you begin

Bring the outputs from Labs 1-5 and the [setup/reset runbook](README.md). This is a review and teach-back, not another implementation exercise.

## Task 1: Verify the handoff package

1. Exchange evidence with another pair or the facilitator.
2. For each output below, record one state: **participant completed**, **presenter demonstrated**, **prepared evidence reviewed**, or **blocked**.
3. Identify any missing prerequisite or hidden step that would prevent someone else from repeating the work.

| Output | State | Evidence location | Remaining gap |
| --- | --- | --- | --- |
| Architecture record and tool choices | Complete | Complete | Complete |
| Ingestion contract and observed rerun | Complete | Complete | Complete |
| SQL baseline/correction/rerun/guard checks | Complete | Complete | Complete |
| Model, measures, report, and actual mode | Complete | Complete | Complete |
| Consumer access and freshness | Complete | Complete | Complete |
| Operating checklist and separate logs | Complete | Complete | Complete |

Do not upgrade a reviewed screenshot to participant completion or a manual step to verified unattended automation.

## Task 2: Teach back the design

Without reading SQL aloud, explain:

1. Why Warehouse fits the baseline and what would justify a Lakehouse/notebook component.
2. Why landing text and raw values matter.
3. Why A005 is not a match and A006 is not zero.
4. Why reloading and rerunning unchanged input must not duplicate the intended state.
5. Why scheduled ingestion alone does not prove complete orchestration.
6. How the consumer can establish the publication's identity and freshness.

**Acceptance check:** The listener can trace source -> landing -> quality -> Gold -> model -> report and identify the gates, not just name the components.

## Task 3: Convert gaps into actions

Choose the most important unresolved items and agree:

| Item and current state | Accepted owner | Next action | Completion evidence | Agreed review point |
| --- | --- | --- | --- | --- |
| Complete | Agree | Complete | Complete | Agree |
| Complete | Agree | Complete | Complete | Agree |

Use specific actions such as "Retest pipeline invocation with the intended connection and capture a sanitized run result," rather than "Fix pipelines." Do not invent ownership or dates without agreement.

Expected source-data exceptions are not automatically implementation defects. Keep them with the source/data owner.

## Task 4: Select the next learning track

Record each participant's intended responsibility, preferred primary track, and one skill to develop. Confirm with the participant and technical lead.

| Responsibility | Primary track | Next skill |
| --- | --- | --- |
| Complete | SQL/Warehouse or notebook/Spark | Complete |

SQL/Warehouse emphasizes relational modeling, procedures, loads, and quality/operations. Notebook/Spark emphasizes Python/PySpark, Delta processing, parameters, and engineering orchestration. Neither is a maturity ranking, and today does not require everyone to learn Python.

## Final completion check

The package is ready for a learning handoff when another practitioner can find the source files, follow the approved setup sequence, reproduce the expected results, and identify the next action when a stage is blocked.

Tenant checks still pending must remain visible. Completion of the learning exercises is not production approval.

**Submit:** Accepted completion record, evidence locations, actions, and track choices. Use the setup runbook for baseline restoration and approved cleanup.

**Previous:** [Lab 5](05_operations_lab.md)
