"""Check both Session 04 dataset tiers, reproducibility, contracts, and links.

Run: python lessons/session_04/artifacts/validate_examples.py
This does not execute Spark, Warehouse SQL, copy activities, or tenant identities.
"""

import ast
from collections import Counter, defaultdict
from contextlib import redirect_stdout
import csv
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
import unittest

from generate_datasets import generate
from build_notebooks import build


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "artifacts" / "data"
SCENARIO = DATA / "scenario"
NOTEBOOKS = ROOT / "notebooks"


def key(value):
    return value.strip().upper()


def scenario_devices():
    for path in sorted((SCENARIO / "devices").glob("*.csv")):
        with path.open(newline="") as stream:
            yield from csv.DictReader(stream)


class NotebookExampleChecks(unittest.TestCase):
    def test_importable_notebooks_are_clean_portable_and_current(self):
        names = {
            f"{stem}_{variant}.ipynb"
            for stem in (
                "00_notebook_101", "01_troubleshooting", "02_main_lab",
                "03_independent_challenge",
            )
            for variant in ("starter", "solution")
        }
        self.assertEqual({path.name for path in NOTEBOOKS.glob("*.ipynb")}, names)
        for name in sorted(names):
            notebook = json.loads((NOTEBOOKS / name).read_text())
            self.assertEqual((notebook["nbformat"], notebook["nbformat_minor"]), (4, 5))
            self.assertEqual(set(notebook["metadata"]), {"kernelspec", "language_info"})
            self.assertEqual(notebook["metadata"]["kernelspec"]["name"], "synapse_pyspark")
            self.assertTrue(notebook["cells"], name)
            ids = [cell["id"] for cell in notebook["cells"]]
            self.assertEqual(len(ids), len(set(ids)), name)
            for index, cell in enumerate(notebook["cells"]):
                self.assertRegex(cell["id"], r"^[A-Za-z0-9_-]{1,64}$")
                self.assertIn(cell["cell_type"], ("markdown", "code"))
                self.assertIsInstance(cell["source"], list)
                self.assertTrue(all(isinstance(line, str) for line in cell["source"]))
                if cell["cell_type"] == "code":
                    self.assertIsNone(cell["execution_count"], name)
                    self.assertEqual(cell["outputs"], [], name)
                    ast.parse("".join(cell["source"]), filename=f"{name}:cell-{index}")
        with tempfile.TemporaryDirectory(prefix="s04-notebooks-") as directory:
            generated = build(Path(directory))
            self.assertEqual(len(generated), len(names))
            self.assertEqual({path.name for path in generated}, names)
            for path in generated:
                self.assertEqual(
                    path.read_bytes(), (NOTEBOOKS / path.name).read_bytes(), path.name
                )

    def test_notebook_starters_only_replace_three_practice_answers(self):
        for stem, source in (
            ("00_notebook_101", "00_notebook_101.md"),
            ("02_main_lab", "09_realistic_data_lab.md"),
        ):
            starter = json.loads((NOTEBOOKS / f"{stem}_starter.ipynb").read_text())
            solution = json.loads((NOTEBOOKS / f"{stem}_solution.ipynb").read_text())
            self.assertEqual(len(starter["cells"]), len(solution["cells"]))
            practice_count = 0
            for left, right in zip(starter["cells"][1:], solution["cells"][1:]):
                if "practice" in right["metadata"].get("tags", []):
                    practice_count += 1
                    self.assertEqual(left["metadata"], right["metadata"])
                    stop = ast.parse("".join(left["source"])).body
                    self.assertEqual(len(stop), 1)
                    self.assertIsInstance(stop[0], ast.Raise)
                    self.assertEqual(stop[0].exc.func.id, "NotImplementedError")
                    self.assertNotEqual(left["source"], right["source"])
                else:
                    self.assertEqual(left, right, (stem, right["id"]))
            self.assertEqual(practice_count, 3, stem)
            expected_code = [
                block.strip()
                for block in re.findall(
                    r"```python\n(.*?)```", (ROOT / source).read_text(), re.DOTALL
                )
            ]
            actual_code = [
                "".join(cell["source"]).strip()
                for cell in solution["cells"] if cell["cell_type"] == "code"
            ]
            self.assertEqual(actual_code, expected_code)
        main = json.loads((NOTEBOOKS / "02_main_lab_solution.ipynb").read_text())
        main_markdown = "\n".join(
            "".join(cell["source"]) for cell in main["cells"]
            if cell["cell_type"] == "markdown"
        )
        for sql in re.findall(
            r"```sql\n(.*?)```", (ROOT / "09_realistic_data_lab.md").read_text(), re.DOTALL
        ):
            self.assertIn(sql.strip(), main_markdown)

    def test_beginner_write_controls_and_python_exercise(self):
        warmup = json.loads((NOTEBOOKS / "00_notebook_101_solution.ipynb").read_text())
        code = [
            "".join(cell["source"]) for cell in warmup["cells"]
            if cell["cell_type"] == "code"
        ]
        configuration = ast.parse(code[0])
        flags = {
            node.targets[0].id: node.value.value
            for node in configuration.body
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
        }
        self.assertIs(flags["ALLOW_TRAINING_WRITE"], False)
        self.assertIs(flags["VERIFY_PERSISTED_TABLE"], False)
        writes = [source for source in code if ".saveAsTable(" in source]
        self.assertEqual(len(writes), 1)
        write_cell = ast.parse(writes[0])
        self.assertIsInstance(write_cell.body[0], ast.If)
        self.assertEqual(write_cell.body[0].test.id, "ALLOW_TRAINING_WRITE")
        self.assertIn('.mode("errorifexists")', writes[0])
        self.assertFalse(any('.mode("overwrite")' in source for source in code))
        practice = next(
            cell for cell in warmup["cells"]
            if "python-normalize" in cell["metadata"].get("tags", [])
        )
        namespace = {}
        exec("".join(practice["source"]), namespace)
        self.assertEqual(namespace["normalize_identifier"](" c001 "), "C001")
        self.assertIsNone(namespace["normalize_identifier"](""))
        for variant in ("starter", "solution"):
            main = json.loads((NOTEBOOKS / f"02_main_lab_{variant}.ipynb").read_text())
            gate = next(cell for cell in main["cells"] if cell["cell_type"] == "code")
            scope = {}
            with self.assertRaisesRegex(RuntimeError, "Safety stop"):
                exec("".join(gate["source"]), scope)
            self.assertIs(scope["RUN_TRAINING_LAB"], False)

    def test_repair_notebooks_have_three_read_only_actionable_fixes(self):
        pairs = {}
        for variant in ("starter", "solution"):
            notebook = json.loads(
                (NOTEBOOKS / f"01_troubleshooting_{variant}.ipynb").read_text()
            )
            pairs[variant] = [
                cell for cell in notebook["cells"] if cell["cell_type"] == "code"
            ]
            self.assertEqual(len(pairs[variant]), 4)
            for cell in pairs[variant]:
                tree = ast.parse("".join(cell["source"]))
                self.assertFalse(any(
                    isinstance(node, ast.Attribute)
                    and node.attr in ("write", "save", "saveAsTable", "insertInto", "sql")
                    for node in ast.walk(tree)
                ))
        starter, solution = pairs["starter"], pairs["solution"]
        self.assertEqual(starter[0], solution[0])
        self.assertEqual(
            sum(left["source"] != right["source"] for left, right in zip(starter, solution)),
            3,
        )
        with self.assertRaises(NameError):
            exec("".join(starter[1]["source"]), {})
        scope = {}
        with redirect_stdout(io.StringIO()):
            exec("".join(solution[1]["source"]), scope)
        self.assertEqual(scope["repair_preview_limit"], 5)
        expected_fields = json.loads((SCENARIO / "manifest.json").read_text())[
            "devices"
        ]["source_fields"]
        for variant, cells in pairs.items():
            select = next(
                node for node in ast.walk(ast.parse("".join(cells[2]["source"])))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "select"
            )
            columns = [argument.value for argument in select.args]
            self.assertEqual(
                all(column in expected_fields for column in columns),
                variant == "solution",
            )
            csv_call = next(
                node for node in ast.walk(ast.parse("".join(cells[3]["source"])))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "csv"
            )
            relative = csv_call.args[0].right.value.lstrip("/")
            self.assertEqual((SCENARIO / relative).is_file(), variant == "solution")

    def test_challenge_is_read_only_scoped_and_has_two_independent_tasks(self):
        variants = {}
        for variant in ("starter", "solution"):
            notebook = json.loads(
                (NOTEBOOKS / f"03_independent_challenge_{variant}.ipynb").read_text()
            )
            variants[variant] = [
                cell for cell in notebook["cells"] if cell["cell_type"] == "code"
            ]
            self.assertEqual(len(variants[variant]), 3)
            for code in variants[variant]:
                tree = ast.parse("".join(code["source"]))
                self.assertFalse(any(
                    isinstance(node, ast.Attribute)
                    and node.attr in (
                        "write", "save", "saveAsTable", "insertInto", "sql",
                        "delete", "remove", "unlink", "system", "install",
                    )
                    for node in ast.walk(tree)
                ))
            setup = ast.parse("".join(variants[variant][0]["source"]))
            timezone = [
                node for node in ast.walk(setup)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "set"
            ]
            self.assertEqual(
                [ast.literal_eval(arg) for arg in timezone[0].args],
                ["spark.sql.session.timeZone", "UTC"],
            )
            tasks = [
                cell for cell in notebook["cells"]
                if "challenge" in cell["metadata"].get("tags", [])
            ]
            self.assertEqual([cell["cell_type"] for cell in tasks], [
                "code", "code", "markdown",
            ])
        starter, solution = variants["starter"], variants["solution"]
        self.assertEqual(starter[0], solution[0])
        self.assertEqual(
            sum(left["source"] != right["source"] for left, right in zip(starter, solution)),
            2,
        )
        for code in starter[1:]:
            stop = ast.parse("".join(code["source"])).body
            self.assertEqual(len(stop), 1)
            self.assertIsInstance(stop[0], ast.Raise)
            self.assertEqual(stop[0].exc.func.id, "NotImplementedError")
        quality = ast.parse("".join(solution[2]["source"]))
        extraction = next(
            node for node in ast.walk(quality)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "regexp_extract"
        )
        export_pattern = ast.literal_eval(extraction.args[1])
        for date in ("2026-10-06", "2026-10-10"):
            self.assertEqual(
                re.search(export_pattern, f"abfss://example/devices/readings_{date}.csv")[1],
                date,
            )
        fill = next(
            node for node in ast.walk(quality)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "fillna"
        )
        self.assertEqual(ast.literal_eval(fill.args[0]), {"quarantine_rows": 0})

    def test_challenge_answer_key_matches_independent_source_evidence(self):
        notebook = json.loads(
            (NOTEBOOKS / "03_independent_challenge_solution.ipynb").read_text()
        )
        setup = ast.parse(next(
            "".join(cell["source"]) for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        ))
        scope = {}
        for node in setup.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                if isinstance(node.value, ast.Constant):
                    scope[node.targets[0].id] = ast.literal_eval(node.value)
            elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple):
                scope.update(zip(
                    [target.id for target in node.targets[0].elts],
                    ast.literal_eval(node.value),
                ))
        self.assertEqual(scope["BATCH_ID"], "s04-lab-devices-001")
        answer = next(
            "".join(cell["source"]) for cell in notebook["cells"]
            if "interpretation" in cell["metadata"].get("tags", [])
        )
        evidence = {}
        for date in (scope["BASELINE_DATE"], scope["TARGET_DATE"]):
            with (SCENARIO / "devices" / f"readings_{date}.csv").open(newline="") as stream:
                rows = [
                    row for row in csv.DictReader(stream)
                    if key(row["device_id"]) == scope["DEVICE_ID"]
                ]
            counts = Counter((key(row["device_id"]), key(row["event_id"])) for row in rows)
            reasons, values = Counter(), []
            for row in rows:
                device, event = key(row["device_id"]), key(row["event_id"])
                try:
                    timestamp = datetime.strptime(
                        row["event_time_utc"].strip(), "%Y-%m-%dT%H:%M:%SZ"
                    )
                except ValueError:
                    timestamp = None
                try:
                    temperature = Decimal(row["temperature_c"].strip())
                except InvalidOperation:
                    temperature = None
                if not device or not event:
                    reasons["MISSING_EVENT_KEY"] += 1
                elif counts[(device, event)] > 1:
                    reasons["DUPLICATE_EVENT"] += 1
                elif timestamp is None:
                    reasons["INVALID_TIMESTAMP"] += 1
                elif temperature is None:
                    reasons["INVALID_TEMPERATURE"] += 1
                elif not Decimal("-40") <= temperature <= Decimal("85"):
                    reasons["OUT_OF_RANGE"] += 1
                else:
                    self.assertEqual(timestamp.date().isoformat(), date)
                    self.assertEqual((row["site_id"], row["device_type"]), ("S04", "COLD_STORE"))
                    values.append(temperature)
            count = len(values)
            mean = (sum(values) / count).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            percentage = (Decimal(count) / scope["SCHEDULED_READINGS"] * 100).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            expected_row = (
                f"| {date} | {count} | {min(values):.2f} | {max(values):.2f} | "
                f"{mean:.2f} | {scope['SCHEDULED_READINGS'] - count} | {percentage} |"
            )
            self.assertIn(expected_row, answer)
            evidence[date] = (len(rows), reasons, mean)
        raw, reasons, before = evidence[scope["BASELINE_DATE"]]
        self.assertIn(f"{raw} raw rows and {sum(reasons.values())} quarantine rows", answer)
        for reason, count in reasons.items():
            self.assertIn(f"{count} {reason}", answer)
        raw, reasons, after = evidence[scope["TARGET_DATE"]]
        self.assertEqual(sum(reasons.values()), 0)
        self.assertIn(f"{raw} raw rows and **zero** quarantine rows", answer)
        self.assertIn(f"**{after - before:.2f} C**", answer)

    def test_scenario_files_and_deterministic_regeneration(self):
        manifest = json.loads((SCENARIO / "manifest.json").read_text())
        self.assertEqual(len(list((SCENARIO / "devices").glob("*.csv"))), 14)
        self.assertEqual(len(list((SCENARIO / "orders").glob("*.jsonl"))), 14)
        files = {
            path.relative_to(SCENARIO).as_posix(): path
            for path in SCENARIO.rglob("*")
            if path.is_file() and path.name != "manifest.json"
        }
        self.assertEqual(set(files), set(manifest["files"]))
        for name, digest in manifest["files"].items():
            self.assertEqual(hashlib.sha256(files[name].read_bytes()).hexdigest(), digest)
        with tempfile.TemporaryDirectory(prefix="s04-scenario-") as directory:
            regenerated = Path(directory)
            generate(regenerated)
            for path in [SCENARIO / "manifest.json", *files.values()]:
                other = regenerated / path.relative_to(SCENARIO)
                self.assertEqual(path.read_bytes(), other.read_bytes(), path.name)

    def test_scenario_devices_independent_rules_profiles_and_all_daily_rows(self):
        manifest = json.loads((SCENARIO / "manifest.json").read_text())
        expected = manifest["devices"]
        counts = Counter(
            (key(row["device_id"]), key(row["event_id"]))
            for row in scenario_devices()
        )
        raw_count = accepted = 0
        reasons, missing = Counter(), Counter({name: 0 for name in expected["source_fields"]})
        spellings, slots = set(), set()
        daily = defaultdict(list)
        numbers = []
        start = datetime(2026, 10, 1)
        for row in scenario_devices():
            raw_count += 1
            self.assertEqual(list(row), expected["source_fields"])
            self.assertNotIn(None, row.values())
            self.assertEqual(int(row["export_row_number"]), raw_count)
            missing.update(name for name, value in row.items() if not value.strip())
            spellings.add(row["device_id"])
            device, event = key(row["device_id"]), key(row["event_id"])
            timestamp_text = row["event_time_utc"].strip()
            temperature_text = row["temperature_c"].strip()
            timestamp = None
            try:
                temperature = Decimal(temperature_text)
                numbers.append(temperature)
            except InvalidOperation:
                temperature = None
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp_text):
                try:
                    timestamp = datetime.strptime(timestamp_text, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    pass
            if event:
                slot_index = int(event[1:]) - 1
                day_index, within_day = divmod(slot_index, 50 * 288)
                device_index, minute_slot = divmod(within_day, 288)
                self.assertEqual(device, f"D{device_index + 1:03d}")
                if timestamp is not None:
                    self.assertEqual(timestamp, start + timedelta(
                        days=day_index, minutes=5 * minute_slot
                    ))
            else:
                day_index = (timestamp - start).days
                minute_slot = timestamp.hour * 12 + timestamp.minute // 5
                slot_index = (day_index * 50 + int(device[1:]) - 1) * 288 + minute_slot
            slots.add(slot_index)
            reason = None
            if not device or not event:
                reason = "MISSING_EVENT_KEY"
            elif counts[(device, event)] > 1:
                reason = "DUPLICATE_EVENT"
            elif timestamp is None:
                reason = "INVALID_TIMESTAMP"
            elif temperature is None or not re.fullmatch(r"-?\d{1,3}(\.\d{1,2})?", temperature_text):
                reason = "INVALID_TEMPERATURE"
            elif not Decimal("-40") <= temperature <= Decimal("85"):
                reason = "OUT_OF_RANGE"
            elif not re.fullmatch(r"S\d{2}", row["site_id"]) or row["device_type"] not in (
                "AMBIENT", "COLD_STORE", "PUMP"
            ):
                reason = "MISSING_DEVICE_CONTEXT"
            if reason:
                reasons[reason] += 1
            else:
                accepted += 1
                daily[(
                    timestamp.date().isoformat(), device,
                    row["site_id"], row["device_type"],
                )].append(temperature)
        self.assertEqual(raw_count, expected["raw_rows"])
        self.assertEqual(accepted, expected["accepted_rows"])
        self.assertEqual(sum(reasons.values()), expected["rejected_rows"])
        self.assertEqual(reasons, expected["rejection_counts"])
        self.assertEqual(missing, expected["missing_counts"])
        self.assertEqual(len(spellings), expected["raw_device_spellings"])
        self.assertEqual(len({key(value) for value in spellings}), expected["device_count"])
        self.assertEqual(expected["scheduled_slots"], 50 * 14 * 288)
        self.assertEqual(len(slots), expected["original_events"])
        self.assertEqual(expected["scheduled_slots"] - len(slots), expected["missing_slots"])
        self.assertEqual(raw_count - len(slots), expected["duplicate_extra_rows"])
        self.assertTrue(all(0 <= slot < expected["scheduled_slots"] for slot in slots))
        for minute_slot in range(24, 36):
            self.assertNotIn((6 * 50 + 16) * 288 + minute_slot, slots)
        self.assertEqual(len(numbers), expected["raw_numeric_count"])
        self.assertEqual(min(numbers), Decimal(expected["raw_numeric_min"]))
        self.assertEqual(max(numbers), Decimal(expected["raw_numeric_max"]))
        self.assertEqual(sum(numbers), Decimal(expected["raw_numeric_sum"]))
        computed = []
        for (date, device, site, device_type), values in sorted(daily.items()):
            computed.append({
                "batch_id": expected["batch_id"], "reading_date": date,
                "device_id": device, "site_id": site, "device_type": device_type,
                "reading_count": str(len(values)),
                "min_temperature_c": f"{min(values):.2f}",
                "max_temperature_c": f"{max(values):.2f}",
                "avg_temperature_c": str((sum(values) / len(values)).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )),
            })
        with (SCENARIO / "expected" / "device_daily.csv").open(newline="") as stream:
            self.assertEqual(list(csv.DictReader(stream)), computed)
        self.assertEqual(len(computed), expected["daily_rows"])
        before = daily[("2026-10-06", "D021", "S03", "PUMP")]
        after = daily[("2026-10-08", "D021", "S03", "PUMP")]
        self.assertGreater(sum(after) / len(after) - sum(before) / len(before), Decimal("3.5"))

    def test_scenario_orders_independent_rules_and_all_accepted_lines(self):
        manifest = json.loads((SCENARIO / "manifest.json").read_text())
        expected = manifest["orders"]
        documents = [
            json.loads(line)
            for path in sorted((SCENARIO / "orders").glob("*.jsonl"))
            for line in path.read_text().splitlines()
        ]
        expanded = [
            (document, item)
            for document in documents
            for item in document["lines"] or [None]
        ]
        counts = Counter(
            (key(document["order_id"]), int(item["line_number"]))
            for document, item in expanded if item is not None
        )
        reasons = Counter()
        result = []
        for document, item in expanded:
            customer = document.get("customer", {})
            order_id = key(document.get("order_id", ""))
            line = int(item["line_number"]) if item is not None else None
            date_text = document.get("order_date", "").strip()
            date = None
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_text):
                try:
                    date = datetime.strptime(date_text, "%Y-%m-%d").date()
                except ValueError:
                    pass
            reason = None
            if not order_id:
                reason = "MISSING_ORDER_ID"
            elif line is None or line <= 0:
                reason = "NO_VALID_LINE"
            elif counts[(order_id, line)] > 1:
                reason = "DUPLICATE_LINE"
            elif not all(customer.get(name, "").strip() for name in ("id", "name", "region")):
                reason = "MISSING_CUSTOMER"
            elif date is None:
                reason = "INVALID_ORDER_DATE"
            elif key(document.get("order_status", "")) not in (
                "NEW", "PROCESSING", "SHIPPED", "CANCELLED"
            ):
                reason = "INVALID_ORDER_STATUS"
            elif not key(item.get("sku", "")):
                reason = "MISSING_SKU"
            elif not key(item.get("product", {}).get("category", "")):
                reason = "MISSING_PRODUCT_CATEGORY"
            elif not re.fullmatch(r"[1-9][0-9]{0,5}", item["quantity"].strip()):
                reason = "INVALID_QUANTITY"
            elif not re.fullmatch(r"[0-9]{1,8}(\.[0-9]{1,2})?", item["unit_price"].strip()):
                reason = "INVALID_PRICE"
            if reason:
                reasons[reason] += 1
                continue
            amount = int(item["quantity"]) * Decimal(item["unit_price"])
            result.append({
                "batch_id": expected["batch_id"], "order_id": order_id,
                "line_number": str(line), "order_date": date.isoformat(),
                "order_status": key(document["order_status"]),
                "customer_id": key(customer["id"]), "customer_name": customer["name"].strip(),
                "customer_region": key(customer["region"]),
                "sku": key(item["sku"]),
                "product_category": key(item["product"]["category"]),
                "quantity": str(int(item["quantity"])),
                "unit_price": f"{Decimal(item['unit_price']):.2f}",
                "line_amount": f"{amount:.2f}",
            })
        result.sort(key=lambda row: (row["order_id"], int(row["line_number"])))
        self.assertEqual(len(documents), expected["documents"])
        self.assertEqual(len(expanded), expected["expanded_rows"])
        self.assertEqual(len(result), expected["accepted_rows"])
        self.assertEqual(sum(reasons.values()), expected["rejected_rows"])
        self.assertEqual(reasons, expected["rejection_counts"])
        self.assertEqual(
            sum(Decimal(row["line_amount"]) for row in result),
            Decimal(expected["accepted_line_amount"]),
        )
        self.assertEqual(
            sum("shipping" not in document for document in documents),
            expected["documents_without_shipping"],
        )
        with (SCENARIO / "expected" / "order_lines.csv").open(newline="") as stream:
            self.assertEqual(list(csv.DictReader(stream)), result)

    def test_scenario_notebook_and_warehouse_transfer_contracts(self):
        source = (ROOT / "09_realistic_data_lab.md").read_text()
        tree = ast.parse("\n".join(re.findall(r"```python\n(.*?)```", source, re.DOTALL)))
        assignments = {
            node.targets[0].id: node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
        }
        device_fields = ast.literal_eval(assignments["device_fields"])
        order_fields = ast.literal_eval(assignments["order_fields"])
        daily_fields = list(reversed([
            node.args[0].value for node in ast.walk(assignments["daily_schema"])
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add"
        ]))
        for path in sorted((SCENARIO / "devices").glob("*.csv")):
            with path.open(newline="") as stream:
                self.assertEqual(next(csv.reader(stream)), device_fields)
        setup = (ROOT / "artifacts/sql/scenario_warehouse_setup.sql").read_text()
        for name, fields in (("order_line", order_fields), ("device_daily", daily_fields)):
            with (SCENARIO / "expected" / (
                "order_lines.csv" if name == "order_line" else "device_daily.csv"
            )).open(newline="") as stream:
                self.assertEqual(next(csv.reader(stream)), fields)
            for schema in ("stg", "gold"):
                definition = re.search(
                    rf"CREATE TABLE {schema}\.s04_lab_{name}\s*\((.*?)\n\);",
                    setup, re.DOTALL,
                ).group(1)
                actual = re.findall(r"^\s+(\w+)\s+\w+", definition, re.MULTILINE)
                self.assertEqual(actual, fields + (["published_at_utc"] if schema == "gold" else []))
            publication = (ROOT / "artifacts/sql" / (
                "scenario_publish_orders.sql" if name == "order_line"
                else "scenario_publish_devices.sql"
            )).read_text()
            insertion = re.search(
                rf"INSERT INTO gold\.s04_lab_{name}\s*\((.*?)\)\s*SELECT(.*?)FROM",
                publication, re.DOTALL,
            )
            insert_fields = [field.strip() for field in insertion.group(1).split(",")]
            select_fields = [field.strip() for field in insertion.group(2).split(",")]
            self.assertEqual(insert_fields, fields + ["published_at_utc"])
            self.assertEqual(select_fields, fields + ["SYSUTCDATETIME()"])
        manifest = json.loads((SCENARIO / "manifest.json").read_text())
        orders_sql = (ROOT / "artifacts/sql/scenario_publish_orders.sql").read_text()
        devices_sql = (ROOT / "artifacts/sql/scenario_publish_devices.sql").read_text()
        self.assertIn(f'<> {manifest["orders"]["accepted_rows"]}', orders_sql)
        self.assertIn(f'<> {manifest["orders"]["accepted_line_amount"]}', orders_sql)
        self.assertIn(f'<> {manifest["devices"]["daily_rows"]}', devices_sql)
        self.assertIn(f'<> {manifest["devices"]["accepted_rows"]}', devices_sql)

    def test_order_fixture_acceptance_and_amounts(self):
        documents = [
            json.loads(line)
            for line in (DATA / "orders.jsonl").read_text().splitlines()
        ]
        self.assertEqual(len(documents), 4)
        expanded = [
            (key(document["order_id"]), item)
            for document in documents
            for item in (document["lines"] or [None])
        ]
        counts = Counter(
            (order, int(item["line_number"]))
            for order, item in expanded if item is not None
        )
        accepted = []
        reasons = Counter()
        for order, item in expanded:
            if item is None:
                reasons["NO_VALID_LINE"] += 1
                continue
            line = int(item["line_number"])
            if counts[(order, line)] > 1:
                reasons["DUPLICATE_LINE"] += 1
                continue
            if not re.fullmatch(r"[1-9][0-9]{0,5}", item["quantity"].strip()):
                reasons["INVALID_QUANTITY"] += 1
                continue
            if not re.fullmatch(
                r"[0-9]{1,8}(\.[0-9]{1,2})?", item["unit_price"].strip()
            ):
                reasons["INVALID_PRICE"] += 1
                continue
            quantity = int(item["quantity"])
            price = Decimal(item["unit_price"])
            accepted.append(
                (order, line, key(item["sku"]), quantity, price, quantity * price)
            )
        self.assertEqual(len(expanded), 7)
        self.assertEqual(reasons, {
            "NO_VALID_LINE": 1, "DUPLICATE_LINE": 2, "INVALID_QUANTITY": 1,
        })
        self.assertEqual(accepted, [
            ("O1001", 1, "PUMP-01", 2, Decimal("125.50"), Decimal("251.00")),
            ("O1001", 2, "FILTER-01", 1, Decimal("30.00"), Decimal("30.00")),
            ("O1002", 2, "SEAL-01", 3, Decimal("5.00"), Decimal("15.00")),
        ])
        self.assertEqual(sum(row[-1] for row in accepted), Decimal("296.00"))

    def test_device_fixture_quality_and_daily_results(self):
        with (DATA / "device_readings.csv").open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 9)
        counts = Counter((key(r["device_id"]), key(r["event_id"])) for r in rows)
        daily = defaultdict(list)
        reasons = Counter()
        for row in rows:
            device, event = key(row["device_id"]), key(row["event_id"])
            if counts[(device, event)] > 1:
                reasons["DUPLICATE_EVENT"] += 1
                continue
            try:
                timestamp = datetime.strptime(
                    row["event_time_utc"], "%Y-%m-%dT%H:%M:%SZ"
                )
            except ValueError:
                reasons["INVALID_TIMESTAMP"] += 1
                continue
            try:
                temperature = Decimal(row["temperature_c"])
            except InvalidOperation:
                reasons["INVALID_TEMPERATURE"] += 1
                continue
            if not Decimal("-40") <= temperature <= Decimal("85"):
                reasons["OUT_OF_RANGE"] += 1
                continue
            daily[(device, timestamp.date().isoformat())].append(temperature)
        self.assertEqual(reasons, {
            "DUPLICATE_EVENT": 2, "INVALID_TIMESTAMP": 1,
            "INVALID_TEMPERATURE": 1, "OUT_OF_RANGE": 1,
        })
        result = {
            group: (len(values), min(values), max(values), sum(values) / len(values))
            for group, values in daily.items()
        }
        self.assertEqual(result, {
            ("D01", "2026-10-28"): (
                2, Decimal("20.00"), Decimal("24.00"), Decimal("22.00"),
            ),
            ("D02", "2026-10-28"): (
                2, Decimal("30.00"), Decimal("32.00"), Decimal("31.00"),
            ),
        })

    def test_notebook_cell_python_syntax(self):
        lessons = sorted(ROOT.glob("[0-9][0-9]_*.md"))
        for path in lessons:
            blocks = re.findall(r"```python\n(.*?)```", path.read_text(), re.DOTALL)
            for index, code in enumerate(blocks, 1):
                ast.parse(code, filename=f"{path.name}:cell-{index}")

    def test_device_profile_does_not_confuse_present_with_valid(self):
        with (DATA / "device_readings.csv").open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertTrue(all(value.strip() for row in rows for value in row.values()))
        self.assertEqual(len({row["device_id"] for row in rows}), 3)
        self.assertEqual(len({key(row["device_id"]) for row in rows}), 2)
        numbers = []
        for row in rows:
            try:
                numbers.append(Decimal(row["temperature_c"]))
            except InvalidOperation:
                pass
        self.assertEqual(len(numbers), 8)
        self.assertEqual((min(numbers), max(numbers)), (Decimal("20"), Decimal("200")))
        self.assertEqual(sum(numbers) / len(numbers), Decimal("46.875"))

    def test_device_reader_schema_matches_expanded_fixture(self):
        source = (ROOT / "03_device_telemetry.md").read_text()
        blocks = re.findall(r"```python\n(.*?)```", source, re.DOTALL)
        tree = ast.parse("\n".join(blocks))
        schema = next(
            node.value for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "input_schema"
                for target in node.targets
            )
        )
        fields = [
            field.args[0].value for field in schema.args[0].elts
        ]
        with (DATA / "device_readings.csv").open(newline="") as stream:
            header = next(csv.reader(stream))
        self.assertEqual(fields, header)

    def test_silver_projections_keep_context_without_working_columns(self):
        def projection(filename, variable):
            blocks = re.findall(
                r"```python\n(.*?)```", (ROOT / filename).read_text(), re.DOTALL
            )
            for node in ast.walk(ast.parse("\n".join(blocks))):
                if not isinstance(node, ast.Assign):
                    continue
                if not any(
                    isinstance(target, ast.Name) and target.id == variable
                    for target in node.targets
                ):
                    continue
                calls = [
                    call for call in ast.walk(node.value)
                    if isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Attribute)
                ]
                selects = [call for call in calls if call.func.attr == "select"]
                if not selects:
                    continue
                columns = []
                for argument in selects[0].args:
                    if isinstance(argument, ast.Constant):
                        columns.append(argument.value)
                    elif (
                        isinstance(argument, ast.Call)
                        and isinstance(argument.func, ast.Attribute)
                        and argument.func.attr == "alias"
                    ):
                        columns.append(argument.args[0].value)
                    else:
                        self.fail(f"Unrecognized projection in {filename}: {variable}")
                columns.extend(
                    call.args[0].value for call in calls
                    if call.func.attr == "withColumn"
                )
                return columns
            self.fail(f"No explicit projection found: {filename}: {variable}")

        device_columns = projection("03_device_telemetry.md", "silver_events")
        self.assertIn("firmware_version", device_columns)
        self.assertIn("signal_strength_dbm", device_columns)
        self.assertTrue({
            "batch_id", "device_id", "event_id", "event_time_utc", "temperature_c",
            "source_file", "ingested_at_utc", "quality_rule_version",
        }.issubset(device_columns))
        self.assertFalse({
            "ui_theme", "debug_message", "export_row_number",
            "temperature_text", "event_time_text", "event_key_count", "quality_issue",
        }.intersection(device_columns))

        order_columns = projection("02_nested_json_orders.md", "silver_lines")
        transfer_columns = projection("02_nested_json_orders.md", "transfer")
        warehouse = (ROOT / "04_warehouse_gold.md").read_text()
        stage_definition = re.search(
            r"CREATE TABLE stg\.s04_accepted_order_line\s*\((.*?)\n\);",
            warehouse, re.DOTALL,
        ).group(1)
        stage_columns = re.findall(r"^\s+(\w+)\s+\w+", stage_definition, re.MULTILINE)
        self.assertEqual(transfer_columns, stage_columns)
        self.assertTrue(set(transfer_columns).issubset(order_columns))
        self.assertFalse({
            "raw_json", "item", "quantity_text", "unit_price_text",
            "line_key_count", "quality_issue",
        }.intersection(order_columns))

    def test_local_links_and_code_fences(self):
        sources = list(ROOT.glob("[0-9][0-9]_*.md"))
        sources.extend([
            ROOT.parents[1] / "session_4_blueprint.md",
            ROOT.parents[1] / "README.md",
            DATA / "README.md",
            ROOT / "prerequisites.md",
            ROOT / "notebook_survival_guide.md",
            NOTEBOOKS / "README.md",
        ])
        texts = [(path, path.read_text()) for path in sources]
        for path in NOTEBOOKS.glob("*.ipynb"):
            notebook = json.loads(path.read_text())
            texts.append((path, "\n".join(
                "".join(cell["source"]) for cell in notebook["cells"]
                if cell["cell_type"] == "markdown"
            )))
        for path, text in texts:
            self.assertEqual(text.count("```") % 2, 0, path.name)
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if link.startswith(("http:", "https:")):
                    continue
                name, _, fragment = link.partition("#")
                target = path.parent / name if name else path
                self.assertTrue(target.exists(), (path.name, link))
                if fragment and target.suffix == ".md":
                    anchors = {
                        re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                        for heading in re.findall(r"^#{1,6} (.+)$", target.read_text(), re.M)
                    }
                    self.assertIn(fragment, anchors, (path.name, link))


if __name__ == "__main__":
    print(
        "Offline datasets, regeneration, profile, contract, and syntax checks only; Spark, "
        "Data Wrangler, SQL, copy, and tenant execution remain unverified.",
        flush=True,
    )
    unittest.main(verbosity=2)
