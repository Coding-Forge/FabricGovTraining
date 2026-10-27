# Session 3 lesson blueprint

## Learning outcomes

By the end of Session 3, participants should be able to:

1. Choose a Warehouse or Lakehouse based on workload characteristics.
2. Explain where Dataflow Gen2, pipelines, copy jobs, SQL, and notebooks fit.
3. Implement a repeatable source-to-curated-data pattern.
4. Apply bronze, silver, and gold responsibilities pragmatically.
5. Build curated tables, views, and reconciliation logic using T-SQL.
6. Select a governed Power BI consumption path.
7. Identify scheduling, monitoring, naming, ownership, and lifecycle requirements.
8. Separate learner gaps from GCC High product or environment limitations.

## Recommended three-hour flow

### Module 1: Architecture decision framework - 25 minutes

- Review the Session 2 workload.
- Compare Warehouse and Lakehouse.
- Select the simplest justified architecture.
- Record the decision and rejected alternatives.

**Output:** Completed architecture decision record.

### Module 2: Repeatable ingestion - 35 minutes

- Review SharePoint source characteristics.
- Build or inspect the Dataflow Gen2 ingestion.
- Discuss full versus incremental loading.
- Compare direct scheduling with pipeline orchestration.

**Output:** Repeatable ingestion pattern with its scheduling method documented.

### Module 3: Curated SQL engineering - 50 minutes

- Land source-aligned tables.
- Normalize mismatched structures.
- Build curated tables and views.
- Introduce stored-procedure patterns.
- Produce reconciliation output with exception handling.

**Output:** Curated Warehouse objects and reconciliation results.

### Module 4: Consumption architecture - 35 minutes

- Connect curated data to a semantic model.
- Compare reusable semantic models, Direct Lake, and direct SQL consumption.
- Identify governance and reuse implications.

**Output:** Selected consumption path with rationale.

### Module 5: Operations and GCC High findings - 25 minutes

- Scheduling and monitoring.
- Workspace roles and artifact ownership.
- Naming and lifecycle.
- Support ownership.
- GCC High findings versus learner gaps.

**Output:** Initial operations checklist and findings register.

### Module 6: Exit review - 10 minutes

- Confirm artifacts created.
- Review unresolved questions.
- Assign owners.
- Confirm which learners enter the low-code or pro-code follow-up track.
