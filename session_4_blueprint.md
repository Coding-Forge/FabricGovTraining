# Session 04 blueprint: Notebooks with Warehouse Gold

**Audience:** SQL/Power Query practitioners moving into Python, PySpark, and file-based data engineering  
**Status:** Proposed content and worked examples; delivery date and duration are not yet assigned  
**Scope:** Notebook foundations, exploration/Wrangler, Silver/Warehouse Gold, independent analysis, and Git/VS Code workflows  
**Execution:** Examples require Fabric tenant preflight; they are not a claim of GCC High availability.

This is the current Session 04 direction. It develops the notebook track from the earlier program plan; the advanced Warehouse-only track is not the subject of this session.

**First-time-user path:** [Notebook 101](lessons/session_04/00_notebook_101.md)
and its read-only repair exercise, then the
[realistic notebook lab](lessons/session_04/09_realistic_data_lab.md).
Use the [importable starter/solution notebooks](lessons/session_04/notebooks/README.md)
instead of assembling code from Markdown.
The [two dataset tiers](lessons/session_04/artifacts/data/README.md) separate
small rule-explanation fixtures from the main multi-file analytical workload.

**Mandatory before delivery:** Complete the [customer setup and presenter readiness gate](lessons/session_04/prerequisites.md).
The presenter must check in with the customer **3-5 business days beforehand**
to verify completion and address blockers, then reconfirm on the preceding
business day. Provisioning, permissions, data landing, and the rehearsal are not
delivery-day activities.

## The central teaching point

Session 03 showed why a relational reconciliation workload can stay SQL-first. Session 04 should not recreate that join in Python just to introduce notebooks.

Instead, show where notebook-based engineering is useful: nested/file-oriented inputs, reusable Python libraries, specialized transformations, and distributed event preparation. Keep the Warehouse where it adds value: relational serving, SQL-managed publication, dimensional models, and familiar reporting.

> A notebook is compute and code, not a storage destination. The notebook lands data in a Lakehouse, prepares it with Spark, and hands an explicit table contract to a Warehouse.

## Learning outcomes

Participants should be able to:

1. Explain when a notebook is justified and when Warehouse SQL or Power Query is simpler.
2. Distinguish the notebook, Spark session, Lakehouse Files/Tables, SQL analytics endpoint, and Warehouse.
3. Preserve raw evidence before parsing or cleaning.
4. Flatten nested JSON and apply explicit type, key, and quality rules.
5. Normalize events, quarantine ambiguous duplicates, and aggregate accepted readings.
6. Publish only verified outputs to Warehouse staging, then promote them to Gold.
7. Explain rerun, failure, identity, and freshness boundaries without assuming end-to-end atomicity.
8. Profile missing, invalid, duplicate, and out-of-range values without confusing samples with full-data evidence.
9. Use notebook charts to answer specific questions and label their scope, grain, and denominator.
10. Use Data Wrangler to generate/review transformations, then validate the exported PySpark on the intended dataset.
11. Select reusable business/context/lineage columns for Silver and distinguish them from evidence-only fields and temporary helpers.
12. Locate common PySpark APIs by engineering task and explain when an operation is appropriate, costly, or unsafe for the contract.
13. Navigate cells/session controls, explain stale execution state, and distinguish saving a notebook from persisting data.
14. Recognize essential Python and Spark expressions, reproduce equivalent PySpark/Spark SQL results, and repair variable/column/path errors.
15. Review write scope before Run all, use the training approval controls, and prove a new table survives a session restart without blindly appending/overwriting.
16. Use API help, distinguish logical tables from physical files, diagnose path/identity errors, and answer a new question independently with scoped quality evidence.
17. Review/version a notebook through a private practice Git branch and distinguish workspace changes, commits, pull requests, sync, and execution.
18. If connected tooling is supported, author locally in VS Code while executing on verified Fabric compute, and distinguish Save, Publish, Update Notebook, and Commit to Git.

## Proposed teaching sequence

| Module | Teaching focus | Demonstration or exercise | Output |
| --- | --- | --- | --- |
| 1. Choose the engineering tool | Requirements, not product preference | Compare simple reconciliation, nested orders, telemetry, and library-dependent enrichment | Decision and rejected alternative |
| 2. Notebook foundations | UI, Python/PySpark, state, Spark SQL, safe persistence, debugging | Notebook 101 starter: three small tasks, restart/read-back demonstration, and three-error read-only repair; then main lab sections 1-2 | Explained execution model, repaired notebook, approved target scope, and device Bronze |
| 3. Explore and visualize | Missingness vs. validity, keys, distributions, sample scope | Main lab section 3: profile 201,579 device rows before cleaning | Full-batch profile and a justified cleaning decision |
| 4. Data Wrangler | Sample, preview, export, review, run, validate | Main lab section 3, with [UI/export guidance](lessons/session_04/06_data_wrangler.md) | Reviewed recipe applied to the full batch; raw evidence unchanged |
| 5. Clean nested JSON/events | Explicit schema, array expansion, UTC, key/value rules, quarantine | Main lab sections 4 and 7-8; use micro fixtures first if helpful | 194,545 accepted events; 14,391 accepted order lines; reviewed quarantine |
| 6. Design Silver columns | Keys, measures, context, lineage, evidence-only fields | Main lab Silver projections and [column-selection reasoning](lessons/session_04/07_silver_column_design.md) | Explicit context/lineage allowlists and documented exclusions |
| 7. Shape and inspect Gold | Change of grain, counts, daily metrics, chart interpretation | Main lab sections 5-6: daily preparation and diagnostic charts | 700 device/day summaries; fourteen-day patterns and labeled coverage |
| 8. Warehouse Gold | Copy/connector boundaries, staging, validation, transactional publication | Main lab section 9 and its scenario-specific SQL | Queryable accepted order lines and device/day Gold; date/region/category SQL |
| 9. Operate and explain | Success gates, retries, source lineage, permissions, ownership | Repeat one batch; discuss a failed handoff | Evidence-backed run record and next actions |
| 10. Analyze independently | New question, accepted-only metrics, source populations, coverage caveats | [Read-only challenge](lessons/session_04/10_independent_challenge.md) for D032 on two different dates | Reproducible summary and defensible interpretation |
| 11. Version and review | Git concepts, native notebook source, commit/PR, both sync directions | [Git practice](lessons/session_04/11_git_and_fabric_notebooks.md) with a read-only notebook copy in a private practice repo/workspace | Reviewed change and actual commit/PR/sync evidence |
| 12. Connected authoring, if supported | Local editor versus remote compute; separate publishing and Git | [VS Code exercise](lessons/session_04/12_vscode_connected_authoring.md) using Microsoft Fabric Runtime | Remote run evidence, published edit, reconciled incoming change |

These are content modules, not a confirmed timed agenda. The primary lab covers both scenarios. Use devices as the participant path and orders as a presenter demonstration if Spark startup, transfer, or participant experience makes both impractical.

For first-time users, complete the Notebook 101 warm-up and repair exercise
before the realistic pipeline. The three starter practice cells in each
warm-up/main notebook are labeled intentional stops, not unexplained failures.
Use completed solutions for presenter rehearsal/recovery; require learners to
explain their own work. Do not trade away execution-state/debugging practice
to cover advanced tuning APIs. The use-case discussion can precede the warm-up.
Keep the [survival guide](lessons/session_04/notebook_survival_guide.md) alongside
the exercises. Use the independent challenge before showing its solution.
Git is a follow-on workflow module; VS Code is a separately preflighted optional
module, not a prerequisite for the browser-based notebook lessons. Agree their
delivery allocation rather than squeezing them into an unconfirmed agenda.

Follow the main lab's section order, pausing for exploration/Wrangler before cleaning.
Lessons 02-07 retain the tiny-fixture path for explaining individual rules:
four orders and nine events, with different schemas, batch/table names, and SQL
guards. Do not mix their counts or publication scripts with the main lab.
Lesson filenames are references, not an instruction to postpone exploration until
after publication.

## Target architecture

```text
ADLS Gen2: approved, versioned CSV/JSON source files
  -> Verified pipeline file copy (prepared before delivery)
  -> Lakehouse Files: retained raw, batch-specific input
  -> Notebook: persist Bronze evidence, parse, flatten, normalize
  -> Lakehouse Delta: accepted Silver + quarantine + transfer tables
  -> Verified copy activity (or a verified Warehouse Spark connector)
  -> Warehouse staging: explicit, flat column contract
  -> Warehouse SQL: validate and transactionally publish Gold
  -> Shared semantic model / Power BI / approved SQL consumers
```

Default the lesson to a copy activity from a Lakehouse table into an existing Warehouse staging table, followed by separate SQL publication. Do not copy directly over the live Gold table.

Direct Spark-to-Warehouse writing is an optional alternative, not a prerequisite. The current Microsoft documentation specifies Runtime 2.0 for writes and interactive Entra user authentication; service principal authentication is not supported by that connector. Verify the actual runtime, execution identity, network path, and Government availability.

## Materials

- [Mandatory pre-delivery setup and customer check-in](lessons/session_04/prerequisites.md)
- [Notebook 101 warm-up, restart demonstration, and repair exercise](lessons/session_04/00_notebook_101.md)
- [Eight importable starter/solution notebooks and live-testing sequence](lessons/session_04/notebooks/README.md)
- [Notebook survival guide](lessons/session_04/notebook_survival_guide.md)
- [Independent read-only challenge and rubric](lessons/session_04/10_independent_challenge.md)
- [Git versioning and review lesson](lessons/session_04/11_git_and_fabric_notebooks.md)
- [VS Code connected-authoring lesson](lessons/session_04/12_vscode_connected_authoring.md)
- [Primary lab: Realistic multi-file notebook workflow](lessons/session_04/09_realistic_data_lab.md)
- [Dataset tiers, exact outcomes, and regeneration](lessons/session_04/artifacts/data/README.md)
- [Use cases and tool decision guide](lessons/session_04/01_notebook_use_cases.md)
- [Micro example 1: Nested order JSON](lessons/session_04/02_nested_json_orders.md)
- [Micro example 2: Device telemetry](lessons/session_04/03_device_telemetry.md)
- [Handoff concepts and micro-fixture Warehouse publication](lessons/session_04/04_warehouse_gold.md)
- [Micro-fixture exploration and notebook visualization](lessons/session_04/05_exploration_and_visualization.md)
- [Data Wrangler demonstration and code review](lessons/session_04/06_data_wrangler.md)
- [Silver column decisions and Gold processing](lessons/session_04/07_silver_column_design.md)
- [Categorized PySpark function field guide](lessons/session_04/08_pyspark_function_reference.md)
- [Synthetic order input](lessons/session_04/artifacts/data/orders.jsonl)
- [Synthetic device input](lessons/session_04/artifacts/data/device_readings.csv)
- [Main-lab source files, expected tables, and manifest](lessons/session_04/artifacts/data/scenario/)
- [Deterministic main-lab dataset generator](lessons/session_04/artifacts/generate_datasets.py)
- [Notebook asset builder](lessons/session_04/artifacts/build_notebooks.py)
- [Main-lab Warehouse setup](lessons/session_04/artifacts/sql/scenario_warehouse_setup.sql)
- [Main-lab order publication](lessons/session_04/artifacts/sql/scenario_publish_orders.sql)
- [Main-lab device publication](lessons/session_04/artifacts/sql/scenario_publish_devices.sql)
- [Offline example checks](lessons/session_04/artifacts/validate_examples.py)

The package now includes eight output-free `.ipynb` files: starter/solution pairs
for warm-up, read-only repair, the realistic lab, and independent analysis. The Markdown handouts
remain the source of the worked warm-up/main cells. The micro examples use
separate notebooks as stated in those lessons. A Session 04 presentation and
timed delivery guide are not yet provided.

## Preflight and completion evidence

The [prerequisite guide](lessons/session_04/prerequisites.md) defines customer
owners, ADLS upload/copy settings, answer-key placement, rehearsal evidence, and
the mandatory 3-5-business-day presenter check-in. Complete its readiness gate
before the delivery day; the checks below are not permission to defer setup
until class.

Use an isolated training Lakehouse and Warehouse per participant/pair. Confirm Spark startup/runtime, the attached default Lakehouse, schema/table naming, supported copy connections/staging, Warehouse SQL execution, and the intended identity for each hop. Preflight Data Wrangler and notebook chart controls separately; an unavailable UI remains a labeled blocked demonstration.

No example downloads public data, calls an external AI service, or embeds credentials. Core parsing/cleaning uses built-in Spark functions; optional code-based charts use pandas and Matplotlib from the approved runtime. No notebook installs packages. API authentication, pagination, retries, and secret management are separate production concerns, not proven by reading these fixtures.

Observe raw counts, quarantine reasons, accepted rows, transfer counts, exact Gold results, an unchanged rerun, and a blocked-publication scenario. Label participant execution, presenter demonstration, prepared evidence, and blocked steps separately.

Also retain the profile, labeled charts, reviewed Wrangler recipe, and a column decision explaining what was included in Silver, what remained evidence-only, and how the Gold grain changed.

For beginners, retain the three warm-up answers, explained variable/column/path
repairs, and safe persistence/restart evidence (or label the optional write
skipped). Check that the imported notebook is PySpark with the correct default
Lakehouse; the portable files do not bind customer resources. Warm-up writes
are off by default; main-lab variants stop at their approval gate by default.
Retain the independent challenge's two daily results and quality/coverage
interpretation. For Git/VS Code, preflight the private practice repo, workspace
connection, approved extensions, actual cloud sign-in, remote runtime, and
publish/sync operations; record unsupported actions as blocked, not successful.
Use the [first real-workspace test sequence](lessons/session_04/notebooks/README.md#first-real-workspace-test)
to distinguish local checks from actual tenant evidence.

From the repository root, run `python lessons/session_04/artifacts/validate_examples.py`
for independent acceptance/expected-row calculations for both tiers, full-data
profiles, deterministic dataset/notebook regeneration, hashes, Python cell
syntax, starter/solution and write-control checks, column/SQL contracts, and
local links. It does not execute Fabric imports, the PySpark transformations,
Data Wrangler UI, Warehouse SQL, or transfer path.
