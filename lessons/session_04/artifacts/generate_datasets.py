"""Rebuild the deterministic Session 04 main-lab inputs and expected results.

Run from the repository root:
    python lessons/session_04/artifacts/generate_datasets.py
No network, third-party packages, timestamps, or credentials are used.
"""

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import random


START = datetime(2026, 10, 1)
DAYS = 14
DEVICE_BATCH = "s04-lab-devices-001"
ORDER_BATCH = "s04-lab-orders-001"
DEVICE_FIELDS = [
    "device_id", "event_id", "event_time_utc", "temperature_c",
    "firmware_version", "signal_strength_dbm", "ui_theme", "debug_message",
    "export_row_number", "site_id", "device_type",
]
ORDER_FIELDS = [
    "batch_id", "order_id", "line_number", "order_date", "order_status",
    "customer_id", "customer_name", "customer_region", "sku",
    "product_category", "quantity", "unit_price", "line_amount",
]
DAILY_FIELDS = [
    "batch_id", "reading_date", "device_id", "site_id", "device_type",
    "reading_count", "min_temperature_c", "max_temperature_c",
    "avg_temperature_c",
]


def money(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def generate(output):
    for folder in ("devices", "orders", "expected"):
        (output / folder).mkdir(parents=True, exist_ok=True)
    device_rng = random.Random(4204)
    order_rng = random.Random(4304)
    device_reasons = Counter()
    order_reasons = Counter()
    daily = defaultdict(list)
    order_expected = []
    raw_devices = original_events = missing_slots = expanded_orders = 0
    numeric_temperatures = []
    missing_values = Counter({field: 0 for field in DEVICE_FIELDS})
    raw_spellings = set()
    order_total = Decimal("0.00")
    optional_shipping = 0
    source_files = []
    hourly_shape = [
        -20, -22, -24, -25, -24, -20, -12, -4, 4, 10, 16, 20,
        24, 26, 24, 20, 14, 8, 2, -4, -10, -14, -16, -18,
    ]

    for day in range(DAYS):
        date = START + timedelta(days=day)
        path = output / "devices" / f"readings_{date:%Y-%m-%d}.csv"
        source_files.append(path)
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream, fieldnames=DEVICE_FIELDS, lineterminator="\n"
            )
            writer.writeheader()
            for device in range(1, 51):
                site = f"S{(device - 1) // 10 + 1:02d}"
                device_type = ("AMBIENT", "COLD_STORE", "PUMP")[(device - 1) % 3]
                base_tenths = {"AMBIENT": 220, "COLD_STORE": 50, "PUMP": 380}[
                    device_type
                ]
                for slot in range(288):
                    index = (day * 50 + device - 1) * 288 + slot
                    if index % 199 == 0 or (
                        device == 17 and day == 6 and 24 <= slot < 36
                    ):
                        missing_slots += 1
                        continue
                    original_events += 1
                    timestamp = date + timedelta(minutes=5 * slot)
                    firmware = (
                        "2.2" if site == "S03" and (day > 6 or (
                            day == 6 and slot >= 144
                        )) else "2.1"
                    )
                    tenths = (
                        base_tenths + hourly_shape[slot // 12]
                        + (device % 5) * 3 + device_rng.randint(-12, 12)
                        + (40 if firmware == "2.2" else 0)
                    )
                    temperature = Decimal(tenths) / 10
                    row = {
                        "device_id": (
                            f" d{device:03d} " if index % 17 == 0
                            else f"D{device:03d}"
                        ),
                        "event_id": f"E{index + 1:07d}",
                        "event_time_utc": f"{timestamp:%Y-%m-%dT%H:%M:%SZ}",
                        "temperature_c": f"{temperature:.2f}",
                        "firmware_version": firmware,
                        "signal_strength_dbm": str(
                            -55 - device % 20 - device_rng.randint(0, 9)
                        ),
                        "ui_theme": "dark" if device % 2 else "light",
                        "debug_message": "render_ok, cached" if slot % 2 else "render_ok",
                        "export_row_number": "",
                        "site_id": site,
                        "device_type": device_type,
                    }
                    kind = index % 1000
                    reason = None
                    copies = 1
                    if kind < 5:
                        row["event_time_utc"] = "not a timestamp"
                        reason = "INVALID_TIMESTAMP"
                    elif kind < 10:
                        row["temperature_c"] = "sensor error"
                        reason = "INVALID_TEMPERATURE"
                    elif kind < 15:
                        row["temperature_c"] = "200.00"
                        reason = "OUT_OF_RANGE"
                    elif kind < 20:
                        row["temperature_c"] = ""
                        reason = "INVALID_TEMPERATURE"
                    elif kind < 25:
                        copies = 2
                        reason = "DUPLICATE_EVENT"
                    elif kind < 30:
                        row["event_id"] = ""
                        reason = "MISSING_EVENT_KEY"
                    elif kind < 35:
                        row["signal_strength_dbm"] = ""
                    if reason is None:
                        daily[(f"{date:%Y-%m-%d}", f"D{device:03d}", site,
                               device_type)].append(temperature)
                    else:
                        device_reasons[reason] += copies
                    for _ in range(copies):
                        raw_devices += 1
                        row["export_row_number"] = str(raw_devices)
                        writer.writerow(row)
                        raw_spellings.add(row["device_id"])
                        missing_values.update(
                            field for field, value in row.items() if not value.strip()
                        )
                        if row["temperature_c"] not in ("", "sensor error"):
                            numeric_temperatures.append(Decimal(row["temperature_c"]))

    products = [
        ("PUMP-01", "PUMPS", 12550), ("PUMP-02", "PUMPS", 22500),
        ("FILTER-01", "FILTERS", 3000), ("FILTER-02", "FILTERS", 4250),
        ("VALVE-01", "VALVES", 2500), ("VALVE-02", "VALVES", 6875),
        ("SEAL-01", "PARTS", 500), ("SEAL-02", "PARTS", 850),
        ("GAUGE-01", "PARTS", 1000), ("GAUGE-02", "PARTS", 1875),
        ("FILTER-03", "FILTERS", 5575), ("VALVE-03", "VALVES", 9510),
    ]
    documents_by_day = defaultdict(list)
    for number in range(1, 5001):
        day = (number - 1) % DAYS
        date = START + timedelta(days=day)
        customer = (number - 1) % 100 + 1
        region = ("NORTH", "SOUTH", "EAST", "WEST")[(customer - 1) % 4]
        status = ("NEW", "PROCESSING", "SHIPPED", "CANCELLED")[number % 4]
        document = {
            "order_id": f" o{number:06d} " if number % 17 == 0 else f"O{number:06d}",
            "order_date": f"{date:%Y-%m-%d}",
            "order_status": status,
            "customer": {
                "id": f"C{customer:04d}",
                "name": f"Contoso Customer {customer:03d}",
                "region": region,
            },
            "lines": [],
            "ui_theme": "dark",
            "debug_message": "export_ok",
        }
        if number % 5:
            document["shipping"] = {
                "address": {"city": f"{region.title()}port", "country": "US"},
                "service_level": "EXPRESS" if number % 3 == 0 else "STANDARD",
            }
        else:
            optional_shipping += 1
        for line in range(1, order_rng.randint(1, 5) + 1):
            sku, category, price = order_rng.choice(products)
            item = {
                "line_number": str(line),
                "sku": f" {sku.lower()} " if number % 11 == 0 else sku,
                "quantity": str(order_rng.randint(1, 12)),
                "unit_price": money(price),
                "product": {"category": category},
                "display_label": f"{sku} x line {line}",
            }
            if number % 7:
                item["product"]["description"] = f"Synthetic {sku.lower()}"
            document["lines"].append(item)

        kind = number % 100
        if kind == 0:
            document["lines"] = []
        elif kind == 1:
            document["lines"][0]["quantity"] = "not provided"
        elif kind == 2:
            document["lines"][0]["unit_price"] = "$12.00"
        elif kind == 3:
            document["lines"].append(
                json.loads(json.dumps(document["lines"][0]))
            )
        elif kind == 4:
            document["lines"][0]["sku"] = ""
        elif kind == 5:
            document["customer"]["id"] = ""
        elif kind == 6:
            document["order_date"] = "not a date"
        elif kind == 7:
            document["lines"][0]["product"]["category"] = ""

        for item in document["lines"] or [None]:
            expanded_orders += 1
            reason = None
            if item is None:
                reason = "NO_VALID_LINE"
            elif kind == 3 and item["line_number"] == "1":
                reason = "DUPLICATE_LINE"
            elif kind == 5:
                reason = "MISSING_CUSTOMER"
            elif kind == 6:
                reason = "INVALID_ORDER_DATE"
            elif item["line_number"] == "1":
                reason = {
                    1: "INVALID_QUANTITY", 2: "INVALID_PRICE",
                    4: "MISSING_SKU", 7: "MISSING_PRODUCT_CATEGORY",
                }.get(kind)
            if reason:
                order_reasons[reason] += 1
                continue
            amount = int(item["quantity"]) * Decimal(item["unit_price"])
            order_total += amount
            order_expected.append({
                "batch_id": ORDER_BATCH,
                "order_id": document["order_id"].strip().upper(),
                "line_number": item["line_number"],
                "order_date": document["order_date"],
                "order_status": status,
                "customer_id": document["customer"]["id"],
                "customer_name": document["customer"]["name"],
                "customer_region": region,
                "sku": item["sku"].strip().upper(),
                "product_category": item["product"]["category"],
                "quantity": item["quantity"],
                "unit_price": item["unit_price"],
                "line_amount": f"{amount:.2f}",
            })
        documents_by_day[date].append(document)

    for date, documents in sorted(documents_by_day.items()):
        path = output / "orders" / f"orders_{date:%Y-%m-%d}.jsonl"
        source_files.append(path)
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            for document in documents:
                stream.write(json.dumps(document, separators=(",", ":")) + "\n")

    daily_expected = []
    for (date, device, site, device_type), values in sorted(daily.items()):
        mean = (sum(values) / len(values)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        daily_expected.append({
            "batch_id": DEVICE_BATCH, "reading_date": date,
            "device_id": device, "site_id": site, "device_type": device_type,
            "reading_count": len(values), "min_temperature_c": f"{min(values):.2f}",
            "max_temperature_c": f"{max(values):.2f}", "avg_temperature_c": str(mean),
        })
    order_expected.sort(key=lambda row: (row["order_id"], int(row["line_number"])))
    write_csv(output / "expected" / "device_daily.csv", DAILY_FIELDS, daily_expected)
    write_csv(output / "expected" / "order_lines.csv", ORDER_FIELDS, order_expected)
    manifest = {
        "dataset_version": "s04-scenario-v1",
        "seeds": {"devices": 4204, "orders": 4304},
        "start_date": "2026-10-01", "end_date": "2026-10-14",
        "devices": {
            "batch_id": DEVICE_BATCH, "scheduled_slots": 50 * DAYS * 288,
            "missing_slots": missing_slots, "original_events": original_events,
            "duplicate_extra_rows": raw_devices - original_events,
            "raw_rows": raw_devices, "accepted_rows": sum(map(len, daily.values())),
            "rejected_rows": sum(device_reasons.values()),
            "rejection_counts": dict(sorted(device_reasons.items())),
            "daily_rows": len(daily_expected), "device_count": 50,
            "raw_device_spellings": len(raw_spellings),
            "source_fields": DEVICE_FIELDS,
            "missing_counts": dict(sorted(missing_values.items())),
            "raw_numeric_count": len(numeric_temperatures),
            "raw_numeric_min": str(min(numeric_temperatures)),
            "raw_numeric_max": str(max(numeric_temperatures)),
            "raw_numeric_sum": str(sum(numeric_temperatures)),
        },
        "orders": {
            "batch_id": ORDER_BATCH, "documents": 5000,
            "expanded_rows": expanded_orders, "accepted_rows": len(order_expected),
            "rejected_rows": sum(order_reasons.values()),
            "rejection_counts": dict(sorted(order_reasons.items())),
            "accepted_line_amount": f"{order_total:.2f}",
            "documents_without_shipping": optional_shipping,
        },
        "files": {
            path.relative_to(output).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(source_files + list((output / "expected").glob("*.csv")))
        },
    }
    with (output / "manifest.json").open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parent / "data" / "scenario",
    )
    args = parser.parse_args()
    result = generate(args.output)
    print(json.dumps({
        "devices": result["devices"], "orders": result["orders"],
        "output": str(args.output),
    }, indent=2))
