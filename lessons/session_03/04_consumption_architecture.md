# Lesson 4: Consumption architecture

**Session 3 | October 28, 2026 | 35 minutes**  
**Blueprint:** [Module 4](../../session_3_blueprint.md#module-4-consumption-architecture---35-minutes)  
**Lesson output:** A selected consumption path with a documented rationale.

## What this lesson teaches

Producing a correct table does not automatically produce a governed analytical experience. Consumers still need agreed definitions, appropriate access, understandable measures, and confidence that they are looking at the intended publication.

This lesson connects the curated reconciliation output to Power BI. We will distinguish the role of a semantic model from the storage/query mode it uses, compare model-based reporting with direct SQL consumption, and decide which responsibilities belong upstream versus in the model.

Use approximately eight minutes for the conceptual distinctions, fifteen for the worked model/report, seven for governance and freshness, and five for the consumption decision.

## 1. Separate business semantics from data access

The Gold reconciliation table has already answered a business question at a defined grain: one row per normalized record ID for the current comparison. It exposes the amounts, statuses, source row counts, and reconciliation classification.

A **semantic model** adds the reusable analytical contract around that data. It defines measures, relationships where needed, meaningful names, formatting, and model-level access rules. Reports connect to the model to ask analytical questions without each report author inventing a new interpretation of the underlying columns.

For example, the organization needs a consistent definition of an exception. In this lesson:

> An exception is any published reconciliation record whose classification is not `MATCH`.

That definition includes duplicate keys and invalid amounts. If one report excludes them while another includes them, the two reports can show different exception rates even though both read the same Gold table.

The semantic model is where reusable reporting measures can express that agreed definition. The underlying record-level classification remains in Gold because it is also needed by SQL consumers and other downstream tools.

This division avoids two opposite mistakes. We should not reimplement the reconciliation algorithm independently in every report, but we also should not move every display-oriented measure into a physical SQL table.

## 2. Understand the storage/query choices

A shared semantic model and Direct Lake are not competing architectures. A shared model can use Direct Lake tables. It can also use Import or DirectQuery, subject to the model design and available capabilities.

The choice of storage/query mode describes how table data is made available to the model's query engine. The choice to share a model describes how business definitions are reused.

| Mode or route | How to understand it | Important operating consideration |
| --- | --- | --- |
| Import | Data is loaded into the semantic model's imported storage | Source changes require a successful model refresh before the imported data changes |
| DirectQuery | Model queries are translated into queries against the source | Source performance, connection behavior, and query-time permissions matter |
| Direct Lake | Model tables use supported Delta data in OneLake, loading needed data into memory | Model framing/freshness, supported source objects, capacity, and identity behavior still matter |
| Direct SQL | A SQL client queries the Warehouse through SQL access | SQL permissions and curated definitions must be governed independently of report access |

Direct Lake avoids the conventional full import of the analytical dataset into model storage. It does not mean that no data enters memory, that every source object is supported, or that freshness no longer needs attention.

Current general documentation distinguishes **Direct Lake on OneLake** from **Direct Lake on SQL**. Their source discovery, security interactions, and fallback behavior differ. Direct Lake on SQL can fall back to DirectQuery in supported circumstances, including SQL views, depending on its behavior settings. Direct Lake on OneLake does not use that DirectQuery fallback path.

For this lesson, use the physical `gold.reconciliation` table and inspect the actual mode in the prepared model. Do not label a model "Direct Lake" merely because its data originated in Fabric. Verify the available experience in the target Government tenant rather than assuming both variants are present.

Import remains a legitimate option if it is the verified path and meets the workload. Choosing a working, supportable mode is more important than displaying a particular product label.

## 3. Build a small, reusable reconciliation model

Connect to the Gold result using the preflighted tenant experience and create or inspect an explicitly named semantic model. Do not depend on the assumption that creating a Warehouse automatically creates the intended model and measures.

For the examples below, name the model table `Reconciliation`. Map it to `gold.reconciliation`, and expose friendly names where useful. Retain `batch_id` and `published_at_utc` so consumers can understand which publication they are viewing.

The current table is sufficient for a small lesson. A broader enterprise model might separate facts and dimensions, but adding those structures here would distract from the consumption decision.

### Define reusable measures

Create these measures in the semantic model:

```dax
Compared Records =
COUNTROWS('Reconciliation')
```

```dax
Matched Records =
COALESCE(
    CALCULATE(
        [Compared Records],
        KEEPFILTERS('Reconciliation'[classification] = "MATCH")
    ),
    0
)
```

```dax
Exception Records =
COALESCE(
    CALCULATE(
        [Compared Records],
        KEEPFILTERS('Reconciliation'[classification] <> "MATCH")
    ),
    0
)
```

```dax
Match Rate =
DIVIDE([Matched Records], [Compared Records])
```

`Compared Records` counts Gold business keys, not raw source rows. `KEEPFILTERS` makes the classification condition intersect the current report filters rather than replacing a classification selection. This matters when a visual or slicer already limits the classifications being shown.

Format `Match Rate` as a percentage. In an unfiltered baseline report, expect six compared records, one match, five exceptions, and a match rate of approximately 16.67%.

The current Gold table contains only the latest publication. A chart using its timestamp does not create a historical trend. Historical analysis would require a deliberate history design rather than pretending overwritten snapshots remain available.

### Create an explainable report

Use summary cards for the four measures, a classification breakdown, and a detail table containing record ID, both amounts, both statuses, classification, and publication metadata.

The summary tells the audience where to look. The detail table lets them investigate why.

Trace A002 through the report and back to SQL. Its mismatch should be explained by 200.00 versus 250.00, not by a visual effect or a report-only formula. Trace A005 as well: a duplicate is an exception even though its source amounts appear consistent.

Do not make a match rate look better by filtering away quality exceptions without disclosure. If an approved business metric uses only comparable records as its denominator, define that as a separate measure with a distinct name and documented eligibility rules.

## 4. Compare direct SQL consumption

Some users need SQL rather than a report. An analyst may investigate exceptions, or an approved integration may read the curated output.

Direct SQL is reasonable when those consumers have the necessary skills, permissions, and support agreement. They should read the curated result rather than rebuilding reconciliation independently from Bronze.

For example:

```sql
SELECT
    batch_id,
    classification,
    COUNT(*) AS record_count
FROM gold.reconciliation
GROUP BY batch_id, classification
ORDER BY batch_id, classification;
```

This produces a classification summary without duplicating the record-level comparison rules.

However, SQL clients do not automatically inherit the DAX measures or semantic-model row-level security. Granting SQL access is a separate decision. If direct SQL consumers must share an aggregate definition, expose and govern that definition through an approved SQL object or contract as well.

Similarly, a report author who needs to build a new report over a shared model may require model Build permission. That is not the same as permission merely to view an existing report, and neither should be assumed to require broad workspace write access.

## 5. Govern access and prove freshness

Access crosses several boundaries: source connections, workspace roles, Warehouse objects, the semantic model, and the report or app. There may also be OneLake access routes. Permission at one boundary is not proof that all other boundaries are appropriately restricted.

Test the intended consumer identity, not just an administrator's view. A successful demonstration under the presenter's broad privileges proves little about a read-only user's experience.

Separate four freshness questions:

1. Did both intended source snapshots load successfully?
2. Did the SQL publication complete for the intended comparison?
3. Did the chosen model mode observe that publication through its required refresh, framing, or query path?
4. Does the report display the intended publication and expected results?

For Import, the model refresh is an explicit additional data-copy step. For Direct Lake, inspect the applicable framing and freshness behavior instead of assuming every report interaction sees the latest source state immediately. For DirectQuery, query-time access still does not prove that the underlying Gold publication is the correct one.

Use the batch identifier, publication timestamp, and known expected result together. A timestamp by itself does not prove business correctness.

## 6. Make the consumption decision

Complete a short decision:

> Our primary audience is ___. We will publish ___ through a shared semantic model using the verified ___ mode. Record-level reconciliation rules remain in ___. Reusable reporting measures live in ___. Direct SQL access is permitted for ___ through ___. Freshness is verified by ___. The model and access owners are ___.

A strong decision identifies who owns definitions, who receives each access path, and how new publications become visible. "We will use Direct Lake because it is faster" is insufficient without testing the relevant workload, capability, and security requirements.

## Lesson conclusion

Governed consumption is more than connecting a report to a table. We have separated the reusable business model from the storage/query mode, kept reconciliation rules consistent across consumers, and made freshness and access testable.

**Previous:** [Lesson 3](03_curated_sql_engineering.md)  
**Next:** [Lesson 5: Operations and GCC High findings](05_operations_and_gcc_high_findings.md)

**Product reference:** [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview). General documentation describes product options, not verified availability or identity behavior in the target GCC High environment.
