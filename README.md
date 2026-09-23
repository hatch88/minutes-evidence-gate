# minutes-evidence-gate

A small, local checker for action items drafted from meeting notes. It verifies that every quoted source passage exists in the notes before tasks are imported or sent.

The first version checks **provenance and structure**, not whether a proposed task is semantically correct. A human still decides whether the cited passage supports the action, owner, and due date.

## Why this exists

AI meeting summaries can produce plausible tasks with missing evidence, invented owners, or inferred deadlines. This tool gives maintainers a deterministic gate they can place between task extraction and a task system. It never sends data to a network service.

## Quick start

Requires Python 3.10 or newer. No third-party packages.

```sh
python3 action_evidence.py examples/meeting.md examples/tasks.json
```

Exit code `0` means the structural checks passed. Exit code `1` means the draft needs review. Exit code `2` means an input file or JSON structure could not be read.

## Input format

The second argument is a JSON array of task objects:

```json
[
  {
    "id": "MTG-001",
    "title": "Prepare the release checklist",
    "status": "candidate",
    "source_quote": "Maya will prepare the release checklist by Friday.",
    "owner": "Maya",
    "owner_quote": "Maya will prepare the release checklist by Friday.",
    "due_date": "Friday",
    "due_date_quote": "Maya will prepare the release checklist by Friday."
  }
]
```

`owner`, `owner_quote`, `due_date`, and `due_date_quote` are optional. If an owner or due date is supplied, its corresponding quote is required. All quotes must appear in the meeting notes after whitespace normalization. The owner and due date text must appear in their respective quotes. IDs must be unique. All tasks remain `candidate` at this stage; confirmation and completion need separate evidence and are outside this version.

## Current limits

- It does not extract tasks, understand paraphrases, check whether a quote supports a task, or verify that a date was interpreted correctly.
- It reads UTF-8 Markdown and JSON locally. No meeting transcript, customer data, or private project material is bundled with this repository.
- Public examples are fictional. No claim of external adoption is made.

## Roadmap and participation

See [ROADMAP.md](ROADMAP.md) for planned improvements. Reports about false positives, confusing errors, and integration needs are welcome. The project will publish real issue and release history as it develops.

## License

MIT, see [LICENSE](LICENSE).
