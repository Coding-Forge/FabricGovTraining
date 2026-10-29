"""Build portable, output-free Session 04 starter/solution .ipynb files.

Run: python lessons/session_04/artifacts/build_notebooks.py
Only explicit Python fences become executable cells. Warehouse SQL stays prose.
"""

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_DEVICE = "D032"
CHALLENGE_DATES = ("2026-10-06", "2026-10-10")
PRACTICES = {
    "python-normalize": (
        "Define normalize_identifier(value): return a stripped uppercase string "
        "or None for missing/blank input; add the three handout assertions."
    ),
    "spark-clean": (
        "Create toy_clean from toy_raw. Normalize device_id with Spark functions "
        "and try_cast temperature_text into decimal(8,2) as temperature_c."
    ),
    "spark-sql": (
        "Create sql_daily with spark.sql: group s04_101_accepted by device_id; "
        "return device_id, reading_count, and decimal(8,2) avg_temperature_c."
    ),
    "main-firmware": (
        "Create/display firmware_profile: filter devices to site S03 and count "
        "raw rows by firmware_version."
    ),
    "main-coverage": (
        "Create/display device_day: filter coverage to D017 on 2026-10-07 and "
        "select reading_date, device_id, reading_count, accepted_slot_shortfall."
    ),
    "main-status": (
        "Create/display status_summary: group order_transfer by order_status "
        "and calculate accepted_lines and accepted_line_amount."
    ),
}


def cell(kind, source, tags=()):
    result = {
        "cell_type": kind,
        "metadata": {"tags": list(tags)} if tags else {},
        "source": source.strip().splitlines(keepends=True),
    }
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


def markdown_cell(source):
    def relative_link(match):
        label, target = match.groups()
        if target.startswith(("https:", "http:", "#")):
            return match.group(0)
        return f"[{label}](../{target})"

    return cell("markdown", re.sub(r"\[([^\]]+)\]\(([^)]+)\)", relative_link, source))


def lesson_cells(path, solution):
    text = path.read_text(encoding="utf-8")
    cells = []
    position = 0
    for block in re.finditer(r"```python\n(.*?)```", text, re.DOTALL):
        before = text[position:block.start()]
        marker = re.search(r"<!-- practice: ([a-z-]+) -->\s*$", before)
        if marker:
            before = before[:marker.start()]
        if before.strip():
            cells.append(markdown_cell(before))
        tags = []
        code = block.group(1).strip()
        if marker:
            practice = marker.group(1)
            prompt = PRACTICES[practice]
            tags = ["practice", practice]
            if not solution:
                code = (
                    "# Replace this intentional practice stop with your answer.\n"
                    f"raise NotImplementedError({prompt!r})"
                )
        cells.append(cell("code", code, tags))
        position = block.end()
    if text[position:].strip():
        cells.append(markdown_cell(text[position:]))
    return cells


def troubleshooting_cells(solution):
    cells = [
        cell("markdown", """
# Fix the notebook: Three safe mistakes

Use the assigned default Lakehouse with pre-staged scenario files. This is a
**read-only** exercise. Run setup first, then repair one labeled error at a time.
Do not begin with Run all in the starter. In a new session the first error is
an undefined variable, the second is a column typo, and the third is a path typo.
Unexpected setup/permission failures are readiness blockers, not exercises.

The solution fills all three repairs. For learner completion, explain each fix,
restart your own session, and run your repaired notebook from the top.
"""),
        cell("code", """
from pyspark.sql import types as T

REPAIR_BASE = "Files/session_04/scenario"
repair_fields = [
    "device_id", "event_id", "event_time_utc", "temperature_c",
    "firmware_version", "signal_strength_dbm", "ui_theme", "debug_message",
    "export_row_number", "site_id", "device_type",
]
repair_schema = T.StructType([
    T.StructField(name, T.StringType()) for name in repair_fields
])
repair_source = (
    spark.read.schema(repair_schema).option("header", True)
    .option("mode", "FAILFAST")
    .csv(REPAIR_BASE + "/devices/readings_2026-10-01.csv")
)
repair_source.limit(5).show(truncate=False)
"""),
        cell("markdown", """
## Repair 1: Where does this variable come from?

Run the next cell in a fresh session. The starter raises `NameError`.
Define the preview limit before its use; do not rely on a value left in another
notebook/session. Explain why saved output does not establish current state.
"""),
        cell("code", (
            "repair_preview_limit = 5\nprint(repair_preview_limit)"
            if solution else "print(repair_preview_limit)"
        ), ["repair", "missing-variable"]),
        cell("markdown", """
## Repair 2: Which columns actually exist?

The starter asks Spark for a misspelled field. Inspect `repair_source.printSchema()`
and correct the reference. Do not invent a replacement column or silently drop
the measurement. The value is raw text here; selecting it does not validate it.
"""),
        cell("code", (
            'repair_source.select("device_id", "temperature_c").limit(5).show(truncate=False)'
            if solution else
            'repair_source.select("device_id", "temperatur_c").limit(5).show(truncate=False)'
        ), ["repair", "column-name"]),
        cell("markdown", """
## Repair 3: Does the folder match the prepared source?

The starter uses `devicez`, not the approved `devices` folder. Compare with
Lakehouse Files and correct that one path. Do not change credentials, permissions,
or source files to work around this error.
"""),
        cell("code", (
            "repair_file = (\n"
            "    spark.read.schema(repair_schema).option('header', True)\n"
            "    .option('mode', 'FAILFAST')\n"
            f"    .csv(REPAIR_BASE + '/{'devices' if solution else 'devicez'}/"
            "readings_2026-10-01.csv')\n"
            ")\n"
            "repair_file.limit(5).show(truncate=False)"
        ), ["repair", "source-path"]),
        cell("markdown", """
## Prove the repair

Record each original message, the root cause, and your correction. Restart your
own session and rerun setup plus all three repaired cells in order. No persistent
write, package installation, credential change, or Warehouse SQL is needed.
Return to the Notebook 101 handout and then the main lab.
"""),
    ]
    return cells


def challenge_cells(solution):
    with (ROOT / "artifacts/data/scenario/expected/device_daily.csv").open(newline="") as stream:
        reference = [
            row for row in csv.DictReader(stream)
            if row["device_id"] == CHALLENGE_DEVICE and row["reading_date"] in CHALLENGE_DATES
        ]
    reference.sort(key=lambda row: row["reading_date"])
    if len(reference) != 2:
        raise ValueError("The challenge answer key must contain both requested days.")
    reference_table = [
        "| UTC date | Accepted | Min C | Max C | Mean C | Shortfall / 288 | Accepted % |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in reference:
        count = int(row["reading_count"])
        percent = (Decimal(count) / 288 * 100).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        reference_table.append(
            f"| {row['reading_date']} | {count} | {row['min_temperature_c']} | "
            f"{row['max_temperature_c']} | {row['avg_temperature_c']} | "
            f"{288 - count} | {percent} |"
        )
    difference = Decimal(reference[1]["avg_temperature_c"]) - Decimal(
        reference[0]["avg_temperature_c"]
    )
    return [
        cell("markdown", """
# Independent challenge: Evidence, not just a green notebook

After the successful main notebook, answer the question for D032 on October 10
versus October 6, 2026 UTC. Use existing accepted Silver for metrics and source
exports/quarantine for quality evidence. No writes, source edits, installs, or
permission changes. Setup supplies context only, not a transformation recipe.
See `10_independent_challenge.md` in the supplied training package for the rubric.
"""),
        cell("code", f"""
from pyspark.sql import functions as F

spark.conf.set("spark.sql.session.timeZone", "UTC")
DEVICE_ID = {CHALLENGE_DEVICE!r}
BASELINE_DATE, TARGET_DATE = {CHALLENGE_DATES!r}
BATCH_ID = "s04-lab-devices-001"
SCHEDULED_READINGS = 288
for table in ("s04_lab_device_silver", "s04_lab_device_bronze", "s04_lab_device_rejected"):
    if not spark.catalog.tableExists(table):
        raise RuntimeError("Run the successful main notebook in this default Lakehouse first.")
challenge_events = spark.table("s04_lab_device_silver").filter(F.col("batch_id") == BATCH_ID)
challenge_bronze = spark.table("s04_lab_device_bronze").filter(F.col("batch_id") == BATCH_ID)
challenge_rejected = spark.table("s04_lab_device_rejected").filter(F.col("batch_id") == BATCH_ID)
"""),
        cell("markdown", """
## Task 1: Summarize the two days

Return device/day/site/type, accepted count, min/max/mean temperature, scheduled
count, accepted-slot shortfall, and accepted percentage. Use accepted events,
two UTC dates, and a clearly stated grain. Do not copy a pre-aggregated answer.
"""),
        cell("code", """
challenge_summary = (
    challenge_events.filter(F.col("device_id") == DEVICE_ID)
    .withColumn("reading_date", F.to_date("event_time_utc"))
    .filter(F.col("reading_date").isin(BASELINE_DATE, TARGET_DATE))
    .groupBy("reading_date", "device_id", "site_id", "device_type")
    .agg(
        F.count("*").alias("reading_count"),
        F.min("temperature_c").alias("min_temperature_c"),
        F.max("temperature_c").alias("max_temperature_c"),
        F.avg("temperature_c").cast("decimal(8,2)").alias("avg_temperature_c"),
    )
    .withColumn("scheduled_readings", F.lit(SCHEDULED_READINGS))
    .withColumn("accepted_slot_shortfall", SCHEDULED_READINGS - F.col("reading_count"))
    .withColumn("accepted_percent", F.round(F.col("reading_count") / SCHEDULED_READINGS * 100, 2))
)
display(challenge_summary.orderBy("reading_date"))
""" if solution else """
raise NotImplementedError("Task 1: Build and display your accepted-only device/day summary.")
""", ["challenge", "daily-summary"]),
        cell("markdown", """
## Task 2: Explain the source populations

Count raw source rows and quarantine reasons for each requested daily export.
Include a zero-rejection day explicitly. Use source_file for export scope:
an invalid timestamp cannot establish that record's true event date.
"""),
        cell("code", r"""
def export_scope(df):
    return (
        df.filter(F.upper(F.trim("device_id")) == DEVICE_ID)
        .withColumn("source_export_date", F.regexp_extract(
            "source_file", r"readings_([0-9]{4}-[0-9]{2}-[0-9]{2})\.csv$", 1
        ))
        .filter(F.col("source_export_date").isin(BASELINE_DATE, TARGET_DATE))
    )


source_counts = export_scope(challenge_bronze).groupBy("source_export_date").agg(
    F.count("*").alias("raw_source_rows")
)
rejection_counts = export_scope(challenge_rejected).groupBy(
    "source_export_date", "quality_issue"
).count()
rejection_totals = rejection_counts.groupBy("source_export_date").agg(
    F.sum("count").alias("quarantine_rows")
)
quality_summary = source_counts.join(
    rejection_totals, "source_export_date", "left"
).fillna({"quarantine_rows": 0})
display(quality_summary.orderBy("source_export_date"))
display(rejection_counts.orderBy("source_export_date", "quality_issue"))
""" if solution else """
raise NotImplementedError("Task 2: Count raw export rows and quarantine evidence for both dates.")
""", ["challenge", "quality-evidence"]),
        cell("markdown", (
            "## Presenter answer key\n\n"
            + "\n".join(reference_table)
            + f"\n\nD032 is a COLD_STORE device at S04. The change between reported "
            f"rounded daily means is **{difference:.2f} C** (target minus baseline).\n\n"
            "October 6 has 291 raw rows and 35 quarantine rows: "
            "10 DUPLICATE_EVENT, 10 INVALID_TEMPERATURE, 5 INVALID_TIMESTAMP, "
            "5 MISSING_EVENT_KEY, and 5 OUT_OF_RANGE. October 10 has 287 raw rows "
            "and **zero** quarantine rows. Filling a missing aggregate count with "
            "zero for reporting is not filling invalid sensor values with zero.\n\n"
            "October 10 still lacks one accepted observation against the known "
            "288-slot schedule. Zero quarantine does not prove complete ingestion "
            "or device uptime. The baseline has 32 slots without accepted readings; "
            "raw/quarantine counts include duplicate occurrences and are different "
            "populations. Invalid-time records are scoped by source export, not "
            "assigned repaired event timestamps.\n\n"
            "A -0.01 C difference between rounded means is not evidence of a trend, "
            "statistical significance, device health, or a firmware-related cause. "
            "Do not average those rounded means into an overall event mean. "
            "Compute ran on Fabric Spark over persisted Lakehouse tables; this "
            "exercise writes nothing and proves no Warehouse/model freshness.\n\n"
            "Restart your own session and rerun to demonstrate independence from "
            "other notebooks' variables. Evaluate the learner's explanation, not "
            "just whether this completed solution ran."
            if solution else """
## Task 3: Your interpretation

Replace this Markdown with your question/scope/grain, both summaries, the
reported-mean comparison, source/quality caveats, accepted coverage conclusion,
and limits on device-health/causality claims. State where execution occurred,
whether anything was persisted, and what this does not prove about Warehouse
Gold or model freshness. Restart your own session and rerun your completed work.
"""
        ), ["challenge", "interpretation"]),
    ]


def notebook(cells, title, source, solution):
    introduction = cell("markdown", f"""
# {title} - {"completed solution" if solution else "participant starter"}

Select **PySpark**, attach the facilitator-assigned default Lakehouse, and
confirm pre-delivery readiness before running. No Lakehouse/workspace IDs,
credentials, outputs, or preselected environment are embedded.

{"Worked answers are supplied; explain them rather than treating a green run as learner completion." if solution else "Practice stops/errors are intentional; follow the handout and complete them before continuing."}

Source: `{source}` in the supplied training package. Relative documentation links
work in the repository/package context and may not resolve after Fabric import;
keep the matching handout and notebook import guide open separately.
""")
    all_cells = [introduction, *cells]
    for index, item in enumerate(all_cells, 1):
        item["id"] = f"s04-cell-{index:03d}"
    return {
        "cells": all_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Synapse PySpark",
                "language": "python",
                "name": "synapse_pyspark",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    names = []
    for solution in (False, True):
        suffix = "solution" if solution else "starter"
        for stem, title, source in (
            ("00_notebook_101", "Notebook 101", "00_notebook_101.md"),
            ("02_main_lab", "Realistic notebook main lab", "09_realistic_data_lab.md"),
        ):
            content = notebook(
                lesson_cells(ROOT / source, solution), title, source, solution
            )
            path = output / f"{stem}_{suffix}.ipynb"
            with path.open("w", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(content, indent=2) + "\n")
            names.append(path)
        content = notebook(
            challenge_cells(solution), "Independent device analysis",
            "10_independent_challenge.md and artifacts/build_notebooks.py (challenge_cells)",
            solution,
        )
        path = output / f"03_independent_challenge_{suffix}.ipynb"
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(content, indent=2) + "\n")
        names.append(path)
        content = notebook(
            troubleshooting_cells(solution), "Fix the notebook",
            "artifacts/build_notebooks.py (troubleshooting_cells)", solution,
        )
        path = output / f"01_troubleshooting_{suffix}.ipynb"
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(content, indent=2) + "\n")
        names.append(path)
    return names


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "notebooks")
    args = parser.parse_args()
    for filename in build(args.output):
        print(filename.name)
