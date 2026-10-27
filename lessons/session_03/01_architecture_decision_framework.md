# Lesson 1: Architecture decision framework

**Session 3 | October 28, 2026 | 25 minutes**  
**Blueprint:** [Module 1](../../session_3_blueprint.md#module-1-architecture-decision-framework---25-minutes)  
**Lesson output:** A completed architecture decision record.

## What this lesson teaches

A good architecture is not the one that contains the most Fabric components. It is the one that meets the business requirement with a clear transformation path, appropriate controls, and an operating model the team can sustain.

In this lesson, we will revisit the reconciliation workload from Session 2, compare Warehouse and Lakehouse, and make a deliberate starting-point decision. The objective is not to memorize a product comparison. It is to learn how to turn a business requirement into a defensible technical choice.

Use approximately five minutes to revisit the workload, eight minutes to compare the platforms, seven minutes to select an architecture, and five minutes to record the decision.

## 1. Start with the business question

Our workload begins with two systems that describe overlapping business records. Each system produces a file, and those files are stored in SharePoint. Their column names and representations differ. One system may call a field `RecordId`, while the other calls it `Reference`. An identifier might contain surrounding spaces or inconsistent capitalization. An amount might be a valid number in one file and an invalid text value in the other.

The business question is straightforward:

> Do the two extracts describe the same records, amounts, and statuses? If not, which differences require investigation?

This is more precise than saying, "We need to move some files into Fabric." Moving files is an implementation activity. Reconciliation is the business outcome.

The solution must preserve source evidence, make comparable values consistent, identify differences, and present exceptions to an approved audience. It must also repeat successfully when the next extract arrives. A one-time result that depends on someone manually repairing every refresh does not yet satisfy the operating requirement.

Before selecting a platform, identify the **grain** of the output. Grain describes what one row represents. For this workload, one published reconciliation row represents one normalized business record ID in one comparison of two complete source snapshots. If a source contains duplicate IDs, the solution must identify that ambiguity rather than accidentally multiplying rows during a join.

The intended consumer is a Power BI audience that needs a trusted summary and enough detail to investigate exceptions. SQL practitioners also need a way to inspect the underlying curated data. Those consumption needs influence how we publish the output, but they do not require every possible Fabric engineering tool.

## 2. Understand what Warehouse and Lakehouse share

Warehouse and Lakehouse are both Fabric analytical data stores built on OneLake and open Delta storage. Choosing Warehouse does not mean choosing something outside OneLake. Choosing Lakehouse does not mean giving up relational queries.

The important differences concern the development experience, supported write operations, data organization, and the team's transformation approach.

A **Warehouse** is a strong starting point when the work is primarily relational and the team intends to create and modify analytical tables using T-SQL. It supports Warehouse tables, views, stored procedures, and supported data manipulation operations. It also supports transactions that can group related SQL changes into a single commit or rollback.

A **Lakehouse** is a strong starting point when the workload needs file-oriented engineering, structured and unstructured data together, or Spark-based transformation. Its SQL analytics endpoint lets SQL users query exposed Delta tables and define supported SQL objects. However, that endpoint does not turn Lakehouse tables into tables that can be inserted, updated, or deleted through T-SQL.

This distinction is especially important for SQL developers. Seeing a SQL query editor does not establish that the underlying item supports the same write path as a Warehouse.

| Question | Warehouse consideration | Lakehouse consideration |
| --- | --- | --- |
| How will we develop transformations? | Primarily T-SQL | Often Spark, notebooks, or other supported Lakehouse writers |
| What data must we handle? | Relational analytical tables | Files, Delta tables, and potentially unstructured data |
| Do we need SQL-managed table writes? | A natural fit | Not through the Lakehouse SQL analytics endpoint |
| Do related SQL writes need a transaction? | Supports multi-table SQL transactions | Do not assume the same cross-table SQL transaction model |
| What can this team operate today? | Builds on SQL engineering skills | May require additional engineering skills and support practices |

Neither product is a complete replacement for every SQL Server capability. Validate required T-SQL features rather than assuming that a familiar syntax or tool guarantees compatibility.

## 3. Choose the simplest justified architecture

For the current workload, the strongest starting point is a Warehouse-centered design:

```text
SharePoint extracts
        |
        v
Dataflow Gen2
        |
        v
Warehouse: source-aligned landing tables
        |
        v
T-SQL normalization and reconciliation
        |
        v
Curated reconciliation table
        |
        v
Shared semantic model and Power BI
```

This recommendation follows the requirements. The files are tabular. The core transformation is a relational comparison. The audience already knows SQL and Power Query. Nothing in the current requirement demands Spark or a separate notebook tier.

Adding a Lakehouse solely because Fabric has a Lakehouse experience would introduce another component without solving a demonstrated problem. Conversely, if the workload later includes large collections of documents, custom Python processing, or an established Spark engineering pipeline, Lakehouse may become appropriate. Architecture decisions should be revisited when their assumptions change.

The same reasoning applies to notebooks. A notebook is an engineering tool, not a maturity badge. Use one when its capabilities solve a requirement that the chosen SQL and Power Query approach does not address well. Do not introduce Python merely to recreate a straightforward SQL join for an audience that will support the solution in SQL.

### Where bronze, silver, and gold fit

Bronze, silver, and gold describe responsibilities in the data flow.

**Bronze** preserves source-aligned evidence. We should be able to determine what each source supplied, including duplicates and invalid values.

**Silver** makes values consistent and evaluates quality. Here we align column names, normalize identifiers, convert amounts deliberately, and identify records that cannot be compared safely.

**Gold** publishes the business-facing result. In this workload, that is an explainable reconciliation classification for each business key, along with the values needed to investigate an exception.

These responsibilities do not automatically require three workspaces, three capacities, or three physical copies of every table. In the training implementation, separate schemas inside one Warehouse make the responsibilities visible. Silver can use views where materialization is unnecessary. Production boundaries should follow security, lifecycle, performance, and ownership requirements.

## 4. Record the decision and the alternatives

An architecture decision record is a short explanation of why an option was selected under specific conditions. It is useful precisely because the conditions may change.

A useful decision is more specific than "Use Warehouse." It names the workload, the required operations, the assumptions, and the alternatives considered.

### Worked decision record

| Field | Example decision |
| --- | --- |
| Business outcome | Compare two source extracts and expose migration/reconciliation exceptions |
| Data and grain | Structured snapshots; one result per normalized record ID per comparison |
| Selected starting point | Dataflow Gen2 ingestion into a Fabric Warehouse |
| Transformation approach | Power Query for ingestion shaping; T-SQL for normalization, quality rules, and reconciliation |
| Consumption approach | Curated table exposed through a shared semantic model; approved SQL access where needed |
| Reason | Meets the workload using the team's existing SQL and Power Query skills |
| Alternative considered | Lakehouse with notebook-based transformation |
| Why not selected now | No current file/Spark requirement justifies a second engineering path |
| Assumptions | Approved source access, functioning destination connections, and verified tenant capabilities |
| Revisit when | Data types, transformation requirements, scale characteristics, security boundaries, or team ownership change |

Notice that an unverified capability is an assumption to test, not a fact to hide. The engagement's prior experience is useful evidence, but it does not establish that every feature or connection works today.

## 5. Apply the lesson

Write a decision record for the reconciliation workload using the fields above. Then change one assumption: the source now includes documents requiring custom Python extraction before comparison. Explain whether that change affects ingestion, transformation, storage, or all three.

A strong answer does not automatically replace the entire solution. It identifies where the new requirement belongs and preserves the parts that still meet their purpose.

### Check your understanding

**Why is Warehouse a reasonable starting point here?** The workload is relational, requires supported SQL writes, and is operated by a SQL/Power Query-oriented team.

**Does Warehouse bypass OneLake?** No. Warehouse also uses OneLake and Delta storage.

**Can we write Lakehouse table data through its SQL analytics endpoint?** No. Query access and supported SQL object definitions are not the same as T-SQL table-data writes.

**Does a medallion pattern require three workspaces?** No. The layers identify responsibilities; physical separation requires its own justification.

## Lesson conclusion

We have selected a starting architecture based on a business question, output grain, required operations, and team capability. The next lesson turns that architecture into a repeatable ingestion contract.

**Next:** [Lesson 2: Repeatable ingestion](02_repeatable_ingestion.md)

**Product references:** [Warehouse/Lakehouse decision guide](https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-lakehouse-warehouse) and [T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area). General product documentation does not confirm availability in the target GCC High tenant.
