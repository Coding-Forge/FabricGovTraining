"""Check packaged fixtures and lesson alignment without connecting to Fabric.

Run: python lessons/session_03/artifacts/validate_lab_assets.py
"""

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "artifacts"


def read_csv(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def normalize_sql(value):
    return re.sub(r"\s+", " ", value).strip()


def reference_result(a_rows, b_rows):
    """Independent fixture oracle, not an execution of the Warehouse procedure."""
    grouped = {}
    for system, rows, fields in (
        ("A", a_rows, ("RecordId", "Amount", "Status")),
        ("B", b_rows, ("Reference", "Total", "State")),
    ):
        for row in rows:
            key = row[fields[0]].strip().upper()
            if not key:
                raise ValueError("Blank keys block teaching publication")
            try:
                amount = Decimal(row[fields[1]].strip()).quantize(Decimal("0.01"))
            except InvalidOperation:
                amount = None
            status = row[fields[2]].strip().upper() or None
            grouped.setdefault(key, {"A": [], "B": []})[system].append((amount, status))

    result = []
    for key, sources in sorted(grouped.items()):
        a, b = sources["A"], sources["B"]
        a_amount, a_status = a[0] if len(a) == 1 else (None, None)
        b_amount, b_status = b[0] if len(b) == 1 else (None, None)
        if len(a) > 1 or len(b) > 1:
            classification = "DUPLICATE_KEY"
        elif any(amount is None for amount, _ in a + b):
            classification = "INVALID_AMOUNT"
        elif any(status is None for _, status in a + b):
            classification = "INVALID_STATUS"
        elif not b:
            classification = "ONLY_IN_A"
        elif not a:
            classification = "ONLY_IN_B"
        elif a_amount != b_amount and a_status != b_status:
            classification = "AMOUNT_AND_STATUS_MISMATCH"
        elif a_amount != b_amount:
            classification = "AMOUNT_MISMATCH"
        elif a_status != b_status:
            classification = "STATUS_MISMATCH"
        else:
            classification = "MATCH"
        result.append({
            "record_id": key,
            "a_row_count": str(len(a)),
            "b_row_count": str(len(b)),
            "a_amount": str(a_amount) if a_amount is not None else "",
            "b_amount": str(b_amount) if b_amount is not None else "",
            "a_status": a_status or "",
            "b_status": b_status or "",
            "classification": classification,
        })
    return result


class LabPackageChecks(unittest.TestCase):
    def test_fixtures_match_documented_results(self):
        a = read_csv(ASSETS / "data/baseline/system_a.csv")
        baseline_b = read_csv(ASSETS / "data/baseline/system_b.csv")
        corrected_b = read_csv(ASSETS / "data/corrected/system_b.csv")
        self.assertEqual((len(a), len(baseline_b)), (6, 5))
        changes = [
            (before, after)
            for before, after in zip(baseline_b, corrected_b)
            if before != after
        ]
        self.assertEqual(changes, [(
            {"Reference": "A002", "Total": "250.00", "State": "ACTIVE"},
            {"Reference": "A002", "Total": "200.00", "State": "ACTIVE"},
        )])
        for scenario, b, matches in (
            ("baseline", baseline_b, 1), ("corrected", corrected_b, 2)
        ):
            with self.subTest(scenario=scenario):
                actual = reference_result(a, b)
                expected = read_csv(ASSETS / f"data/expected/{scenario}.csv")
                self.assertEqual(actual, expected)
                self.assertEqual(sum(r["classification"] == "MATCH" for r in actual), matches)

    def test_csvs_sql_and_dax_match_teaching_sources(self):
        ingestion = (ROOT / "02_repeatable_ingestion.md").read_text()
        for filename, block in zip(
            ("system_a.csv", "system_b.csv"),
            re.findall(r"```csv\n(.*?)```", ingestion, re.S),
        ):
            self.assertEqual((ASSETS / "data/baseline" / filename).read_text().strip(), block.strip())

        lesson = (ROOT / "03_curated_sql_engineering.md").read_text()
        blocks = re.findall(r"```sql\n(.*?)```", lesson, re.S)
        for name, prefix in (
            ("02_create_normalized_view.sql", "CREATE VIEW silver.normalized_records"),
            ("03_create_summary_view.sql", "CREATE VIEW silver.record_summary"),
            ("04_create_refresh_procedure.sql", "CREATE PROCEDURE gold.usp_refresh_reconciliation"),
        ):
            original = next(block for block in blocks if block.startswith(prefix))
            self.assertEqual(normalize_sql((ASSETS / "sql" / name).read_text()), normalize_sql(original))

        seed = (ASSETS / "sql/91_seed_baseline_sql_only.sql").read_text()
        for system, filename in (("a", "system_a.csv"), ("b", "system_b.csv")):
            values = re.search(
                rf"INSERT INTO bronze\.system_{system} .*?VALUES(.*?);", seed, re.S
            ).group(1)
            tuples = re.findall(r"\('([^']*)', '([^']*)', '([^']*)'\)", values)
            self.assertEqual(tuples, [tuple(row.values()) for row in read_csv(ASSETS / "data/baseline" / filename)])

        dax = (ASSETS / "dax/reconciliation_measures.dax").read_text()
        for block in re.findall(r"```dax\n(.*?)```", (ROOT / "04_consumption_architecture.md").read_text(), re.S):
            self.assertIn(normalize_sql(block), normalize_sql(dax))

    def test_lab_links_and_metadata(self):
        guides = sorted((ROOT / "labs").glob("0[1-6]_*.md"))
        self.assertEqual(len(guides), 6)
        total = 0
        for path in guides + [ROOT / "labs/README.md"]:
            content = path.read_text()
            self.assertEqual(content.count("```") % 2, 0, path.name)
            if path in guides:
                total += int(re.search(r"\| (\d+) minutes\*\*", content).group(1))
                self.assertIn("**Lesson output:**", content)
            for link in re.findall(r"\]\(([^)]+)\)", content):
                if link.startswith(("http:", "https:", "#")):
                    continue
                self.assertTrue((path.parent / link.split("#")[0]).is_file(), (path.name, link))
        self.assertEqual(total, 96)


if __name__ == "__main__":
    print("Offline package checks only; no Fabric, Dataflow, DAX, or access execution is performed.", flush=True)
    unittest.main(verbosity=2)
