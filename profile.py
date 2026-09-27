#!/usr/bin/env python3
"""Profile one CSV file: row count, and filled, blank, and sample value per column."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile a CSV file.")
    parser.add_argument(
        "--table",
        default=os.environ.get("TABLE") or "/inputs/table",
        help="CSV to profile. Default: /inputs/table",
    )
    parser.add_argument(
        "--out",
        default=os.environ.get("OUTPUT_PROFILE") or "/outputs/profile.json",
        help="Where to write the JSON profile.",
    )
    return parser.parse_args()


def profile(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise SystemExit(f"Missing file: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit(f"{path} has no header row")
        fields = list(reader.fieldnames)
        filled = {name: 0 for name in fields}
        blank = {name: 0 for name in fields}
        sample = {name: "" for name in fields}
        rows = 0
        for row in reader:
            rows += 1
            for name in fields:
                value = (row.get(name) or "").strip()
                if value:
                    filled[name] += 1
                    if not sample[name]:
                        sample[name] = value
                else:
                    blank[name] += 1
    return {
        "summary": {
            "rows": rows,
            "columns": len(fields),
            "blank_cells": sum(blank.values()),
        },
        "columns": ["column", "filled", "blank", "sample"],
        "rows": [
            {
                "column": name,
                "filled": filled[name],
                "blank": blank[name],
                "sample": sample[name],
            }
            for name in fields
        ],
    }


def main() -> None:
    args = parse_args()
    report = profile(Path(args.table))
    payload = json.dumps(report, indent=2)
    out = Path(args.out)
    if str(out) not in ("", "-"):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    sys.stdout.write(payload + "\n")
    summary = report["summary"]
    print(
        f"{summary['rows']} rows, {summary['columns']} columns, {summary['blank_cells']} blank cells",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
