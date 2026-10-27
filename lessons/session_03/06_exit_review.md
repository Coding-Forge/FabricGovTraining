# Lesson 6: Exit review

**Session 3 | October 28, 2026 | 10 minutes**  
**Blueprint:** [Module 6](../session_3_blueprint.md#module-6-exit-review---10-minutes)  
**Lesson output:** An evidence-based completion record, owned follow-ups, and participant track alignment.

## What this lesson teaches

An exit review is not a recap of which Fabric screens were opened. It is a short acceptance conversation: what can participants explain, what was actually completed, what remains unresolved, and who will do the next piece of work?

This matters because a workshop can feel successful while leaving behind an implementation that nobody can repeat. Our goal is to make that gap visible without treating an environment blocker as a learner failure.

Use four minutes to confirm artifacts and conduct teach-back, four minutes to assign unresolved work, and two minutes to align follow-up learning tracks.

## 1. Confirm the artifacts, not just attendance

The blueprint defines five substantive outputs before this exit review. Inspect them together:

| Lesson | Expected artifact | Evidence of a useful result |
| --- | --- | --- |
| Architecture | Decision record | Explains the selected platform, rejected alternative, assumptions, and revisit condition |
| Ingestion | Refresh contract | Names the source scope, destinations, load mode, trigger, and downstream gate |
| SQL engineering | Curated objects and results | Explains classifications and demonstrates or clearly labels rerun behavior |
| Consumption | Consumption decision | Names the model strategy, actual mode, access path, and freshness check |
| Operations | Checklist and findings register | Provides ordered success gates, failure handling, and responsible owners |

For each artifact, record one of four states:

**Participant completed** means the participant performed the work and can explain the result.

**Presenter demonstrated** means the live path was shown, but participant execution has not yet been established.

**Prepared evidence reviewed** means screenshots, scripts, or previously generated results were used instead of a live execution.

**Blocked** means the required outcome could not be established because a dependency remained unresolved.

These labels are not grades. They describe the evidence honestly. A prepared screenshot can preserve the lesson when a tenant issue occurs, but it cannot prove that the participant's connection works.

## 2. Use teach-back to reveal understanding

Ask participants to explain the flow in their own words. A strong explanation connects each component to its purpose:

> We selected Warehouse because this structured reconciliation workload needs relational transformations and is owned by a SQL-oriented team. Dataflow Gen2 selects the intended SharePoint files and replaces the source-aligned landing snapshots. SQL normalizes comparable values, identifies quality problems, and publishes one result per business key. A shared semantic model provides reusable reporting measures. The operating flow confirms source alignment and stage success before downstream publication.

Then probe the decisions with a few short questions.

**Why is A005 an exception rather than a match?** There are two System A rows for its key. The comparison contract does not authorize choosing one, even though their amounts agree.

**Why does A006 not become zero?** An unconvertible source value is missing valid numeric evidence, not a legitimate zero amount.

**What happens when we rerun unchanged inputs?** Replace-mode ingestion preserves the same six and five landing rows. The procedure replaces Gold with the same six classifications instead of appending duplicates.

**Why is a direct dataflow schedule not necessarily an end-to-end solution?** It starts ingestion but does not prove downstream SQL execution, model freshness, or success dependencies.

**What would justify a notebook later?** A demonstrated requirement for an appropriate pro-code capability, such as custom Python processing or Spark engineering, rather than the desire to include another tool.

Do not require participants to memorize syntax. We are checking whether they can explain the consequences of the design.

## 3. Review unresolved questions and assign owners

A question without an owner is unlikely to become an action. Convert each unresolved item into a specific next step with an accountable person, expected evidence, and an agreed review point.

For example, "Pipelines are broken" is too broad. A useful action is:

> Retest pipeline invocation of the named training dataflow using the approved connection and intended execution identity. Capture the sanitized run result, confirm the investigation status, and update the environment finding before unattended scheduling is proposed.

Likewise, "Need more SQL training" is not a sufficiently focused learning action. Replace it with:

> Practice executing the reconciliation procedure twice and explain why the output remains one row per key.

Use this completion record:

| Item | Current state | Owner | Next action | Completion evidence | Review point |
| --- | --- | --- | --- | --- | --- |
| Architecture decision | Record actual state | Assign person | Resolve assumptions or approve decision | Updated decision record | Agree date/event |
| Repeatable ingestion | Record actual state | Assign person | Validate outstanding source/destination path | Refresh result and counts | Agree date/event |
| SQL publication | Record actual state | Assign person | Complete rerun or recovery walkthrough | Expected result and execution evidence | Agree date/event |
| Consumption | Record actual state | Assign person | Verify mode, freshness, or consumer identity | Model/report evidence | Agree date/event |
| Operations/findings | Record actual state | Assign person | Close the highest-impact operating gap | Updated checklist or finding | Agree date/event |

Do not fill this table with invented commitments. The relevant people must accept ownership.

Keep source-data exceptions separate from unresolved implementation work. A005 being classified as a duplicate is the expected lesson result, not necessarily a SQL defect requiring a code fix.

## 4. Align the follow-up tracks

The blueprint separates deeper Warehouse/SQL engineering from notebook/Spark engineering. Track selection should reflect the work each participant will own, not a ranking of which tool is more advanced.

The **SQL/Warehouse track** fits practitioners responsible for relational modeling, stored procedures, repeatable full/incremental processing, quality rules, and SQL operations.

The **notebook/Spark track** fits selected engineers responsible for Python/PySpark transformation, Delta engineering, parameterized notebooks, and their orchestration.

Participants can have a primary track and later gain familiarity with the other. They do not all need Python to consume a governed semantic model, and notebook engineers still need to understand shared data contracts.

Record each participant's intended responsibility, preferred follow-up track, and one concrete skill to develop. Confirm this with the participant and technical lead rather than assigning tracks based only on today's tool familiarity.

## 5. Close with a repeatability standard

The strongest next demonstration is for another practitioner to repeat the scenario using the agreed guide and approved artifacts, without relying on the original presenter to remember hidden steps.

That does not mean every production gate has been satisfied today. This session establishes a repeatable learning implementation and makes the remaining operating and environment work explicit.

Close with the outcome:

> We have a reasoned architecture, a defined ingestion contract, explicit reconciliation rules, a consumption decision, and an initial operating model. Where we demonstrated rather than independently completed a path, that distinction is recorded. Where a dependency remains unresolved, it has an owner and an evidence-based next action.

**Previous:** [Lesson 5](05_operations_and_gcc_high_findings.md)  
**Session outline:** [Session 3 blueprint](../session_3_blueprint.md)
