"""Check the provenance fields of tasks drafted from meeting notes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def compact(text: str) -> str:
    """Collapse whitespace without changing words or punctuation."""
    return " ".join(text.split())


def validate(notes: str, tasks: object) -> list[str]:
    if not isinstance(tasks, list):
        return ["tasks JSON must be an array"]

    errors: list[str] = []
    seen_ids: set[str] = set()
    normalized_notes = compact(notes)

    for index, task in enumerate(tasks, start=1):
        label = f"task {index}"
        if not isinstance(task, dict):
            errors.append(f"{label}: expected an object")
            continue

        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id.strip():
            errors.append(f"{label}: id is required")
        elif task_id in seen_ids:
            errors.append(f"{label}: duplicate id {task_id!r}")
        else:
            seen_ids.add(task_id)
            label = f"task {task_id}"

        title = task.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{label}: title is required")

        if task.get("status") != "candidate":
            errors.append(f"{label}: status must be 'candidate'")

        for field in ("source_quote", "owner_quote", "due_date_quote"):
            quote = task.get(field)
            required = field == "source_quote" or task.get(field.removesuffix("_quote")) is not None
            if required and (not isinstance(quote, str) or not quote.strip()):
                errors.append(f"{label}: {field} is required")
                continue
            if quote is None:
                continue
            if not isinstance(quote, str) or not quote.strip():
                errors.append(f"{label}: {field} must be nonempty text")
                continue
            if compact(quote) not in normalized_notes:
                errors.append(f"{label}: {field} was not found in the meeting notes")

        for field in ("owner", "due_date"):
            value = task.get(field)
            if value is None:
                continue
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}: {field} must be nonempty text")
                continue
            quote = task.get(f"{field}_quote")
            if isinstance(quote, str) and compact(value) not in compact(quote):
                errors.append(f"{label}: {field} text was not found in {field}_quote")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notes", type=Path, help="UTF-8 meeting notes in Markdown")
    parser.add_argument("tasks", type=Path, help="UTF-8 tasks JSON array")
    args = parser.parse_args(argv)

    try:
        notes = args.notes.read_text(encoding="utf-8")
        tasks = json.loads(args.tasks.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2

    errors = validate(notes, tasks)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: checked {len(tasks)} candidate task(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
