# Session 03 customer delivery guide

**Session:** Low-code Fabric Data Engineering  
**Delivery:** October 28, 2026, 11:00 AM-2:00 PM ET  
**Lead:** Brandon Campbell  
**Audience:** SQL, Power Query, and Power BI practitioners  
**Use:** Presenter run of show; not another participant lesson  
**Readiness:** Planned delivery. Live tenant paths and customer access still require preflight.

## 1. The delivery approach

Deliver **one reconciliation story**, not three separate presentations of the same material.

Use the **presentation** to establish the question and explain a decision. Switch to the **live environment** to demonstrate a small, preflighted step. Hand participants to the matching **lab** to apply that idea and capture evidence. Return to the deck for a brief debrief and the next decision. Use the **lessons/teaching handbook** as the explanatory reference, not as a second script to read aloud.

The recurring pattern is:

> Explain the purpose -> demonstrate the smallest useful step -> participants apply it -> inspect evidence -> transition.

Keep the same business question visible: **Do two complete extracts agree, and which exceptions need investigation?** Carry A002, A005, and A006 through ingestion, SQL, reporting, and operations so participants do not have to learn a new scenario in every module.

This guide coordinates the existing 54-slide deck, six lessons, and six labs. The 96 minutes of practice are **inside** the three-hour agenda. A five-minute break is also included; it does not extend the session.

## 2. Resource map and what to share

All paths are relative to `lessons/session_03/`. Page numbers below are the current physical PDF pages, including covers. Use section titles if a rebuilt PDF changes pagination.

| Resource | Presenter use | Participant use |
| --- | --- | --- |
| [PowerPoint](presentation/session_03_low_code_fabric_data_engineering.pptx) | Main delivery spine; speaker notes contain deeper teaching context | Share a copy through the approved channel |
| [Teaching handbook](pdf/session_03_teaching_handbook.pdf) | Prepare explanations and answer deeper questions | Read alongside or after delivery; do not require live reading of every page |
| [Lab workbook](pdf/session_03_lab_workbook.pdf) | Point to tasks and completion checks | Primary live exercise document |
| [Setup/reset runbook](labs/README.md) | Environment preflight, script order, reset, safety, and fallbacks | Consult when preparing or repeating the workload |
| `artifacts/data/` | Baseline, corrected input, and expected outputs | Use the named files when directed |
| `artifacts/sql/` | Prepared definitions, execution, result checks, retry/guard tests | Run only the assigned file against the isolated Warehouse |
| `artifacts/dax/reconciliation_measures.dax` | Demonstrate one measure at a time | Create measures separately, not as a bulk DAX query |
| [This delivery guide](delivery_guide.md) | Timing, handoffs, transitions, and recovery decisions | Not required for participating |

File names for staging or using this guide offline:

```text
presentation/session_03_low_code_fabric_data_engineering.pptx
pdf/session_03_teaching_handbook.pdf
pdf/session_03_lab_workbook.pdf
pdf/session_03_delivery_guide.pdf
labs/README.md
labs/01_architecture_lab.md through 06_exit_review_lab.md
artifacts/data/
artifacts/sql/
artifacts/dax/reconciliation_measures.dax
```

The Markdown guide links directly to these resources. The printable guide uses the file names above; its contents navigation is internal to the guide.

### Material crosswalk

| Module | Slides | Lesson / handbook starts | Lab / workbook starts | Required output |
| --- | --- | --- | --- | --- |
| Architecture | 1-10, including opening | [Lesson 1](01_architecture_decision_framework.md), p. 3 | [Lab 1](labs/01_architecture_lab.md), p. 9 | Architecture decision record |
| Ingestion | 11-19 | [Lesson 2](02_repeatable_ingestion.md), p. 9 | [Lab 2](labs/02_ingestion_lab.md), p. 12 | Ingestion and refresh contract |
| SQL engineering | 20-30 | [Lesson 3](03_curated_sql_engineering.md), p. 15 | [Lab 3](labs/03_sql_engineering_lab.md), p. 15 | Explained results and execution evidence |
| Consumption | 31-39 | [Lesson 4](04_consumption_architecture.md), p. 25 | [Lab 4](labs/04_consumption_lab.md), p. 18 | Consumption/access/freshness decision |
| Operations | 40-47 | [Lesson 5](05_operations_and_gcc_high_findings.md), p. 31 | [Lab 5](labs/05_operations_lab.md), p. 21 | Operating checklist and separate issue records |
| Exit review | 48-53 | [Lesson 6](06_exit_review.md), p. 37 | [Lab 6](labs/06_exit_review_lab.md), p. 24 | Completion record and accepted actions |

Slide 54 is the source/reference slide. Keep it available for questions or the handoff; it is not an extra timed module.

### Customer distribution

Before delivery, place the deck, both participant PDFs, and the source lab files in an **approved customer-accessible location**. Retain the `labs/` and `artifacts/` directory structure so links and file names make sense. Confirm access using a customer participant identity, not only the presenter's account.

Share a short start message with the actual approved links, assigned workspace/Warehouse/source folder, and evidence-submission location. Do not send placeholder URLs or credentials. Do not depend on access to a meeting recording.

Suggested message:

> Open the lab workbook and keep the teaching handbook available as a reference. We will work through one source-to-report reconciliation in six connected steps. Use only your assigned training environment. Save the requested evidence in the agreed location; record any blocked step rather than working around permissions.

## 3. Roles, preflight, and delivery decision

### Assign roles before the session

| Role | Responsibility during delivery |
| --- | --- |
| Lead presenter | Teach, control screen changes, explain decisions, and hold timeboxes |
| Lab/customer technical lead | Triage participant issues and confirm assigned environments/source readiness |
| Producer or timekeeper | Post links, give time warnings, capture questions, and collect evidence states |
| Support/findings owner | Own scoped environment findings and agreed escalation actions |
| Backup presenter, if needed | Take the named remaining modules with the current state and evidence location |

One person may hold multiple roles, but agree ownership before joining. If presenting alone, use paired learners, avoid individual breakouts, and park troubleshooting that would stop the full class.

**Calendar check:** The original lesson plan recorded a possible 1:30-2:00 PM overlap. Confirm whether it still applies. Resolve it or arrange an explicit backup for Lab 5, its debrief, and Module 6. If the lead leaves at 1:30, the backup must take over at the **start** of Lab 5 and own the full 1:30-2:00 block. Do not discover this during the workshop.

### Before the delivery day

1. Complete the full readiness gate in the setup runbook using the intended tenant, connections, and identities.
2. Rehearse the entire path on the presenter Warehouse: baseline ingestion -> SQL checks -> unchanged rerun -> correction -> baseline restoration -> guard rejection -> model/report verification.
3. Measure refresh runtimes, including the correction and reset. If they cannot fit their lab windows, plan the slower steps as a preflighted presenter demonstration or prepared-evidence walkthrough; do not promise every learner will execute them live.
4. Prepare separate learner/pair Warehouses and source folders. The scripts have fixed object names; do not let pairs write to one shared Warehouse.
5. Agree which definitions and model/report artifacts are precreated. For the three-hour delivery, default to prepared tables/views/procedure and a prepared model/report scaffold. Participants inspect definitions, execute checks, create or inspect measures, and complete decisions. Do not represent inspection of prepared objects as independent creation.
6. Capture recovery evidence using synthetic data: successful refresh/counts, baseline result, corrected result, guard/rerun checks, model mode, and the intended consumer result. These captures must be produced in preflight; they are not supplied merely because expected-result CSVs exist.
7. Agree the customer artifact owners, participant list, source comparison scope, and evidence-retention location.

### 30-45 minutes before start

1. Confirm the workspace/capacity, SQL editor target, source files, and approved connections.
2. Check that no conflicting lab refresh or writer is running. Disable only lab schedules with owner approval.
3. Verify the presenter is at the **baseline**: A = 6, B = 5, Gold = 6, one match, five exceptions. Run the baseline checker.
4. Verify the report is unfiltered, current, and using the actual mode recorded during preflight.
5. Open only the windows needed: slideshow with notes on the private screen, active lab workbook, assigned SharePoint folder, Dataflow, Warehouse SQL, and model/report. Keep baseline and corrected source copies clearly separated.
6. Open SQL files in the required order. Keep reset/seed scripts closed unless the planned recovery branch requires them.
7. Confirm the customer technical lead can post links and take findings, and the backup presenter is ready if needed.
8. Choose the delivery mode below and state it honestly.

| Mode | Select when | How to describe outcomes |
| --- | --- | --- |
| Hands-on | Participant prerequisites and time-critical paths were verified | Record participant execution separately from facilitator demonstrations |
| Guided demonstration | Presenter path works but participant setup or runtime is not ready | Learners predict, inspect, and complete decisions; label live steps presenter demonstrated |
| Prepared-evidence delivery | The service path is blocked but approved captures and expected outputs are available | Teach the pattern and log the blocker; label results prepared evidence reviewed |

An expected-result file is a teaching aid, not evidence that a tenant execution succeeded. A SQL-only seed can preserve later SQL learning but does not validate SharePoint/Dataflow.

## 4. The three-hour run of show

| ET window | Elapsed minutes | Module | Explain/demo/debrief | Participant practice | Break |
| --- | --- | --- | --- | --- | --- |
| 11:00-11:25 | 0-25 | Architecture and opening | 17 | 8 | 0 |
| 11:25-12:00 | 25-60 | Repeatable ingestion | 17 | 18 | 0 |
| 12:00-12:50 | 60-110 | Curated SQL engineering | 20 | 25 | 5 |
| 12:50-1:25 | 110-145 | Consumption architecture | 15 | 20 | 0 |
| 1:25-1:50 | 145-170 | Operations and findings | 10 | 15 | 0 |
| 1:50-2:00 | 170-180 | Exit review | 0 | 10, facilitated review | 0 |
| **Total** | **180** | | **79** | **96** | **5** |

Use the clock as the primary control. Give a two-minute lab warning, then take one answer and one unresolved item rather than waiting for every pair to finish. Record incomplete tasks and their evidence state; do not silently declare them passed.

## 5. Module 1: Make the architecture decision

**Window:** 11:00-11:25 ET. Keep the deck visible until the Lab 1 handoff.

| ET window | Screen / slides | Delivery action |
| --- | --- | --- |
| 11:00-11:04 | Slides 1-3 | Welcome, business outcome, delivery pattern, and completion states |
| 11:04-11:07 | Slides 4-6 | Reconnect to Session 2 and define one output row |
| 11:07-11:12 | Slides 7-9 | Compare write paths, justify the Warehouse starting point, and explain layer responsibilities |
| 11:12-11:20 | Slide 10 -> Lab 1 | Pairs complete the architecture record and changed-requirement exercise |
| 11:20-11:25 | Slide 10 | Take one decision, probe the rejected alternative, and transition |

### What to say and show

Open with:

> We already know how to work with SQL, Power Query, and Power BI. Today we will connect those skills into one repeatable workload. The goal is not to use every Fabric component. It is to explain the design, prove the results, and identify what makes the next run supportable.

State that this is a low-code/SQL-first session, not a Python introduction or production sign-off. The scope is a comparison of two synthetic complete extracts. No employee data is needed.

On slide 6, ask what one row means before discussing storage. On slide 7, emphasize the difference between a Warehouse's supported T-SQL writes and a Lakehouse SQL analytics endpoint's query path. On slide 9, explain that bronze/silver/gold are responsibilities, not automatically three workspaces.

### Lab handoff

> Open Lab 1, workbook page 9. In pairs, record the business question, grain, starting point, alternative, and revisit condition. Assign each tool a purpose. You have eight minutes; no service setup is needed.

At debrief, ask: "What new requirement would justify adding a notebook?" Accept a requirement-based answer rather than a product preference.

**Exit gate:** A readable architecture decision, including the assumption that tenant paths still require verification.

**Transition:** "We have decided where this workload belongs. Now we need to make sure each refresh lands the intended input, not merely some files from the same folder."

## 6. Module 2: Prove repeatable ingestion

**Window:** 11:25-12:00 ET. Use the prepared dataflow; do not build connections from scratch on stage.

| ET window | Screen / slides | Delivery action |
| --- | --- | --- |
| 11:25-11:30 | Slides 11-14 | Define the source contract and point out the intentional duplicate/invalid value |
| 11:30-11:35 | Slides 15-18 -> prepared Dataflow | Show exact file filters, text types, destination mapping/replace, then distinguish tool roles and dependencies |
| 11:35-11:53 | Slide 19 -> Lab 2 | Learners inspect/run the prepared path, verify the unchanged reload, and capture the ingestion contract |
| 11:53-12:00 | Slide 19 / counts | Collect run evidence, distinguish scheduling from orchestration, and gate SQL readiness |

### Demo choreography

1. Start with slide 13's System A. Ask participants to predict what happens if `not provided` is converted to a number during ingestion.
2. Switch to the actual Dataflow query. Show the exact file/folder filter, text-preserving steps, and explicit existing Warehouse destination.
3. Show the replace setting and completed refresh history. If a fresh refresh is started, wait for its successful completion before treating it as evidence.
4. Show A = 6 and B = 5 in the Warehouse. Ask why an unchanged second load must not become twelve and ten.
5. Use slides 16-18 briefly to name full/incremental responsibilities, orchestration boundaries, and why a copy job/notebook is not automatically needed.

### Lab handoff and pacing

> Open Lab 2, workbook page 12. Use your assigned dataflow and source pair. Verify the destination settings, run and inspect the load, and prove that an unchanged rerun retains six and five rows. Record scheduling evidence separately from configuration.

For a fast learner, ask which rules an incremental design would need for updates, deletes, and late arrivals. Do not add an incremental implementation to this lab.

If a second refresh exceeds the rehearsed runtime, stop new attempts, inspect the current run, and use approved prior evidence to finish the explanation. Do not start SQL against a mixed or still-loading pair.

**Exit gate:** Matching, completed baseline inputs; count evidence; explicit trigger and downstream gate. A configured schedule alone is not a passed scheduled-execution test.

**Transition:** "Landing gives us evidence. Curation will decide which records can be compared and how every exception is explained."

## 7. Module 3: Curate, reconcile, and prove safe repetition

**Window:** 12:00-12:50 ET, including a five-minute break.

| ET window | Screen / slides | Delivery action |
| --- | --- | --- |
| 12:00-12:08 | Slides 20-24 -> Warehouse views | Trace raw/normalized values and source-key quality counts |
| 12:08-12:15 | Slides 25-29 -> procedure/results | Explain precedence, full outer join, execution, and publication protection |
| 12:15-12:20 | Pause on slide 30 | Five-minute break; state the exact return time |
| 12:20-12:45 | Slide 30 -> Lab 3 | Inspect, publish/check, rerun, follow correction, restore baseline, and test the guard |
| 12:45-12:50 | Slide 29 / results | Explain one exception and confirm the baseline handoff to consumption |

### Demo choreography

Show only the clauses necessary to explain the rule. The full definitions are in the lesson and packaged SQL; do not scroll through the entire procedure without a teaching purpose.

1. Query `silver.normalized_records`: raw ` a001 ` becomes A001; raw `not provided` produces a null amount.
2. Query `silver.record_summary`: A005 has two A rows, and its A amount is not arbitrarily selected.
3. Use slide 25 to explain that duplicate/invalid conditions precede comparison. Raw evidence retains secondary issues even when the primary classification is a duplicate.
4. Show `EXEC` separately from the procedure definition. Explain that a batch label does not prove the inputs belong together.
5. Show the six baseline classifications on slide 29 and in actual results. Tie A002, A005, and A006 back to the source files.

### Lab handoff and execution order

> At 12:20, open Lab 3, workbook page 15. Run the assigned scripts separately in your Warehouse. Inspect installed definitions rather than rerunning their CREATE statements. Capture the check results, not just a successful query status.

Use this target rhythm inside the 25-minute lab:

| Minutes within lab | Learner action | Script / evidence |
| --- | --- | --- |
| 0-4 | Inspect Silver and its raw/quality fields | Definitions `02` / `03`, or installed views |
| 4-8 | Publish and verify baseline | `05_publish_baseline.sql`, `06_check_results.sql` |
| 8-11 | Verify unchanged business state after rerun | `07_test_rerun.sql` |
| 11-18 | Follow A002's source correction | Corrected B file, completed reload, corrected publication/check |
| 18-25 | Restore baseline and test rejection | Baseline reload, `05` / `06`, `08_test_blank_key_guard.sql` |

These windows depend on measured refresh times. If correction plus reset cannot finish in fourteen minutes, use the **preselected** facilitator demonstration/evidence branch for those tasks. Learners still predict the changed result and record what was actually observed. Do not run multiple overlapping refreshes to catch up.

Expected correction: six keys, two matches, four exceptions. Expected restored baseline: six keys, one match, five exceptions. The blank-key test verifies pre-publication rejection and unchanged prior Gold; it does not simulate a failure halfway through writing Gold.

**Exit gate:** The environment used for the consumption demo is confirmed back at baseline. A pair unable to restore it must not join a different user's shared write target; use an approved baseline demonstration/model or remain blocked.

**Transition:** "The result is now explainable and repeatable. Next we will make sure different reports and SQL consumers do not redefine what an exception means."

## 8. Module 4: Publish a governed analytical experience

**Window:** 12:50-1:25 ET. Prefer the prepared model/report scaffold so the focus stays on semantics and verification.

| ET window | Screen / slides | Delivery action |
| --- | --- | --- |
| 12:50-12:57 | Slides 31-34 | Separate model reuse from mode and identify the tenant's actual supported route |
| 12:57-1:02 | Slides 35-38 -> model/report | Show a measure, filter behavior, source trace, and access boundaries |
| 1:02-1:22 | Slide 39 -> Lab 4 | Inspect/create measures and report, test actual mode/access/freshness, and complete the decision |
| 1:22-1:25 | Slide 39 / report | Confirm totals and ask where each definition is owned |

### Demo choreography

1. Name the actual mode before showing the report. Do not call it Direct Lake merely because the source is in Fabric.
2. Show `gold.reconciliation` mapped to model table `Reconciliation`.
3. Demonstrate one measure definition and explain that each measure in the DAX file is created separately.
4. Show unfiltered baseline totals: 6 compared, 1 matched, 5 exceptions, 16.67% match rate.
5. Filter to `AMOUNT_MISMATCH`: 1 compared, 0 matched, 1 exception, 0% match rate. Clear the filter afterwards.
6. Trace A002 to 200.00 versus 250.00. State that slide 37 is an illustrative report layout, not proof of a deployed customer report.
7. Explain the intended consumer test and the separate SQL access boundary. Perform only the approved, preflighted identity test.

### Lab handoff

> Open Lab 4, workbook page 18. Confirm the actual model mode, create or inspect the shared measures, and prove the totals and filter behavior. Record consumer access and freshness independently. If an identity test is unavailable, mark it blocked; do not elevate permissions to make it pass.

If starting with a prepared report, learners must still trace its data and measures and record that preparation. Reserve new-model authoring for pairs whose path was preflighted and fits the timebox.

**Exit gate:** Consumption decision identifies audience, mode, definition owners, access path, freshness check, and unresolved tests.

**Transition:** "A correct report today is only part of delivery. Now we will decide what happens tomorrow when a source fails and somebody else has to support it."

## 9. Module 5: Turn the solution into an operating agreement

**Window:** 1:25-1:50 ET. This is monitoring plus a tabletop, not deliberate disruption of a live environment.

| ET window | Screen / slides | Delivery action |
| --- | --- | --- |
| 1:25-1:30 | Slides 40-43 -> monitoring evidence | Show the dependent stages, a known run, and the correct failure boundary |
| 1:30-1:45 | Slides 44-47 -> Lab 5 | Pairs complete operating gates, owners, issue routing, and the failed-source scenario |
| 1:45-1:50 | Slide 47 / shared action record | Take the failure response and separate learning needs, data issues, and environment findings |

### Lab handoff

> Open Lab 5, workbook page 21. System A finished today, System B failed, and yesterday's report still opens. Write what stops, which publication remains valid, what users should be told, and what must be verified before retrying.

During the lab, use slides 44-46 as reference prompts for access/ownership, lifecycle, and issue classification. Do not lecture those slides again over participants' working time.

Require the runbook to name who confirms source readiness, who owns the connection, who supports SQL/model stages, and who triages environment findings. Ask how a rule change is reviewed and promoted, not which deployment product they prefer.

**Debrief questions:** "Which gate failed?" "Which state remains valid?" "What evidence permits retry?" "Is this a skill issue, a source issue, or an observed environment behavior?"

**Exit gate:** Ordered operating instructions, named owners, one learning action, and a real or explicitly simulated environment finding. An authentication failure is not automatically a GCC High-wide limitation.

**Transition:** "We have built the learning implementation and its operating outline. The final step is to state honestly what was completed and agree who owns the remaining work."

### Backup-presenter handoff, if required

Before 1:30, confirm the backup can share the deck and access the evidence. Hand over: current slide; baseline/corrected state; lab completion states; active findings; evidence location; remaining time; and agreed actions. The backup starts Lab 5 at slide 44 and finishes through slide 53. Do not make participants repeat earlier work to reconstruct context.

## 10. Module 6: Close with evidence and ownership

**Window:** 1:50-2:00 ET. Lab 6 is the exit review; there is no additional ten-minute exercise after it.

| ET window | Screen / slides | Delivery action |
| --- | --- | --- |
| 1:50-1:54 | Slides 48-50 -> Lab 6 | Inspect artifacts, record evidence states, and ask one or two teach-back questions |
| 1:54-1:58 | Slide 51 / completion record | Agree specific next actions, accepted owners, evidence, and review points |
| 1:58-2:00 | Slides 52-53 | Confirm follow-up track choices and close |

### What to ask

Ask participants to explain why A005 is not a match, why A006 is not zero, and why an ingestion schedule is not an end-to-end operating control. Ask for reasoning rather than memorized syntax.

Use the four evidence states consistently: participant completed; presenter demonstrated; prepared evidence reviewed; blocked. Expected source exceptions are not automatically implementation bugs.

Have the named people accept next actions. Record an unresolved identity test or pipeline invocation as scoped work, not "the platform is broken." Confirm SQL/Warehouse versus notebook/Spark follow-up interest with participants and the technical lead; neither is a maturity ranking.

Close with:

> We now have a reasoned architecture, an ingestion contract, explicit reconciliation rules, a consumption decision, and an initial operating model. Where a path was demonstrated or blocked, that distinction is recorded. The next success test is another practitioner repeating the scenario using these artifacts without hidden steps.

Stop at 2:00. Keep slide 54 available for references rather than adding a new lecture.

## 11. Facilitation and recovery rules

### Keep the room moving

- Announce every change of mode: "Watch this step," "Now work in pairs," or "Return to the result." Tell learners the lab/task, time limit, expected evidence, and stop condition.
- Use the technical lead for participant triage. Give an unexpected environmental issue at most two minutes of full-room troubleshooting before recording it and taking the approved fallback.
- Spend time on the decision, not on repeated navigation. Pre-open the exact query, source file, or model page.
- Do not read the handbook while presenting the same explanation from the deck. Use it to answer a question or assign later reading.
- Keep a parking lot with question, owner, next action, and review point. Do not let future notebook, incremental-load, or governance deep dives consume the exit review.

### Fallback matrix

| Problem | Continue safely | What must remain unverified |
| --- | --- | --- |
| Participant cannot create/write items | Use the approved presenter path and paired prediction/inspection | That participant's independent execution |
| SharePoint/Dataflow unavailable | Use captured evidence; optionally use the approved SQL-only seed for later SQL work | Real ingestion and scheduling |
| Pipeline invocation fails | Show direct-ingestion scheduling and explicitly supervised downstream steps | Unattended end-to-end orchestration |
| Refresh exceeds the window | Inspect the existing run; use preflighted evidence without starting competing runs | Any unobserved reload/correction/reset |
| SQL or guard test gives an unexpected error | Stop that target; inspect transaction state and use a verified presenter/evidence path | The failed target's successful publication/recovery |
| Model mode unavailable | Use a verified approved mode or prepared model evidence; name the actual path | Availability of the originally intended mode |
| Consumer identity test unavailable | Explain boundaries and record a scoped access action | Consumer access; presenter access is not a substitute |
| Display/recording access fails | Use approved distributed PDFs/source files and the written evidence record | Receipt of an unavailable recording |

### If running late

Keep the module boundaries and final ten-minute exit review. Cut repeated explanation and UI navigation first. Convert slower correction/reset or new-model authoring to explicitly labeled presenter/prepared evidence rather than pretending all tasks were executed.

Preserve the architecture decision, source-pair gate, baseline classifications, duplicate/invalid reasoning, a rerun explanation, consumption/freshness boundary, and operating response. If even those cannot fit, record the specific incomplete outcomes and agree a continuation; do not quietly reduce the scope and claim completion.

## 12. Customer handoff and repeatability

Before closing, confirm the customer can find:

1. The deck, teaching handbook, lab workbook, and source lab files.
2. Each pair's decisions, actual evidence states, and approved artifact locations.
3. The exact baseline/corrected state left in any retained training environment.
4. The operating checklist, separate issue records, and accepted owners/review points.
5. Reset instructions and owner-approved schedule/artifact retention.

After delivery, send a short written handoff using the approved channel:

> **Delivered:** Session 03 low-code reconciliation pattern and the linked materials.  
> **Observed:** List the paths actually executed and their evidence.  
> **Not yet verified:** List blocked or demonstrated-only participant outcomes.  
> **Actions:** Named owners, specific next steps, evidence, and agreed review points.  
> **Repeatability:** Confirm who will repeat the scenario using the runbook and how the result will be reviewed.

Do not delete artifacts, disable shared schedules, invent commitments, or call the workshop a production deployment. The delivery is successful when the customer understands the design, can distinguish proven results from open dependencies, and has an actionable path to repeat it.

To rebuild the printable guide from the training directory, run `python lessons/session_03/artifacts/build_delivery_guide.py`. Recheck slide numbers and PDF page references whenever the deck or participant materials change.
