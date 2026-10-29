# Lesson 7: Decide what belongs in Silver, then shape Gold

**Session 04 | Column selection and serving contracts**  
**Output:** A column decision record and an explainable transformation from accepted Silver events to Warehouse Gold.

**Tier choice:** The detailed ten-/twelve-column contracts below use the micro
fixtures. The [main lab](09_realistic_data_lab.md) extends the same reasoning to
realistic data; its schemas and counts are intentionally different.

| Main-lab field | Silver | Gold | Reason |
| --- | --- | --- | --- |
| Device `site_id`, `device_type` | Keep | Keep in daily output | Useful diagnostic/serving dimensions; stable per device in this source contract |
| Device firmware/signal | Keep | Not in device/day Gold | Diagnose changes; firmware is not necessarily single-valued per day |
| Order date/status/region/category | Keep | Keep in accepted-line output | Enable dated, regional, product, and status SQL without re-reading raw JSON |
| Optional shipping service | Keep nullable | Omit for this contract | Reusable fulfillment context; missing shipping is allowed |
| Address, description, display/debug/UI fields | Raw evidence, not this accepted contract | Omit | No requirement in this serving contract; not a universal deletion/noise judgment |

The main lab persists **twelve device Silver columns** and **seventeen order
Silver columns**, transferring nine device/day and thirteen order-line columns.
Its exact projections and expected-row comparisons are in the main walkthrough.

## Silver is not "everything after cleaning"

The notebook needs many temporary columns to investigate and validate input. They do not all belong in the persisted analytical contract.

Use four destinations:

| Destination | Purpose |
| --- | --- |
| Bronze/raw evidence | Preserve the approved source representation for replay and investigation, subject to retention/access rules |
| Quarantine/quality evidence | Explain rejected records, including raw values and reasons |
| Accepted Silver | Reusable typed business records, useful domain context, and enough lineage to explain their origin |
| Gold | A governed consumer contract with a stated grain, definitions, and publication metadata |

These are responsibilities, not a mandatory number of workspaces. In this example Silver is in the Lakehouse and Gold is physically published into the Warehouse.

"Noise" means irrelevant to a particular analytical contract. It does not mean safe to erase everywhere. Likewise, a constant field, high-null field, identifier, or technical field is not automatically noise.

## Ask these questions before selecting columns

1. Does it identify the business entity/event, establish its grain, or support a valid join?
2. Does it carry a meaningful measure, unit, business time, or reusable dimension/context?
3. Is it needed for lineage, debugging, quality interpretation, a regulated obligation, or source-version handling?
4. Is it a raw duplicate or a temporary calculation that can remain in evidence/working state?
5. Can the proposed Gold grain represent it without choosing an arbitrary value?
6. Is retention and exposure justified? Classifying a column as useful does not override privacy, security, or minimization requirements.

Write the reason, owner, type, and destination. Do not decide solely from a histogram or this week's report.

## Worked column decision: Device readings

The source file includes five extra fields specifically to make this decision tangible.

| Source or derived column | Accepted Silver decision | Gold device/day decision | Why |
| --- | --- | --- | --- |
| `device_id` | Keep normalized string | Keep | Entity key and daily grouping |
| `event_id` | Keep normalized string | Omit from the daily table | Event identity remains at Silver grain |
| `event_time_utc` | Keep typed UTC timestamp | Derive `reading_date` | Business time; individual times cannot be one daily scalar |
| `temperature_c` | Keep typed decimal | Derive min/max/average and accepted count | Reusable event measure; Gold summarizes it |
| `firmware_version` | Keep as text | Omit for this contract | Useful for diagnostic slicing; not a decimal number or guaranteed single version per day |
| `signal_strength_dbm` | Keep optional integer context | Omit for this contract | Useful for approved signal-quality investigation |
| `ui_theme` | Bronze only | Omit | Exporter presentation preference has no role in this telemetry contract |
| `debug_message` | Bronze/diagnostic evidence only | Omit | Synthetic renderer message is not a business attribute; real diagnostics may require restricted handling |
| `export_row_number` | Bronze only | Omit | Export position can aid raw investigation but is not stable event identity |
| `batch_id` | Keep | Keep | Relates the current snapshot to the controlled run |
| `source_file` | Keep | Omit from this summary | Silver-to-Bronze trace; do not expose source paths without a consumer need |
| `ingested_at_utc` | Keep | Use separate `published_at_utc` | Arrival time and publication time are different events |
| `quality_rule_version` | Keep | Record through batch lineage; not in this table | Explain which acceptance policy produced Silver |
| Raw temperature/time strings | Bronze/quarantine only in this example | Omit | Preserve evidence without duplicating raw and typed fields in every accepted row |
| `event_key_count`, `quality_issue`, temporary typed/text helpers | Working state/quarantine | Omit | Explain acceptance; the accepted table should not accumulate every implementation helper |

Keeping firmware and signal does not assert that they are causally related to bad readings. Nine teaching rows do not establish that relationship. Optional context needs its own missing/invalid-value policy before production use.

If a new report needs firmware/day metrics, revisit Gold's grain and business question. Do not select `MAX(firmware_version)` merely to satisfy GROUP BY, or group by firmware and continue claiming one row per device/day.

## The actual accepted Silver contract

The [device notebook's Cell 3](03_device_telemetry.md#cell-3-separate-accepted-and-rejected-events) persists exactly these ten columns:

```text
batch_id                string
device_id               string
event_id                string
event_time_utc          timestamp, interpreted in UTC
temperature_c           decimal(8,2)
firmware_version        string
signal_strength_dbm     int
source_file             string
ingested_at_utc         timestamp
quality_rule_version    string
```

Four accepted rows remain at event grain. The five rejected rows retain their reasons and raw/context fields in the separate quarantine table.

An explicit select/allowlist is intentional. A blanket `drop()` of today's three known noise columns would allow tomorrow's unexpected source column to leak into Silver. Contract changes should be deliberate.

These are current-batch teaching snapshots. Silver's rule version helps explain the current output but is not a durable historical batch manifest. A production run record must retain the batch-to-input/rule/version mapping before current tables are replaced.

After running the device notebook, inspect the persisted result rather than only the in-memory variable:

```python
from pyspark.sql import functions as F

silver = spark.table("s04_device_events_silver").filter(
    F.col("batch_id") == "s04-devices-001"
)
silver.printSchema()
silver.orderBy("device_id", "event_time_utc").show(truncate=False)

unexpected = {"ui_theme", "debug_message", "export_row_number"} & set(
    silver.columns
)
if unexpected:
    raise ValueError(f"Evidence-only columns leaked into Silver: {unexpected}")

if silver.groupBy("batch_id", "device_id", "event_id").count().filter(
    F.col("count") != 1
).limit(1).count():
    raise ValueError("Accepted Silver must have unique event keys in this batch.")
```

This inspection complements the acceptance checks; a schema alone does not prove that the correct four events were accepted.

## Process Silver into the Gold contract

The [device notebook's Cell 4](03_device_telemetry.md#cell-4-build-the-warehouse-handoff-table) reads the persisted Silver table, derives UTC reading date, groups by batch/device/day, and computes:

- `reading_count`: accepted observed events.
- `min_temperature_c` and `max_temperature_c`: accepted event extrema.
- `avg_temperature_c`: accepted event mean at the declared precision.

The seven-column transfer contract is:

```text
batch_id, reading_date, device_id, reading_count,
min_temperature_c, max_temperature_c, avg_temperature_c
```

There are two rows:

| Date | Device | Accepted count | Min | Max | Average |
| --- | --- | --- | --- | --- | --- |
| 2026-10-28 | D01 | 2 | 20.00 | 24.00 | 22.00 |
| 2026-10-28 | D02 | 2 | 30.00 | 32.00 | 31.00 |

Firmware, individual event IDs, UI theme, and raw strings do not cross this particular handoff. That does not make all of them useless; their correct home differs.

Use the existing [Warehouse publication walkthrough](04_warehouse_gold.md) to copy these columns into staging, validate, and transactionally replace the current Gold table. Warehouse Gold adds `published_at_utc`.

The Lakehouse transfer table is a prepared output, not proof of Warehouse publication. A real copy/connector execution and SQL result check are required.

## Verify the published Gold, not just the notebook

Run in the approved training Warehouse after publication:

```sql
SELECT
    batch_id, reading_date, device_id, reading_count,
    min_temperature_c, max_temperature_c, avg_temperature_c,
    published_at_utc
FROM gold.s04_device_daily
ORDER BY reading_date, device_id;

SELECT
    COUNT(*) AS device_day_rows,
    SUM(reading_count) AS accepted_event_rows
FROM gold.s04_device_daily
WHERE batch_id = 's04-devices-001';
```

Expect two device/day rows representing four accepted events, not nine. Confirm the exact per-device values, batch, and publication evidence before treating the model/report as current.

Daily averages are not automatically additive across devices/days. A wider-grain average needs the appropriate underlying sum and count; rounding daily means can lose information. Define that requirement and extend the serving contract deliberately rather than averaging averages by convenience.

## Apply the same reasoning to orders

The [orders notebook](02_nested_json_orders.md#cell-5-persist-evidence-and-the-warehouse-transfer-contract) now selects twelve Silver columns: the nine business/batch transfer fields plus `source_file`, `ingested_at_utc`, and `quality_rule_version`.

The full `raw_json`, expanded `item` structure, text-conversion helpers, and duplicate counts stay in Bronze/quarantine or working state, not the accepted line contract. Warehouse Gold keeps the nine transfer fields and adds publication time.

Gold need not always be an aggregate. The accepted order-line Gold table keeps one accepted line per `(order_id, line_number)` for SQL/BI use. Its three rows total 296.00 in accepted-line amount; it is not a complete-order revenue ledger.

## Learner exercise

Have pairs mark every device field as key, measure/time, reusable context, lineage, quality evidence, or irrelevant to this contract. Require a reason for three inclusions and three exclusions.

Then introduce two changes:

1. Operations needs to investigate accepted temperatures by firmware. Does Silver already support the question? What additional Gold contract, if any, would be appropriate?
2. Someone proposes using export row number to make duplicates disappear. Which identity rule would that violate?

Completion evidence is the annotated column decision, the persisted Silver schema, the rejected-record explanation, and the exact Warehouse Gold result. No layer is complete merely because its table name contains "silver" or "gold".
