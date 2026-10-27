# Contoso Fabric Session 3 and Follow-Up Upskilling Plan

**Status:** Private working document  
**Prepared:** October 26, 2026  
**Purpose:** Consolidate the Contoso Fabric training discussions and provide a structured foundation for building Session 3 and follow-up lessons.

## Executive summary

Contoso does not need another general Fabric introduction. The discussions show a mature Power BI and SQL audience moving toward a repeatable Fabric delivery model in GCC High.

Session 3 should remain focused on SQL, Power Query, and low-code data engineering. Notebook, Spark, and deeper pro-code material should be delivered as a separate learning track. The two tracks should later reunite around one end-to-end Contoso workload and explicit GCC High production-readiness gates.

The learning progression is:

1. Fabric architecture and OneLake orientation.
2. Hands-on ingestion and reconciliation using a realistic workload.
3. Low-code data engineering and operationalization.
4. Separate Warehouse/SQL and notebook/Spark engineering tracks.
5. Semantic-model and direct-consumption patterns.
6. End-to-end capstone.
7. GCC High governance and production readiness.

## Audience baseline

### Power BI, SQL, and Power Query practitioners

This is the strongest established cohort. Participants already have experience with:

- Power BI reports and semantic models.
- SQL and relational data concepts.
- Power Query and Dataflow-style transformation.
- Gateways and controlled data access.
- Initial Fabric workspaces, Lakehouse concepts, and OneLake.
- Data loading, normalization, and reconciliation.
- Basic bronze, silver, and gold thinking.

Remaining needs include:

- Confidently choosing Warehouse versus Lakehouse.
- Stored procedures and advanced Warehouse engineering.
- Repeatable full and incremental load patterns.
- Dataflow Gen2 scheduling and orchestration.
- Semantic-model, Direct Lake, and direct SQL consumption choices.
- Monitoring, lifecycle, ownership, and support practices.

### Notebook, Spark, and pro-code practitioners

Contoso identified a separate audience interested in:

- Notebook development.
- Python and PySpark.
- Spark SQL and DataFrames.
- Delta transformation.
- Parameters and orchestration.
- Data-quality checks.
- Reusable engineering patterns.

This audience should not be combined with the low-code Session 3 cohort. The goal is not to teach everyone Python; it is to make a selected engineering cohort productive with notebooks while helping the broader group understand when notebooks add value.

### Administrators and technical leads

Administrators and architects need:

- Controlled Fabric onboarding.
- Workspace roles and artifact permissions.
- Identity, network, security, and compliance decisions.
- Accurate GCC High capability mapping.
- Workload-selection and architecture decision criteria.
- Monitoring, support, lifecycle, and production-readiness practices.

## Discussion chronology

### September 9-11: initial train-the-trainer request

The original request was a one-day remote Fabric introduction. Contoso had recently received Fabric in GCC High and wanted to train the trainers who would later enable others. The expected audience was technical and included administrators.

### September 15: Fabric upskilling scoping session

The first transcribed scoping discussion established requirements that continued to shape Sessions 1-3:

- Training must be specific to GCC High, not a commercial Fabric tour.
- Start from Contoso's established Power BI estate.
- Prioritize platform, security, governance, OneLake, data engineering, and Dataflow Gen2.
- Use governed shared semantic models as part of the migration direction.
- Keep Fabric access controlled during early enablement.
- Revalidate Government capabilities instead of assuming commercial parity.
- Prefer focused sessions over a generic full-day class.

Ed's stated priority order was:

1. Platform, security, and governance.
2. Fabric introduction.
3. OneLake and data engineering.
4. Dataflow Gen2 and pipelines.

Purview integration in GCC High was also identified for verification.

### September 17-25: use-case-led program design

Internal discussions shifted the engagement away from a generic one-day delivery. The agreed approach was to begin with actual Contoso workloads, map them to capabilities verified in Fabric Government, and decide later sessions based on customer value and product maturity.

The resulting workshop framework covered:

- Architecture and readiness.
- Governance and security.
- Workload planning.
- Pilot validation.
- Operational readiness.
- Optional workload deep dives.

### September 25: second scoping discussion

Contoso reaffirmed the following priorities:

- Fabric architecture.
- Security and governance.
- OneLake and data engineering.
- Integration and orchestration.

Basic Power BI administration was explicitly unnecessary. Accurate Government capability mapping was a prerequisite for some training choices. Contoso also reported Org Apps and Gen2-related issues that required engineering follow-up.

The delivery model became a focused three-hour session followed by additional content selected from the results.

### September 29-October 1: workload and sequence selected

Contoso proposed:

1. Approximately 40 minutes on Fabric architecture and OneLake.
2. Approximately two hours of hands-on work in its tenant.
3. A later block for tenant enablement, identity, licensing, and workspace access.
4. A later block for security, networking, compliance, and governance.

The selected workload compared differently structured files from two systems:

- Files stored in SharePoint.
- Loaded into separate tables.
- Normalized and compared on key fields.
- Used to identify migration and reconciliation patterns.

Contoso asked that limitations encountered during the lab be recorded as formal GCC High findings.

### October 2: Session 1

Session 1 moved the group from awareness into hands-on Fabric work. It covered:

- Fabric and OneLake architecture.
- Capacity concepts.
- Workspaces, roles, and artifact boundaries.
- Lakehouse concepts.
- Data loading.
- Transformation and normalization.
- Bronze, silver, and gold patterns.
- Initial notebook exposure.

Important lesson: lab readiness matters. The intended customer data contained employee information and could not simply be reused. Workspace access also prevented some artifact creation. Future sessions require sanitized data and a permissions preflight.

### October 5-6: Session 2 and Session 3 planning

The follow-up workload was reframed as a working MVP:

`SharePoint -> Dataflow Gen2 -> Warehouse/Lakehouse -> T-SQL reconciliation -> repeatable refresh -> semantic model -> Power BI`

Session 3 was defined as a broader low-code data-engineering module for SQL and Power Query practitioners.

Testing confirmed that SharePoint ingestion through Dataflow Gen2 worked in the Government tenant. Dataflow Gen2 orchestration through pipelines exposed an authentication or permissions issue, so direct Dataflow scheduling was used as the interim approach.

### October 6: low-code and pro-code tracks separated

Contoso accepted the low-code framing for Power BI and SQL practitioners but identified a second audience interested in notebooks, Spark, and pipelines.

The resulting direction was:

- Keep Session 3 focused on low-code data engineering.
- Create a separate Session 4 for the pro-code audience.
- Document GCC High limitations found during labs.

### October 12: capability-tracking discussion

The Contoso implementation was used as field evidence in an internal Fabric capability discussion. SharePoint-to-Dataflow Gen2 ingestion worked, but pipeline orchestration of Dataflow Gen2 exposed an authentication issue. A workaround existed, but the product issue remained open.

### October 16: Session 2

Session 2 was the technical pivot point for Session 3. The group worked through:

- Repeatable SharePoint ingestion using Dataflow Gen2.
- Warehouse as the default for the SQL-oriented workload.
- Silver normalization and Gold reconciliation output.
- Direct Lake semantic modeling and Power BI reporting.
- Lakehouse versus Warehouse tradeoffs.
- Semantic-model sharing.
- Pipeline orchestration attempts.
- Storage and capacity questions.
- GCC High authentication and connection failures.

The team demonstrated that the reconciliation workload could remain SQL-first because the participants were stronger in SQL and the workload did not require a separate notebook tier.

A specific gap also surfaced: the team was comfortable with SQL but not necessarily stored procedures.

Follow-ups included:

- Continue and validate the repeatable Dataflow Gen2 pattern.
- Complete the Warehouse landing and reconciliation logic.
- Retry pipeline and stored-procedure orchestration.
- Follow up on authentication, gateways, and Government-specific behavior.
- Continue developing the architecture into Session 3.

### October 16: recording access issue

Contoso did not reliably receive the prior recordings despite repeated sharing attempts. Training continuity should not depend solely on externally shared recordings. Every future session should produce a portable runbook, reference architecture, and lab guide.

### October 17-21: Session 3 confirmed

The Job 2 training plan reframed the engagement as architecture-and-delivery enablement tied to a real workload rather than generic product training.

Ed confirmed that the proposed Session 3 agenda looked like a good start. The accepted direction was a three-hour low-code session for SQL and Power Query practitioners.

### October 28: scheduled Session 3

**Title:** Contoso | Fabric Training Session 3: Low-code Fabric Data Engineering  
**Time:** 11:00 AM-2:00 PM ET  
**Lead:** Brandon Campbell

The calendar agenda includes:

- Lakehouse versus Warehouse.
- Dataflow Gen2, pipelines, and copy jobs.
- Bronze, silver, and gold patterns.
- T-SQL curation and reconciliation.
- Semantic models and governed Power BI consumption.
- Scheduling, monitoring, workspace roles, naming, and lifecycle.
- Notebooks only where SQL or Power Query is insufficient.

An accepted calendar commitment still overlaps the final 30 minutes, from 1:30-2:00 PM ET.

## Session 3 lesson blueprint

### Learning outcomes

By the end of Session 3, participants should be able to:

1. Choose a Warehouse or Lakehouse based on workload characteristics.
2. Explain where Dataflow Gen2, pipelines, copy jobs, SQL, and notebooks fit.
3. Implement a repeatable source-to-curated-data pattern.
4. Apply bronze, silver, and gold responsibilities pragmatically.
5. Build curated tables, views, and reconciliation logic using T-SQL.
6. Select a governed Power BI consumption path.
7. Identify scheduling, monitoring, naming, ownership, and lifecycle requirements.
8. Separate learner gaps from GCC High product or environment limitations.

### Recommended three-hour flow

#### Module 1: Architecture decision framework - 25 minutes

- Review the Session 2 workload.
- Compare Warehouse and Lakehouse.
- Select the simplest justified architecture.
- Record the decision and rejected alternatives.

**Output:** Completed architecture decision record.

#### Module 2: Repeatable ingestion - 35 minutes

- Review SharePoint source characteristics.
- Build or inspect the Dataflow Gen2 ingestion.
- Discuss full versus incremental loading.
- Compare direct scheduling with pipeline orchestration.

**Output:** Repeatable ingestion pattern with its scheduling method documented.

#### Module 3: Curated SQL engineering - 50 minutes

- Land source-aligned tables.
- Normalize mismatched structures.
- Build curated tables and views.
- Introduce stored-procedure patterns.
- Produce reconciliation output with exception handling.

**Output:** Curated Warehouse objects and reconciliation results.

#### Module 4: Consumption architecture - 35 minutes

- Connect curated data to a semantic model.
- Compare reusable semantic models, Direct Lake, and direct SQL consumption.
- Identify governance and reuse implications.

**Output:** Selected consumption path with rationale.

#### Module 5: Operations and GCC High findings - 25 minutes

- Scheduling and monitoring.
- Workspace roles and artifact ownership.
- Naming and lifecycle.
- Support ownership.
- GCC High findings versus learner gaps.

**Output:** Initial operations checklist and findings register.

#### Module 6: Exit review - 10 minutes

- Confirm artifacts created.
- Review unresolved questions.
- Assign owners.
- Confirm which learners enter the low-code or pro-code follow-up track.

## Follow-up upskilling plan

### Session 4A: Fabric Warehouse engineering for SQL teams

**Audience:** SQL and BI developers

**Topics:**

- Fact and dimension design.
- T-SQL transformation patterns.
- Stored procedures.
- Idempotent full and incremental loads.
- Reconciliation and exception handling.
- Data-quality validation.
- Scheduling and operational support.

**Hands-on output:** Curated fact and dimension tables plus a repeatable SQL load and reconciliation procedure.

### Session 4B: Notebooks for Fabric engineers

**Audience:** Selected developers and data engineers

**Topics:**

- Notebook anatomy.
- Python and PySpark fundamentals.
- Mapping SQL operations to DataFrames and Spark SQL.
- Delta read, transform, and write patterns.
- Parameters.
- Data-quality checks.
- Pipeline orchestration.
- Handing curated output to downstream consumers.

**Hands-on output:** A parameterized notebook that validates, transforms, and writes curated Delta data.

### Session 5: Semantic models and direct consumption

**Audience:** SQL/BI developers and architects

**Topics:**

- Reusable semantic models.
- Direct Lake.
- Power BI Desktop using Warehouse or Lakehouse data.
- Direct SQL consumption.
- Governance, reuse, and performance tradeoffs.

**Hands-on output:** The same curated data consumed through a reusable semantic model and a validated direct-consumption route.

### Session 6: end-to-end Contoso capstone

**Audience:** Both technical tracks

**Scenario:**

1. Ingest a sanitized multi-file dataset.
2. Land it in OneLake.
3. Transform one portion using SQL.
4. Transform another portion using a notebook.
5. Publish curated Warehouse or Lakehouse data.
6. Build a reusable semantic-model experience.
7. Build a direct-consumption experience.
8. Document operations and unresolved GCC High findings.

**Hands-on output:** A reusable source-to-report implementation and participant-authored runbook.

### Session 7: GCC High operations and governance

**Audience:** Administrators, architects, operations, and technical leads

**Topics:**

- Persona and access model.
- Workspace roles.
- Identity and gateway dependencies.
- Security and compliance controls.
- Naming and lifecycle.
- Monitoring and support.
- Capacity considerations.
- Pilot-to-production gates.
- GCC High blocker ownership.

**Hands-on output:** Production-readiness, governance, and support checklist.

## Delivery prerequisites

Complete a 30-45 minute readiness gate before every hands-on session:

- Use sanitized or synthetic data, not employee data.
- Validate workspace roles and artifact-creation permissions.
- Validate access to SQL tools, Power BI Desktop, notebooks, pipelines, and Dataflow Gen2.
- Confirm which capabilities function in the target GCC High environment.
- Separate existing support incidents from the training backlog.
- Confirm the source files, lab workspace, capacity, and expected outputs.
- Assign a technical lead, support owner, and artifact owner.

No lesson time should be spent discovering missing workspace permissions.

## GCC High findings practice

Maintain two separate logs:

### Learning log

Track skills or concepts participants still need to develop.

### Environment findings log

Track:

- Reproducible GCC High limitations.
- Authentication and connection failures.
- Missing or partially deployed capabilities.
- Gateway visibility issues.
- Capacity constraints.
- Product defects and support cases.
- Workarounds and their operational impact.

Environment limitations must not be recorded as learner failure.

## Ownership model

Existing responsibilities evidenced in the discussions:

- **Brandon Campbell:** Fabric technical enablement, architecture, examples, GCC High validation, and lesson preparation.
- **Ashlee Teater:** Microsoft engagement coordination and scheduling.
- **Ed Estess and Ken Simpson:** Contoso priorities, participant alignment, and training direction.
- **Alex Birurakis:** Repeatable Dataflow Gen2 implementation and related testing.

Recommended roles for every future lab:

- Microsoft technical lead.
- Contoso technical lead.
- GCC High blocker and support owner.
- Artifact and runbook owner.

## Success measures

Measure outcomes through artifacts and decisions rather than attendance.

The program should produce:

- A named Contoso workload and sponsor.
- A named technical owner and participant cohort.
- An agreed architecture and consumption path.
- An accessible GCC High lab environment.
- A sanitized dataset.
- A repeatable ingestion and transformation pattern.
- Curated Warehouse or Lakehouse data.
- A reusable semantic model.
- A validated direct-consumption route.
- A participant-authored runbook.
- Pilot success criteria and target date.
- Product blockers with engineering or support owners.
- Clear pilot-to-production responsibilities.

The strongest completion test is for participants to repeat the scenario using only the runbook.

## Immediate action checklist

- [ ] Resolve the October 28 conflict from 1:30-2:00 PM ET.
- [ ] Confirm the Session 3 participant list and low-code audience.
- [ ] Validate workspace permissions and artifact-creation access.
- [ ] Prepare sanitized SharePoint source files.
- [ ] Confirm Dataflow Gen2 direct scheduling works.
- [ ] Decide whether pipeline orchestration will be demonstrated or discussed as an open GCC High finding.
- [ ] Prepare the Warehouse-versus-Lakehouse decision worksheet.
- [ ] Prepare starter T-SQL tables, views, stored procedure, and reconciliation logic.
- [ ] Prepare the semantic-model and direct-consumption comparison.
- [ ] Create learning and environment-findings logs.
- [ ] Confirm how Contoso will receive the runbook and session artifacts.
- [ ] Identify the Session 4A and Session 4B cohorts.

## Primary source inventory

- [Contoso | Fabric upskilling scoping session - September 15](https://teams.microsoft.com/l/meeting/details?eventId=AAMkAGU5MzE5YjJlLWEzOTctNGRkOC1hZWY1LWFjNDNjNzg3OWNhMwBGAAAAAAA7MzHWwwHARJKvKXU-SWwyBwCpML5SioqcSoaT5zKI4ihxAAAAAAENAACpML5SioqcSoaT5zKI4ihxAAuknBxeAAA%3d)
- [Contoso | Fabric scoping discussion - meeting 2 - September 25](https://teams.microsoft.com/l/meeting/details?eventId=AAMkAGU5MzE5YjJlLWEzOTctNGRkOC1hZWY1LWFjNDNjNzg3OWNhMwBGAAAAAAA7MzHWwwHARJKvKXU-SWwyBwCpML5SioqcSoaT5zKI4ihxAAAAAAENAACpML5SioqcSoaT5zKI4ihxAAvMOr0uAAA%3d)
- [Contoso | Fabric training overview - October 2](https://teams.microsoft.com/l/meeting/details?eventId=AAMkAGU5MzE5YjJlLWEzOTctNGRkOC1hZWY1LWFjNDNjNzg3OWNhMwBGAAAAAAA7MzHWwwHARJKvKXU-SWwyBwCpML5SioqcSoaT5zKI4ihxAAAAAAENAACpML5SioqcSoaT5zKI4ihxAAwbGqUcAAA%3d)
- [Contoso | Fabric training session 2 - October 16](https://teams.microsoft.com/l/meeting/details?eventId=AAMkAGU5MzE5YjJlLWEzOTctNGRkOC1hZWY1LWFjNDNjNzg3OWNhMwBGAAAAAAA7MzHWwwHARJKvKXU-SWwyBwCpML5SioqcSoaT5zKI4ihxAAAAAAENAACpML5SioqcSoaT5zKI4ihxAAyt_9hoAAA%3d)
- [Contoso Fabric Job 2 Training Plan - October 17](https://microsoft-my.sharepoint.com/personal/brcampb_microsoft_com/_layouts/15/Doc.aspx?sourcedoc=%7B6F3EF205-6337-4C66-9127-FB5211303C20%7D&file=Contoso_Fabric_Job2_Training_Plan_2026-10-17.docx&action=default&mobileredirect=true&DefaultItemOpen=1)
- [Contoso | Fabric Training Session 3 - October 28](https://teams.microsoft.com/l/meeting/details?eventId=AAMkAGU5MzE5YjJlLWEzOTctNGRkOC1hZWY1LWFjNDNjNzg3OWNhMwBGAAAAAAA7MzHWwwHARJKvKXU-SWwyBwCpML5SioqcSoaT5zKI4ihxAAAAAAENAACpML5SioqcSoaT5zKI4ihxAAznfrYfAAA%3d)

## Evidence boundary

The chronology and current Session 3 direction are grounded in the discovered Microsoft 365 sources. Sessions 4A-7, the detailed lesson timings, the two-log operating practice, and the readiness-gate format are recommendations derived from that evidence and are not yet final Contoso commitments.
