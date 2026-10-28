# Session 03 slide-by-slide presenter notes

These notes supplement the six lessons and the delivery guide. Use the teaching language selectively, not as an additional lecture to read in full. Demo and lab windows remain inside the existing three-hour agenda. Workbook references use physical PDF pages, including the cover.

## 01 | Low-code Fabric Data Engineering

OPEN: "Today we are going to connect skills you already have into a repeatable Fabric workload. We will take two extracts, preserve their evidence, explain where they disagree, and publish something another person can use and support. This is not a tour of every Fabric component."

TEACH: Set the audience expectation: SQL and Power Query remain the principal engineering tools. A notebook is an option when a requirement needs it, not a prerequisite for being a data engineer. All records in the exercises are synthetic. We are not moving employee information or changing production settings.

ORIENT: Ask participants to open the lab workbook and keep the teaching handbook available. Explain the rhythm: a short explanation, a prepared demonstration, a matching lab, and a debrief. Ask them to capture evidence and questions rather than silently working around a permission issue.

BOUNDARY: Distinguish a live demonstration, independent participant completion, prepared evidence, and a blocked step. Tenant availability and access must be observed; neither this presentation nor a product diagram proves them.

TRANSITION: "Before we touch a service, let us agree what success looks like and how the three hours fit together."

## 02 | Our three-hour learning path

TEACH: Walk through the sequence as a dependency chain rather than six unrelated topics. Architecture establishes the grain and tool responsibilities. Ingestion supplies the intended inputs. SQL makes the comparison explicit. Consumption shares the result. Operations explains tomorrow's run. The exit review records what was actually achieved.

PACE: The session runs from 11:00 AM to 2:00 PM ET. The module allocations already include demonstrations, discussion, transitions, and 96 minutes of participant practice. The five-minute break is 12:15-12:20, inside SQL engineering. Do not add a separate lab block after a module or another exit exercise after 2:00.

ASK: "Which stage currently causes the most rework in your team: getting the input, agreeing the rules, sharing the result, or supporting the next run?" Take one or two short answers and use them as examples later; do not turn this into an open-ended requirements workshop.

FACILITATE: Prepared SQL objects and a model/report scaffold keep time focused on reasoning and evidence rather than typing or connection setup. Record unresolved topics for owned follow-up.

TRANSITION: "The test is not whether we visited every screen. It is whether we can explain, repeat, and support the result."

## 03 | The standard: explain it, repeat it, support it

TEACH: Explain means a practitioner can defend the tool choice and trace a result to its inputs. Repeat means the same complete inputs produce the same business state without accidental duplication. Support means someone knows which gate failed, which result remains valid, and who owns recovery.

EXAMPLE: A report showing five exceptions may be correct; this dataset deliberately includes quality problems and genuine differences. A refresh showing green may still have selected the wrong folder or combined different snapshot periods. Separate execution evidence from business correctness.

ASK: "If the presenter can open the report but the intended reader cannot, which part of this standard has not been met?" EXPECT: The consumer/access and support evidence remains incomplete even if transformation was successful.

BOUNDARY: Keep the session SQL/Power Query-first. Commercial product documentation is a reference for behavior to investigate, not proof of GCC High deployment or connection support. An observed authentication failure is also not proof of a universal Government limitation.

TRANSITION: "We will start by deciding what this workload needs, then choose the smallest architecture that can satisfy it."

## 04 | Architecture decision framework

OPEN THE MODULE: "The output of this section is a decision record, not a list of products. Another practitioner should understand what we selected, why we selected it, and what would make us reconsider."

TEACH: A useful decision starts with the business outcome, the grain, source characteristics, operating skills, and consumption needs. It then records a justified choice and a plausible rejected alternative. Assumptions are not hidden facts: tenant support, permissions, source readiness, and performance are conditions to verify.

ORIENT: Keep slides 4-6 within 11:04-11:07. Use the business scenario and one-row definition before discussing product features. Slides 7-9 compare the engineering/write path, explain the proposed chain, and clarify layer responsibilities. Lab 1 begins on slide 10 at 11:12.

ASK: "What would convince someone who did not attend this workshop that our starting point was reasonable?" EXPECT: A recorded requirement and rationale, not "it was the newest feature" or "that is what the presenter used."

TRANSITION: "Let us define the question the data must answer before choosing where the data should live."

REFERENCE: The complete architecture lesson follows in the reference portion of these notes; it is preparation material, not additional live lecture time.

## 05 | Start with the business question

TEACH: The business question is whether two complete extracts describe the same records, amounts, and statuses, and which exceptions require investigation. Loading a file successfully does not answer that question. Neither does finding only the records that happen to exist in both systems.

EXPLAIN: The inputs use different column names and representations. One source calls its identifier RecordId; the other calls it Reference. Differences in casing and spaces may be harmless representation differences, while an amount difference may matter to the business. Missing records and unusable values must remain visible.

ASK: "If we loaded every row without an error, could the reconciliation still be wrong?" EXPECT: Yes: the selected files might cover different periods, normalization might be inappropriate, duplicates might multiply joins, or source-only records might disappear.

CONNECT: The output needs both a trustworthy summary for Power BI and detail that SQL practitioners can investigate. That dual need explains why the design preserves source evidence and publishes explicit classifications.

TRANSITION: "Now that the question is clear, we need a precise definition of one answer row."

## 06 | Define what one result row means

TEACH: Say the grain aloud: "One normalized business record ID in one comparison of two complete snapshots." Distinguish an input row from an output business key. System A has six rows; System B has five. The union of their normalized keys contains six identifiers, so eleven source rows do not imply eleven published results.

EXAMPLE: A005 occurs twice in A. The repeated row is evidence of ambiguity, not a second business record to count. The design publishes one A005 result marked DUPLICATE_KEY rather than choosing an arbitrary winner. A003 and A004 still need results even though each exists on only one side.

ASK: "Why not keep the first A005 row if both amounts happen to agree?" EXPECT: There is no approved rule identifying the authoritative occurrence; identical values do not remove the duplicate-key violation.

BOUNDARY: A blank key cannot be assigned safely to the stated grain. The teaching procedure blocks publication rather than inventing an identifier or silently dropping the row.

TRANSITION: "With the grain and operations defined, we can compare Warehouse and Lakehouse on the capabilities this workload actually needs."

## 07 | Warehouse or Lakehouse?

TEACH: Both choices use OneLake and Delta. The distinction here is the development and operating model, not whether one product is modern or whether one has a SQL editor. Our team needs relational transformations, supported T-SQL table writes, reusable views/procedures, and controlled publication.

EXPLAIN: A Warehouse is a natural starting point for that SQL-oriented work. A Lakehouse is valuable for file-oriented or Spark-based engineering and mixed data needs. Its SQL analytics endpoint provides a query path, but it does not make underlying Lakehouse tables writable through Warehouse-style T-SQL DML.

ASK: "Does being able to SELECT from a table through a SQL endpoint establish that we can INSERT into it through that endpoint?" EXPECT: No. Query access and supported data-writing capabilities are different contracts.

CAUTION: Do not describe either option as full SQL Server compatibility. Validate the T-SQL surface, transaction requirements, security path, and tenant availability for the chosen item.

TRANSITION: "For these tabular extracts and this team's SQL skills, the Warehouse-centered path is justified. Let us name the purpose of each stage."

## 08 | A Warehouse-centered path for this workload

TEACH: Trace the chain once from left to right. Dataflow Gen2 selects and lands the SharePoint extracts using familiar Power Query shaping. Warehouse SQL aligns fields, checks quality, and applies the comparison rules. Gold provides a stable business result. The shared semantic model adds reusable analytical measures and a governed reporting experience.

EXPLAIN: Every boundary should have a reason and a completion check. We do not need an additional notebook simply to perform a relational join that the operating team understands in SQL. Conversely, an actual custom extraction requirement may justify adding a targeted pro-code step.

ASK: "If one input later contains documents requiring Python extraction, must the reporting model and all SQL rules be discarded?" EXPECT: No. Revisit the affected ingestion/transformation stage and retain components whose contracts still meet the requirement.

BOUNDARY: This is an architecture proposal to validate, not evidence that every connector, schedule, or identity path works in the tenant.

TRANSITION: "Bronze, Silver, and Gold describe responsibilities within that chain. They do not automatically prescribe three separate deployments."

## 09 | Bronze, Silver, Gold: responsibilities first

TEACH: Bronze preserves source-aligned evidence, including duplicates, whitespace, and invalid amounts. Silver gives the records common names and evaluates quality without pretending that unusable input is valid. Gold publishes the agreed comparison result and fields consumers need to investigate it.

EXAMPLE: A006's text "not provided" belongs in the raw evidence. Its normalized amount is null, and its Gold classification is INVALID_AMOUNT. Those are three views of the same problem, not a reason to silently replace the source value with zero.

ASK: "Do three layers require three workspaces?" EXPECT: No. This training implementation uses schemas and views in one isolated Warehouse. Production boundaries depend on security, ownership, lifecycle, scale, and operational requirements.

CAUTION: A schema name alone does not establish access isolation. A view also does not freeze a point-in-time copy; it reflects its underlying data. We will return to that distinction when protecting source readiness.

TRANSITION: "You now have enough context to record a defensible decision and explain what would cause you to revisit it."

## 10 | Decision exercise

LAB HANDOFF: At 11:12, say: "Open Lab 1, workbook page 9. Work in pairs for eight minutes. Record the outcome, grain, starting point, rejected alternative, assumptions, and revisit condition. Assign each tool a specific job. No service setup is needed."

COACH: Ask pairs to describe the requirement before naming a product. If a pair chooses Warehouse, ask why Lakehouse was not needed for this baseline. If they choose Lakehouse, ask how the required transformations would be written and operated, rather than dismissing the choice by name.

CHANGED REQUIREMENT: Introduce documents needing custom Python extraction. A strong answer identifies which boundary needs a new tool and how its output would rejoin the existing comparison contract. "Replace the entire design" is not justified without further requirements.

DEBRIEF: Give a two-minute warning, finish practice at 11:20, and use the next five minutes for one decision and one unresolved assumption. EXPECT: A requirement-based choice, a stated grain, an alternative, and tenant paths still marked for verification.

TRANSITION: "We have decided where the workload belongs. Now we need to prove that each refresh lands the intended inputs."

## 11 | Repeatable ingestion

OPEN THE MODULE: "A successful connection is the beginning of ingestion, not the completion test. The next run must select the same intended scope, use the expected destination behavior, and provide evidence that both extracts are ready."

TEACH: Distinguish a source contract from the mechanics of retrieving a file. The contract identifies the folder/files, comparison period, expected columns, complete-snapshot meaning, owner, and readiness signal. A configured refresh and an observed successful execution are different evidence.

PACE: Use 11:25-11:30 for slides 11-14. The prepared Dataflow demonstration and slides 15-18 share 11:30-11:35; avoid creating connections from scratch. Lab 2 runs 11:35-11:53, followed by verification and debrief until noon.

ASK: "What would make two individually valid extracts an invalid pair?" EXPECT: Different effective periods, incomplete uploads, one failed refresh, or uncertain source scope.

BOUNDARY: Preserve text landing values and the intentional bad data. Removing the duplicate or invalid amount to obtain a green refresh would defeat the later quality lesson.

TRANSITION: "Let us state the source contract before inspecting the example files."

## 12 | A folder is not a source contract

TEACH: A folder can contain old extracts, temporary uploads, corrected copies, or unrelated files. The query needs precise selection rules, while the operator needs a readiness check that confirms the intended complete pair. File existence alone does not establish business alignment.

EXAMPLE: A file uploaded today may describe yesterday's period. Two refreshes can both succeed while comparing different business dates. Counts are useful but cannot prove that the correct files were selected.

ASK: "Who decides that the pair is ready, and what evidence do they provide?" EXPECT: A named source/readiness owner and a specific confirmation, not an assumption that a clock time guarantees completion.

SHOW: In the prepared environment, identify the approved SharePoint site/folder and connection ownership without displaying credentials. A presenter's browser access does not prove that the stored connection or scheduled execution identity can read the files.

CAUTION: Use only the active baseline pair in the ingestion folder. Corrected and expected-result files remain separate teaching assets.

TRANSITION: "The two small files deliberately contain the kinds of evidence that a permissive ingestion process must not erase."

## 13 | System A: preserve the intentional problems

TEACH: Read the six rows as evidence, not as a cleaning checklist. A001, A002, and A003 establish normal records. A005 appears twice with the same amount; that is still a duplicate-key condition. A006 carries the nonnumeric text "not provided."

ASK: "What happens if an automatic type-conversion step changes Amount to a number before landing?" EXPECT: The invalid value may produce an error or be transformed in a way that loses the original explanation. The training contract lands all source fields as text.

EXPLAIN: Keeping the bad value does not mean approving it. Bronze preserves it so Silver can evaluate it and Gold can report it honestly. Likewise, deduplicating A005 during ingestion would remove the very evidence needed to explain its classification.

SHOW: Point to A005 and A006 rather than reading all rows. Remind participants that the destination count should be six, including the duplicate.

TRANSITION: "System B is smaller and uses different names. Its differences include both harmless formatting and business exceptions."

## 14 | System B: representations and business differences

TEACH: Map Reference to the common record identifier, Total to amount, and State to status. The first identifier contains surrounding spaces and lowercase characters. The quotes on this slide expose those spaces; they are not extra characters in the CSV value.

EXAMPLE: After the approved trim/uppercase normalization, B's first key becomes A001 and agrees with A. A002 remains a genuine 200.00-versus-250.00 amount difference. A003 appears only in A, while A004 appears only in B. A005 has one B row, and A006's valid B amount does not repair A's invalid input.

ASK: "Which difference should disappear after normalization, and which must remain visible?" EXPECT: A001's formatting difference disappears; amount differences, source-only records, duplicate evidence, and invalid amounts remain.

CHECK: The intended B landing count is five. A successful load of five rows is necessary for this baseline, but source-scope and matching-period evidence are still required.

TRANSITION: "We will now inspect the prepared ingestion path and verify where those exact six and five rows land."

## 15 | Dataflow walkthrough: select, preserve, land

LIVE DEMO: At 11:30, switch from the deck to the prepared Dataflow. Identify the assigned source folder and exact file filter. Open the applied steps and show that landing columns remain text. Inspect any automatically added type change rather than assuming it is harmless.

SHOW: Trace each query to its explicit existing destination: bronze.system_a and bronze.system_b in the isolated Warehouse. Show the supported replace behavior and mapping. Do not remove A005 or filter out A006 to obtain a successful refresh.

PROVE: Inspect completed refresh history and then the actual Warehouse counts: A = 6 and B = 5. A preview is not a destination write. If you start a fresh run, do not claim completion until it actually finishes successfully.

ASK: "Where is the evidence that the rows reached the intended table?" EXPECT: Destination results plus the matching successful run, not just the query preview.

FALLBACK: If the connection or refresh is blocked, use approved prepared evidence and label it. Do not change broad permissions during the demonstration.

RETURN: Resume at slide 16; keep slides 16-18 brief within the same five-minute demo/explanation window.

## 16 | Replace, append, and incremental are different

TEACH: Replace represents the current complete snapshot. Append accumulates incoming rows. Incremental processing is a correctness design that needs reliable change evidence and rules for keys, updates, deletes, checkpoints, late arrivals, and retries.

EXAMPLE: With the same complete inputs loaded twice, replace should leave six A rows and five B rows. Append would produce twelve and ten. That extra volume is not additional business activity; it is repeated ingestion of the same snapshot.

ASK: "If an incremental source tells us only which rows changed, how do we discover a deletion?" EXPECT: The design needs an explicit deletion/tombstone mechanism or another approved reconciliation strategy. A timestamp filter alone is not a full answer.

BOUNDARY: Full replacement suits this small teaching workload. Do not extrapolate it as the correct load method for every enterprise source. Also do not call append "incremental" merely because fewer settings were required.

CONNECT: Lab 2 proves the chosen contract by rerunning unchanged inputs. It does not build a production incremental pipeline.

TRANSITION: "Even the correct load mode does not tell downstream work when both inputs are safe to use."

## 17 | Scheduling starts work. Orchestration gates it.

TEACH: A schedule answers "when should this activity start?" Orchestration answers "what must have succeeded, what evidence is required, and what happens next or on failure?" A fifteen-minute gap between independent schedules does not establish a dependency.

EXAMPLE: A completes today while B fails and retains yesterday's landing table. Both tables contain rows, so a simple nonempty check can pass even though the pair is invalid. The operator must establish that both completed extracts belong to the intended comparison before SQL publication.

ASK: "If SQL ran at 6:15 after a 6:00 ingestion schedule, what do we actually know?" EXPECT: Only the planned times; we still need run completion, source alignment, and downstream success evidence.

BOUNDARY: Independent Dataflow replacements are not one atomic update across the pair. In this lab, an explicit supervised readiness gate is acceptable. Call direct ingestion scheduling plus manual SQL partial automation, not an unattended end-to-end pipeline.

TRANSITION: "Let us separate the tools' responsibilities so that moving data and coordinating work are not confused."

## 18 | Give each tool a defined job

TEACH: Dataflow Gen2 supplies Power Query selection, shaping, and loading. A supported pipeline can coordinate activities and dependencies. A copy job may suit movement-oriented requirements. Warehouse SQL owns this design's relational normalization and comparison rules. A notebook is reserved for a justified pro-code requirement.

ASK: "Which tool should decide that a duplicate key takes precedence over an amount comparison?" EXPECT: The shared, approved reconciliation logic, implemented here in SQL, rather than five reports or unrelated copy settings.

EXPLAIN: Tool roles can evolve, but each transition needs an input/output contract and an owner. Adding another service without a responsibility creates more places to investigate, not automatically more reliability.

CAUTION: Do not assume a copy job supports this exact SharePoint transformation or that a pipeline's available activity proves its connection works in Government. Verify the actual connector, destination, supported mode, identity, and tenant behavior.

TRANSITION: "Now you will prove the existing refresh contract and record what must stop when one input fails." Return the participants' attention to slide 19 and the lab workbook.

## 19 | Prove the refresh contract

LAB HANDOFF: At 11:35, say: "Open Lab 2, workbook page 12. You have eighteen minutes. Inspect the assigned source pair, mappings, and destination behavior. Run and inspect the prepared load, then prove that an unchanged reload leaves six A rows and five B rows."

COACH: Require evidence of the destination counts and completed run, plus the source scope, trigger, execution owner, and downstream gate. The original duplicate must remain. Ask learners to record schedule configuration separately from proof of scheduled execution.

FAILURE SCENARIO: "A succeeded; B failed. May we publish a new comparison?" EXPECT: No. Preserve the prior publication and restore a verified matching pair before proceeding. Nonempty tables and a plausible count do not establish alignment.

PACE: Give a two-minute warning at 11:51. From 11:53 to noon, collect one explanation and unresolved items. If refresh time overruns, stop starting new attempts and use labeled approved evidence; do not rush into SQL against active loads.

TRANSITION: "Landing gives us evidence. SQL curation will decide which records can be compared and how the exceptions are explained."

## 20 | Curated SQL engineering

OPEN THE MODULE: "Our SQL is a chain of explainable decisions: normalize representations, assess source/key quality, preserve source-only records, apply approved precedence, and publish one result per business key."

TEACH: Distinguish definitions from executions. A view defines reusable query logic; a procedure defines a repeatable operation; EXEC performs that operation. Prepared definitions save typing time, but participants still need to explain the rules and inspect observed results.

PACE: Use 12:00-12:08 for the object chain and Silver examples, then 12:08-12:15 for precedence, join, procedure, and baseline. Pause on slide 30 for the five-minute break at 12:15. Lab 3 runs 12:20-12:45, with a five-minute results debrief afterward.

SAFETY: Use the isolated Warehouse, not a Lakehouse SQL analytics endpoint. Run each packaged SQL file separately. If views/procedure already exist, inspect them rather than rerunning CREATE or improvising a drop.

TRANSITION: "We will look at the chain first, then trace the specific fields that explain A001, A005, and A006."

REFERENCE: Complete lesson SQL remains below in the original reference notes; code excerpts on teaching slides are not complete execution scripts.

## 21 | Build a chain of explainable SQL objects

TEACH: Name the physical and logical boundaries. Bronze has two source-aligned text tables. silver.normalized_records standardizes the two schemas while retaining raw evidence. silver.record_summary assesses each source/key. gold.reconciliation is the physical current-result table written by gold.usp_refresh_reconciliation.

SHOW: Switch to the prepared Warehouse SQL editor and identify these objects. The schemas and Bronze tables should already exist from preflight because ingestion needed explicit destinations. The normalized and summary view definitions, followed by the procedure definition, are separate executions.

ASK: "Which objects store the current rows, and which expose reusable logic over those rows?" EXPECT: Bronze and Gold tables store rows; the Silver views expose query logic. A view is not a second scheduled load or an immutable snapshot.

CAUTION: Do not concatenate the CREATE files. CREATE VIEW and CREATE PROCEDURE must begin their own batches; the packaged files deliberately contain no GO separators.

TRANSITION: "We will trace the raw value and its normalized form side by side, rather than accepting a cleaned column without an explanation." Continue with slide 22 and the installed normalized view.

## 22 | Normalize values without losing evidence

TEACH: Walk through the identifier expression in order: trim surrounding whitespace, apply the agreed uppercase convention, then turn an empty string into null. The result is a common comparison key, not proof that the original source was clean.

SHOW: In silver.normalized_records, trace B's raw " a001 " to A001. Then trace A006's raw "not provided" to a null normalized amount through TRY_CONVERT. Zero would assert a valid numeric amount; null preserves that the attempted conversion did not yield one.

ASK: "Would uppercasing every identifier be safe for every business domain?" EXPECT: No. Case sensitivity and normalization rules require domain agreement. Real amounts also need an agreed currency, precision, locale, and any comparison tolerance.

BOUNDARY: The displayed SQL is an excerpt, not a runnable full SELECT. decimal(18,2) defines the normalized representation; it does not prove that source precision was originally two decimals.

TRANSITION: "The reusable view gives every downstream consumer the same normalization. It does not lock the source data in time."

## 23 | A view is logic, not a frozen snapshot

TEACH: A view is a stored query definition over underlying objects. It helps centralize normalization so that a report author, SQL investigator, and procedure do not each invent a different trim, type, or quality rule. It does not itself persist an independent copy of the input.

EXAMPLE: If Bronze is replaced while a later operation is reading Silver, the view does not magically preserve the earlier comparison state. That is why the workshop serializes loading and publication and requires a complete matching pair before SQL starts.

ASK: "Could both the normalized values be usable decimals and the comparison still be untrustworthy?" EXPECT: Yes. The sources could belong to different periods or be changing concurrently.

SHOW: Point again to raw and normalized A006 fields. Raw text explains why the normalized amount is null; retaining both makes investigation possible without reconstructing the source from memory.

BOUNDARY: A production batch/versioning design would need durable readiness and concurrency controls. Do not claim that adding a batch label to the output provides those controls.

TRANSITION: "Next we assess how many rows exist for each source/key before attempting a business comparison."

## 24 | Check key quality before joining

TEACH: Group by source_system and normalized record_id. COUNT(*) establishes whether each source contributes exactly one row. The amount is projected only when that count is one. MAX is simply a way to express the value of the sole row; the guard prevents it from choosing a winner among duplicates.

SHOW: Query silver.record_summary for A005. System A has source_row_count = 2, so the projected A amount is not arbitrarily selected even though the duplicate values happen to agree. Show the invalid amount/status counts used to explain other conditions.

ASK: "What changes if the two A005 amounts are identical?" EXPECT: The duplicate-key condition remains. Agreement of values is not an approved deduplication rule.

BOUNDARY: Blank keys are a different problem. They remain visible in normalized evidence and cause the procedure to reject publication. Duplicates and invalid values are published as classified exceptions under this teaching policy.

TRANSITION: "Quality evidence can overlap. We therefore need an explicit rule for which primary classification appears first."

## 25 | Classification precedence is a business rule

TEACH: Read the decision order, not the SQL syntax. Duplicate keys come first, then invalid amount, then invalid status, then source-only conditions, then usable-value mismatches, then MATCH. The first applicable rule supplies the primary classification.

EXAMPLE: If a duplicate row also has an invalid amount, DUPLICATE_KEY is the primary result; the raw and summary evidence still matters for diagnosis. If the present source has an invalid amount and the counterpart is absent, invalid amount precedes the source-only result in this teaching policy.

ASK: "Is there one universally correct precedence for every reconciliation process?" EXPECT: No. This is an explicit business policy that requires agreement. Reordering conditions changes the meaning of the published output, even when the join is unchanged.

FACILITATE: Ask learners to predict A005 and A006 before looking at baseline results. Reinforce that bad data can be an expected, successfully reported exception rather than an execution failure.

TRANSITION: "Once each source/key has been assessed, we still need a join that preserves records missing from either side."

## 26 | An outer join preserves the business question

TEACH: An inner join answers only "what exists in both sources?" That is insufficient when the question includes missing records. The full outer join preserves keys from either side, allowing A003 and A004 to become visible source-only exceptions.

EXPLAIN: Join source/key summaries, not raw detail. With two A005 rows and one B005 row, a raw join could create two rows that look like separate matched business records. Summarization preserves the one-key grain and lets the classification report ambiguity.

ASK: "Which results disappear if we switch to an inner join?" EXPECT: A003 and A004. Then ask what a raw join would do to A005; expect duplicate multiplication rather than one honest quality result.

CONNECT: COALESCE selects the surviving normalized identifier from whichever summary side exists. A missing side is not the same as a present row with an unusable amount, which is why the quality and presence rules remain separate.

TRANSITION: "The procedure packages these rules into a repeatable publication operation, with explicit inputs and a controlled failure path."

## 27 | A procedure defines repeatable SQL work

TEACH: CREATE PROCEDURE installs a reusable definition. EXEC invokes it. Parameters identify the requested operation, but they do not prove that external prerequisites have been met. The batch label is useful output metadata, not a validation that the source extracts belong together.

SHOW: In the prepared Warehouse, inspect only the important procedure sections: input label validation, nonempty source checks, blank-key rejection, Gold replacement, uniqueness check, commit, and catch/rethrow. Then show the separate EXEC used by 05_publish_baseline.sql.

ASK: "Could we supply a convincing batch ID while System B is still yesterday's data?" EXPECT: Yes. The operator's readiness gate and serialized execution remain necessary; the procedure's teaching checks do not establish source-period alignment.

SAFETY: Confirm the dedicated Warehouse and that no load or competing publication is running before invoking the procedure. Do not ask participants to recreate an installed procedure or type its full definition during the demo.

TRANSITION: "Repeatability also requires a clear publication boundary: consumers should not be left with a partially replaced Gold result."

## 28 | Protect publication, not just execution

TEACH: The transaction groups validation, Gold replacement, and output checks into one commit-or-rollback operation. If the operation fails before successful commit, the replacement is rolled back and the error is rethrown so the caller can detect failure rather than assume success.

EXPLAIN: This protects the Gold publication operation. It does not roll back external Dataflow refreshes, validate the business period of each file, refresh a semantic model, or retain historical snapshots. Gold contains the current publication only.

ASK: "Does keeping the prior Gold after a rejection mean today's comparison succeeded?" EXPECT: No. It means the prior committed state remains available; today's failed run must be recorded and consumers need an honest freshness statement.

POLICY: This example blocks empty sources and blank keys, but reports duplicate/invalid values as exceptions. Other workloads may choose different blocking rules, which require coordinated changes to SQL, monitoring, reporting, and operating instructions.

TRANSITION: "Now inspect the result as business evidence. Six explainable rows are more important than a successful EXEC message alone."

## 29 | Expected baseline: every result is explainable

SHOW: Compare actual Gold results with the six expected classifications. A001 matches after formatting normalization. A002 is an amount mismatch: 200.00 versus 250.00. A003 and A004 are source-only. A005 is duplicate-key ambiguity. A006 has an invalid A amount.

ASK: Choose one learner to explain A005 and another to explain A006 from the underlying evidence. EXPECT: No arbitrary duplicate winner and no conversion of invalid text to zero. Five exceptions are intentional; they do not mean the teaching process failed.

COUNT: Eleven input rows become six business keys, one match, and five exceptions. A count alone is insufficient: use 06_check_results.sql to verify the expected business fields and classification state.

DEBRIEF RETURN: Revisit this slide at 12:45 after Lab 3. Confirm that the demonstration/model source has been restored to the baseline before moving to consumption.

TRANSITION: "We will now test whether the same inputs preserve the business state and whether a single source correction flows through honestly." Advance to slide 30 and announce the break before starting the lab.

## 30 | Rerun, then follow one correction

BREAK: At 12:15, pause here and say: "Five-minute break; return at 12:20. Leave your assigned environment intact." Do not consume the participant lab time with another explanation.

LAB HANDOFF: At 12:20, open Lab 3, workbook page 15, for twenty-five minutes. Inspect installed Silver definitions, run 05_publish_baseline.sql and 06_check_results.sql separately, then use 07_test_rerun.sql with unchanged inputs.

COACH: An unchanged rerun preserves six business rows and the expected fields; publication time may change. Next replace the active B file with its corrected copy, not an additional file. Complete both intended reloads, publish with the corrected batch label, and run checker scenario 'corrected'. EXPECT: A002 becomes MATCH; totals become two matches and four exceptions.

RESTORE: Restore the baseline B file, reload, publish/check baseline, and run 08_test_blank_key_guard.sql without competing writers. Its expected rejection preserves prior Gold including publication metadata. This is a pre-publication guard test, not an injected mid-write failure.

PACE: Use the preselected demonstration/evidence branch if refresh times cannot fit. Give a two-minute warning, return to slide 29 at 12:45, and verify baseline before slide 31. Never patch Gold or start overlapping refreshes to catch up.

## 31 | Consumption architecture

OPEN THE MODULE: "A correct SQL table is the beginning of a governed analytical experience, not the whole experience. People still need shared definitions, an appropriate query path, approved access, and evidence that they see the intended publication."

TEACH: Keep two questions separate: where do shared business/reporting definitions live, and how does the model obtain/query its data? The reconciliation classification remains in Gold. Reusable DAX measures belong in the shared model rather than being reinvented in each report.

PACE: Slides 31-34 occupy 12:50-12:57. Use the prepared model/report from 12:57-1:02 alongside slides 35-38. Lab 4 runs 1:02-1:22; reserve three minutes for a debrief.

ASK: "If two reports use the same table but define exceptions differently, have we achieved reuse?" EXPECT: Shared storage alone is not shared semantics. The approved definition and its owner must also be consistent.

BOUNDARY: Name the actual verified mode in the demonstration. Do not label a model Direct Lake simply because its data originates in Fabric.

TRANSITION: "A shared semantic model and Direct Lake are not competing architecture choices; one describes reuse, the other describes a data access mode."

## 32 | Separate shared semantics from storage mode

TEACH: A shared semantic model offers reusable measures, names, relationships, formatting, and model-level rules. Import, DirectQuery, and Direct Lake describe how model tables obtain and query data. A shared model can use any supported, appropriate mode.

EXAMPLE: The Gold classification DUPLICATE_KEY should mean the same thing for a SQL investigator and a Power BI reader. Reporting measures such as Compared Records and Match Rate can be managed centrally without moving the record-level reconciliation algorithm into DAX.

ASK: "If a team changes its model from Import to another verified mode, should the meaning of MATCH change?" EXPECT: No. The business contract should remain stable even when the access/performance design changes.

CAUTION: A shared model is not a blanket security policy over every possible route to the data. Direct SQL and OneLake paths have their own permissions and do not automatically inherit DAX measures or model RLS.

TRANSITION: "Now compare the available routes using their actual freshness, identity, and operating behavior, not a preference for a label."

## 33 | Choose a verified consumption path

TEACH: Import copies data into model storage and needs a successful refresh after the intended publication. DirectQuery queries through the model to the source and still needs verified identity, connection, and performance. Direct Lake uses supported Delta tables with its applicable framing and freshness behavior.

DISTINGUISH: Direct SQL is a separate consumer route, not a fourth semantic-model storage mode. SQL readers query curated Gold under approved permissions and need an agreed contract for any aggregate definitions they share.

ASK: "If Gold has today's batch but the Import report shows yesterday's values, where should we investigate first?" EXPECT: The model refresh/freshness boundary, rather than automatically reloading every source.

BOUNDARY: Direct Lake is not a promise of zero memory use or no freshness management. Availability and creation experiences must be checked in the target tenant. A verified Import route can be a better delivery choice than an unverified claim about another mode.

TRANSITION: "If Direct Lake is available, identify which variant and source path you are actually using before drawing conclusions about its behavior."

## 34 | Direct Lake: verify the actual variant

TEACH: Direct Lake behavior depends on the actual variant and configuration. Direct Lake on SQL uses SQL endpoint discovery/permission behavior and can fall back to DirectQuery under supported settings. Direct Lake on OneLake does not use that same fallback path.

EXPLAIN: Our publication target is the physical gold.reconciliation table. Do not assume that choosing a SQL view has the same behavior as selecting a compatible physical Delta table. For the SQL-based variant, a view may cause fallback depending on settings and support.

ASK: "What evidence would you record rather than merely writing 'Direct Lake' in the decision?" EXPECT: The actual mode/variant, source object, connection/identity path, applicable behavior settings, and observed freshness/consumer result.

BOUNDARY: Do not use this slide to imply that either variant is available in every Government tenant. If a planned route is absent or blocked, use a preflighted approved alternative and record the deviation.

TRANSITION: "Whatever the verified mode, the measures must count the same published business keys and respect the report's filter context." Prepare to switch to the model on slide 35.

## 35 | Create measures that reuse the business contract

LIVE DEMO: At 12:57, switch to the prepared semantic model. Identify gold.reconciliation as the source and Reconciliation as the model table name. Open artifacts/dax/reconciliation_measures.dax and explain that each definition is created separately, in file order; the file is not a bulk DAX query.

TEACH: Compared Records counts rows at the published one-key grain, so the unfiltered baseline is six, not eleven source rows. Matched Records counts classifications equal to MATCH. Exception Records includes every non-MATCH result, including quality exceptions. Match Rate divides matched by compared records.

SHOW: Format Match Rate as a percentage with two decimals. Baseline is 1/6 = 16.67%. The corrected source would produce 2/6 = 33.33%, but the consumption demonstration should already be restored to baseline.

ASK: "Does a publication timestamp make this table a history table?" EXPECT: No. Current Gold is replaced; a trend requires an explicit history design.

RETURN: Use slide 36 to explain the filter behavior, then show that behavior in the same prepared report. Slides 35-38 and the demo share only five minutes.

## 36 | Respect the report's filter context

TEACH: CALCULATE evaluates a measure under a modified filter context. KEEPFILTERS intersects the measure's classification condition with an existing selection rather than replacing that selection. COALESCE presents zero for a count that would otherwise be blank in the no-match case.

SHOW: In the prepared report, filter classification to AMOUNT_MISMATCH. EXPECT: One compared record, zero matched, one exception, and a 0% match rate. Matched Records must not reintroduce A001 when the user explicitly selected only the mismatch classification. The full measure uses the same KEEPFILTERS pattern for MATCH.

ASK: "Why is the filtered denominator one rather than all six keys?" EXPECT: Compared Records respects the current report context. A different business metric needs a deliberately named and approved denominator, not an accidental filter override.

CAUTION: Do not remove quality exceptions to improve the headline percentage. If stakeholders need a rate among only comparable valid pairs, define and label that separately.

TRANSITION: "Clear the filter and inspect how a reader can move from a summary back to the source evidence."

## 37 | A report should summarize and explain

TEACH: The four cards are a starting point for investigation, not the entire report. A useful report connects the total exception count to classification detail and then to the source values that explain a specific key.

SHOW: With filters cleared, verify six compared, one matched, five exceptions, and 16.67%. Select A002 in the detail and trace A's 200.00 versus B's 250.00 back to Gold. Then trace A005 to duplicate-source evidence; its missing projected A amount is not a zero.

ASK: "If the report and SQL counts disagree, what would you inspect before declaring the SQL wrong?" EXPECT: Active filters, the source table and model mode, publication/batch state, model freshness, and the agreed measure definitions.

BOUNDARY: State explicitly that this slide is an illustrative layout made from editable PowerPoint shapes, not a deployed report screenshot. Only the actual demonstration or labeled prepared evidence can establish what was observed.

TRANSITION: "A convincing result under the author identity still leaves a separate question: can the intended reader access only the approved path?" Return to slide 38.

## 38 | Govern each access path independently

TEACH: Viewing a report and building another report over a shared model are distinct needs. Workspace collaboration roles, item permissions, model Build permission, and connection ownership also serve different purposes. Do not solve a reader problem by automatically granting broad editing privileges.

EXPLAIN: Semantic-model RLS and DAX definitions do not automatically govern independent SQL or OneLake access. A user who can query underlying data through another route needs that route's approved permissions and controls.

ASK: "Does a workspace administrator successfully opening the report prove that a restricted reader sees the right data?" EXPECT: No. Test with the approved consumer identity and intended route; elevated author access is not a substitute.

SHOW: Perform only the preflighted identity test. If the identity or access path is unavailable, record it as blocked rather than improvising role changes. Direct SQL consumers should use curated Gold and approved definitions.

TRANSITION: "Your next task is to record the actual route, actual evidence, and any remaining access or freshness gap." Advance to slide 39 and hand off to Lab 4.

## 39 | Choose and prove the consumption path

LAB HANDOFF: At 1:02, say: "Open Lab 4, workbook page 18. You have twenty minutes. Confirm the actual model mode, create or inspect the four measures, build or inspect the report detail, and record access and freshness evidence separately."

COACH: Verify the unfiltered baseline of 6/1/5/16.67%, then the AMOUNT_MISMATCH filter result of 1/0/1/0%. Clear the filter afterward. Learners must be able to trace A002 and explain why A005's quality condition is still an exception.

EVIDENCE: Require the audience, actual mode/variant, source/model names, definition owners, direct SQL decision, approved consumer test, and mode-specific freshness check. A prepared scaffold is acceptable when labeled; it is not evidence that a learner independently created a model.

BOUNDARY: If a consumer identity test is unavailable, mark it blocked. Do not elevate permissions or borrow another pair's write target to manufacture completion.

DEBRIEF: Give a two-minute warning at 1:20. From 1:22-1:25, ask where classification and measures are owned and which gate proves the intended publication is visible.

TRANSITION: "A correct report today is only part of delivery. Now we decide who supports tomorrow's failed source."

## 40 | Operations and GCC High findings

OPEN THE MODULE: "Operational readiness means someone other than the original author can determine whether the run succeeded, identify what failed, and take an approved next action without guessing."

TEACH: Organize the discussion around dependencies, evidence, failure boundaries, and ownership. A schedule is useful, but a runbook also needs to say what stops, what remains valid, who investigates, and which evidence permits recovery.

PACE: Use 1:25-1:30 for slides 40-43 and prepared monitoring evidence. At 1:30, start Lab 5. Slides 44-46 are reference prompts during the fifteen-minute tabletop, not another lecture over working time. Debrief at 1:45 and transition to exit review at 1:50.

ASK: "If you were covering for the author tomorrow, what would you need before deciding to rerun anything?" EXPECT: The failed stage, last valid publication, intended source pair, owner, current run state, and safe retry conditions.

SAFETY: This is a tabletop. Do not remove a permission, break a connection, or disrupt a shared environment to simulate failure.

TRANSITION: "First identify the success gates. We can then decide which evidence demonstrates each gate and where recovery belongs."

## 41 | Use success gates, not optimistic time gaps

TEACH: Walk through the required sequence: confirm a complete matching source pair, confirm both loads and quality/readiness checks, publish SQL, perform the model's actual freshness step, then verify the consumer result. Each stage needs evidence before its dependents proceed.

EXAMPLE: The procedure's nonempty-source check cannot tell whether B belongs to the intended period. A configured schedule cannot tell whether the stored identity succeeded. A completed SQL publication cannot tell whether an Import model refreshed. These are separate gates, not one green status.

ASK: "If the pipeline invocation is blocked but Dataflow scheduling works, how should we describe the solution?" EXPECT: Scheduled ingestion with explicitly supervised downstream steps: partial automation, not a proven unattended chain.

SHOW: Point to the known run/evidence chain prepared for this environment. If using a diagram or prior evidence instead of live history, label it accordingly.

TRANSITION: "Monitoring has to combine technical completion with business evidence. Let us name what each kind of signal actually proves."

## 42 | Monitor execution and business correctness

TEACH: Activity status indicates whether configured work completed. Counts and quality checks indicate whether certain data conditions hold. Publication and consumer evidence indicate whether the intended business result is visible. No single row in this table proves the entire chain.

SHOW: Use a prepared known run to connect the run identifier, selected source scope, start/end times, table names, actual/expected counts, SQL batch/publication metadata, and report observation. Identify the last successful publication independently of the current attempt.

ASK: "Could a run be green with the wrong files?" EXPECT: Yes. Technical success can faithfully execute an incorrect scope. Then ask whether six result rows alone prove six correct classifications; expect that field-level/result checks are also needed.

BOUNDARY: The synthetic six/five/six counts are fixture expectations, not generic production alert thresholds. Real workloads need agreed volume, quality, and timeliness tolerances.

SAFETY: Capture sanitized errors and relevant role/context. Do not collect credentials, tokens, or unnecessary source information in a finding.

TRANSITION: "Once we know which gate failed, recovery should target that boundary rather than blindly restarting every stage."

## 43 | Recover at the right boundary

TEACH: A failed B load blocks a new comparison until a verified matching pair is restored. A SQL failure before commit rolls back the Gold replacement but does not repair Bronze. A model freshness failure may leave new Gold behind an old report. Unexpected totals require checking context and rules before assigning blame.

ASK: "If Gold is correct and only the model refresh failed, what is the risk of immediately rerunning ingestion?" EXPECT: It adds unnecessary work and can introduce a new or mixed source state. Repair and verify the actual failed boundary under the approved retry policy.

EXPLAIN: Yesterday's report remaining readable is availability of a prior result, not proof of today's success. Communicate the publication/freshness state explicitly. A safe retry also needs serialized writers and known idempotent behavior; repetition is not automatically harmless.

LAB SETUP: At 1:30, announce Lab 5, workbook page 21, for fifteen minutes. Introduce the failed-B/yesterday's-report scenario and ask pairs to produce the ordered response. Use slides 44-46 as prompts before leaving slide 47 visible.

TRANSITION: "Write down who owns each gate, not simply which person has permission to click it."

## 44 | Access is not the same as ownership

LAB 5 REFERENCE: Use this slide as a quick prompt during the 1:30-1:45 tabletop, not a separate lecture. Participants should already be working from workbook page 21.

TEACH: Permission answers what an identity can do. Ownership answers who is accountable for a condition, maintenance task, or decision. A workspace Contributor may be able to edit an artifact without being the owner of the source contract, connection renewal, or business classification policy.

ASK PAIRS: "Who confirms source readiness? Who maintains the connection? Who owns SQL rules, the model/report, consumer permissions, and support triage? Who covers an absence?" EXPECT: Named responsibilities with accepted coverage, even when one person holds multiple roles.

EXAMPLE: Giving a reader workspace editing access may make a report open while invalidating the intended restricted-consumer test. An access workaround is not the same as demonstrating the approved security design.

BOUNDARY: Exact role capabilities depend on the actual item and current tenant behavior. Keep identity tests preflighted and do not grant broad roles during the exercise.

RETURN: Move briefly through slides 45-46 as needed, then leave slide 47 visible while participants complete their operating response.

## 45 | Naming and lifecycle make change supportable

LAB 5 REFERENCE: Keep this as a short question for pairs already writing their operating checklist. Do not add a new implementation task or deployment-product demonstration.

TEACH: Names help people find and distinguish artifacts, but a name containing "test" does not provide production isolation. Lifecycle practice establishes how changes are reviewed, checked against known evidence, promoted through an approved path, and recovered if they behave unexpectedly.

EXAMPLE: Suppose invalid amounts change from reportable exceptions to publication blockers. The SQL rule changes, but so do alerting, last-valid-publication behavior, report freshness explanations, and operating instructions. Treat the policy as a cross-artifact contract, not one edited CASE clause.

ASK: "What evidence would you require before approving that rule change?" EXPECT: Known baseline/correction behavior, the intended blocking case, verified failure handling, updated documentation, and accepted ownership.

BOUNDARY: Use only the team's verified promotion mechanism; do not assume commercial Git or deployment capabilities are present in Government. Cleanup also needs dependency review and owner approval.

RETURN: Let pairs add one review/promotion responsibility to their runbook, then use the issue-routing prompt on slide 46.

## 46 | Route the issue before proposing the fix

LAB 5 REFERENCE: Ask each pair to name one learning need, one data issue, and one real or explicitly simulated environment finding. Keep the categories separate because they have different owners and completion evidence.

EXPLAIN: Not understanding CREATE versus EXEC is a learning need. A005's duplicate is a source/data-quality condition. A reproducible connection or permission failure is an environment observation requiring investigation. A category is a routing decision, not a conclusion that a product is defective.

ASK: "What can we honestly write after one authentication error?" EXPECT: The scoped operation, timestamp, identity role/context, expected and actual behavior, sanitized evidence, impact, owner, and next investigation step. Not "GCC High does not support pipelines."

COACH: A useful interim approach records its manual effort and remaining dependency gaps. Direct Dataflow scheduling may preserve ingestion while leaving SQL/model coordination supervised; document that boundary and the condition for reviewing it.

BOUNDARY: Findings should not contain secrets or unneeded personal/source details. A simulated scenario must remain labeled simulated.

RETURN: Move to slide 47 so pairs can finish and defend the failure response.

## 47 | System A succeeded. System B failed.

SCENARIO: Leave this slide visible during Lab 5. Say: "Yesterday's report still opens. Has today's comparison succeeded? Write what stops, which state remains valid, what users should be told, and what evidence allows recovery."

EXPECTED RESPONSE: Today's comparison has not succeeded. Block new publication from the mismatched inputs, identify the last successful Gold/report state, capture the failed B run, and assign investigation to the appropriate owner. A successful A run and a readable old report do not satisfy the missing gate.

RECOVERY: Restore and verify a matching complete pair, ensure no competing writer, then perform SQL and the actual model freshness/consumer checks in order. If a prior publication remains visible, communicate its age and status instead of calling the current run successful.

DEBRIEF: Give the lab warning at 1:43; debrief 1:45-1:50. Ask "Which gate failed?", "What remains valid?", and "What proves retry is safe?" Require named owners, one learning action, and a scoped finding.

TRANSITION: "We now have a learning implementation and an operating outline. The final step is to record honestly what was done and who owns what remains."

## 48 | Exit review

LAB 6 HANDOFF: At 1:50, say: "Open Lab 6, workbook page 24. This ten-minute exit review is the lab itself, not another activity after the session. Have your artifact locations, evidence states, and open actions ready."

TEACH: Completion is about an explainable, repeatable outcome, not attendance or a sequence of screenshots. A prepared demonstration can be valuable learning, but it cannot be recorded as independent participant execution.

PACE: Use slides 48-50 from 1:50-1:54 to inspect artifacts and record evidence states. Use slide 51 from 1:54-1:58 to agree owned actions. Use slides 52-53 from 1:58-2:00 to confirm follow-up tracks and close.

ASK: Choose one or two teach-back questions: why A005 is not a match, why A006 is not zero, or why a Dataflow schedule does not prove end-to-end coordination. Listen for reasoning, not memorized labels.

BOUNDARY: An incomplete access or orchestration test remains an explicit open dependency. Do not convert it to completion to make the final summary sound better.

TRANSITION: "Let us inspect the actual outputs and their evidence, starting with the decisions that explain the design."

## 49 | Inspect the outputs, not just attendance

FACILITATE: Ask participants to point to their architecture record, ingestion contract, SQL checks, consumption decision, and operations/findings record. Prefer one concrete evidence location and explanation over a long account of which buttons were clicked.

TEACH: Acceptance is different for each artifact. Architecture needs rationale and a revisit condition. Ingestion needs scope, load behavior, and a downstream gate. SQL needs explained results and an observed or honestly labeled rerun. Consumption needs actual mode, access, and freshness. Operations needs failure handling and accepted ownership.

ASK: "Could another practitioner repeat the scenario using your record without asking you to remember an undocumented step?" EXPECT: A usable handoff includes prerequisites, order, known expected results, evidence, and unresolved dependencies.

COACH: If learners show only a successful query status, ask for the six classifications or the exact checker result. If they show only a report, ask which batch/source and identity path it represents.

PACE: Keep this inspection inside the first four minutes of Lab 6. Record omissions as actions rather than reopening an earlier lab.

TRANSITION: "Now label what kind of evidence each artifact actually represents."

## 50 | Describe the evidence honestly

TEACH: Use four states consistently. Participant completed means the learner performed and explained the task. Presenter demonstrated means it was shown live. Prepared evidence reviewed means the group inspected a previously captured or supplied result. Blocked means a required dependency remains unresolved.

EXAMPLE: A learner can explain a corrected A002 using the expected CSV even if their Dataflow connection failed. That is useful reasoning, but the live correction path is not independently completed. Similarly, a report opened under an administrator is not proof of restricted-consumer access.

ASK: "Why does this distinction matter for the next person repeating the lab?" EXPECT: It tells them which paths have been observed and which still require validation, so preparation and risk are not based on an inflated completion claim.

COACH: These are evidence states, not grades or blame. Preserve successful learning while making environment and access gaps visible. Expected duplicate/invalid input classifications are also not automatically implementation defects.

TRANSITION: "Every unresolved item now needs an accepted owner, a next action, and evidence that will let us close it."

## 51 | Turn open questions into owned work

FACILITATE: From 1:54-1:58, use a shared action record with item, current state, owner, next action, completion evidence, and agreed review point. Have the named person accept the action; do not invent deadlines or commitments on their behalf.

EXAMPLE: Replace "pipelines are broken" with a scoped retest: invoke the prepared Dataflow through the intended pipeline connection and role, capture the sanitized run result, compare expected/actual behavior, and update the finding. If the cause is unknown, record it as unknown rather than choosing a product-wide explanation.

ASK: "What observable result would let us close this action?" EXPECT: Specific evidence such as a successful run under the intended identity, a verified consumer view, or a reviewed decision, not merely "followed up."

COACH: Separate a learning exercise from a source-quality issue or an environment investigation. Do not turn A005's intentionally duplicated teaching input into an unowned software defect.

BOUNDARY: Unresolved production-readiness gates remain outside the claim of workshop completion.

TRANSITION: "With actions owned, choose the next learning track based on the work each person will actually perform."

## 52 | Choose follow-up tracks by responsibility

TEACH: The SQL/Warehouse track deepens relational modeling, procedures, repeatable loading, quality rules, and operations. The notebook/Spark track develops Python/PySpark, Delta engineering, parameters, and pro-code orchestration. These are responsibility-based choices, not a ranking of sophistication.

ASK: "Which type of work will you be responsible for next, and what is one skill you need to strengthen?" EXPECT: A participant-selected primary track linked to a real responsibility. A person may later learn both; do not assign notebook work merely because it sounds more advanced.

CONNECT: The architecture exercise showed why a custom Python extraction requirement can justify a targeted notebook component without invalidating the entire SQL-first design. Follow-up learning should be equally requirement-driven.

FACILITATE: Confirm choices with participants and the technical lead. Record interest and the next skill without inventing a scheduled future session or promising an unverified product capability.

PACE: Share the final two minutes with slide 53. Do not reopen technical design discussion or add a new exercise.

TRANSITION: "Whichever track you choose, the shared standard remains an implementation that another practitioner can explain, repeat, and support."

## 53 | One workload. A repeatable delivery model.

CLOSE: "We have a reasoned architecture, an ingestion contract, explicit reconciliation rules, a consumption decision, and an initial operating model. Where a path was demonstrated, reviewed from prepared evidence, or blocked, that distinction is recorded."

REINFORCE: The completion test is another practitioner repeating the scenario from the agreed artifacts without hidden steps. Point participants to the teaching handbook for explanations, the lab workbook for tasks, the setup runbook for safe repetition, and the accepted action record for unresolved work.

ASK: Use a final quick confirmation: "Do you know where the package and your next action are recorded?" Resolve only a missing location or owner; do not start a new technical thread.

BOUNDARY: Do not describe this learning implementation as production deployment, proven unattended automation, verified consumer security, or confirmed Government-wide availability unless that exact evidence exists.

FINISH: Stop at 2:00 PM. Preserve outputs and unresolved findings in the approved location. Do not delete shared artifacts or disable schedules without owner approval.

TRANSITION: Keep slide 54 available if someone needs a product reference; it is not an additional timed lecture.

## 54 | Sources and delivery boundaries

REFERENCE USE: This slide supports questions and post-session investigation. The linked Microsoft documentation describes product behavior and design considerations. It does not certify the current target tenant's availability, identity path, licensing, or connection configuration.

EXPLAIN: Use the decision guide for Warehouse/Lakehouse tradeoffs, destination documentation for Dataflow behavior, the T-SQL surface and transaction references for SQL assumptions, and the Direct Lake overview for model-mode investigation. Record the behavior and evidence observed in the actual environment.

ASK IF NEEDED: "Which specific capability or path do we need to verify?" Narrow the question to the item, source/destination, mode, identity role, operation, and expected result before assigning follow-up. A general link is not a substitute for that test.

EXECUTION BOUNDARY: Teaching-slide SQL/DAX may be excerpts. Use the complete packaged SQL files in the documented order and create DAX measures separately. The six full lessons remain embedded in divider reference notes.

HANDOFF: Share approved artifact locations and the owned findings/action record. Keep credentials and sensitive diagnostics out of customer-facing evidence. Do not extend the scheduled session to read this reference list aloud.
