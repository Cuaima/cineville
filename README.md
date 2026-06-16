# Cineville CSV Processor

A small Python CLI for processing membership visit data.

- Reads `members.csv` and `visits.csv`
- Validates that every visit has a barcode and that the barcode exists in members
- Groups visit IDs by member
- Writes output as `member_id,barcode,visit_ids`
- Prints bonus stats: top 5 members by visit count and total walk-ins

## Project structure

- `src/` — application code
- `tests/` — pytest unit tests
- `data/` — default input file location
- `output/` — default output file location
- `logs/` — optional runtime logs
- `docs/` — data model diagram

## Data Model

![Data model](docs/data_model.svg)

## How to run

Install dependencies with UV:

```bash
uv sync
```

Run the script with defaults:

```bash
uv run python -m src.main
```

Override input/output paths:

```bash
uv run python -m src.main --members data/members.csv --visits data/visits.csv --output output/result.csv
```

## Output

The script writes a CSV with these columns:

- `member_id`
- `barcode`
- `visit_ids` — serialized JSON array of visit IDs

The `visit_ids` column is a JSON array (e.g. `["v1","v2"]`) so it remains
machine-readable when embedded in a single CSV cell.

It also prints summary stats to stdout:

- Top 5 members by visit count
- Total walk-in count (empty `reservation_id`)

## Testing

```bash
uv run pytest
```

## Notes on AI usage

I used Claude (Anthropic) as a sounding board throughout this project. Specifically:

- **Architecture decisions** — I discussed whether to use a web framework (FastAPI/Django) or a plain CLI script, and whether to split the code into multiple modules or keep it in a single file
- **Initial scaffolding** — After deciding on the project structure, GitHub Copilot generated a first template of the project structure and boilerplate code, which I used as a starting point
- **Code review** — I used it to review each module for edge cases, error handling gaps, and inconsistencies I missed in my own review of the boilerplate (e.g. catching the frozen dataclass / mutable list inconsistency in models.py)
- **Validation logic** — I discussed where validation should live (the AI wanted to put all validation logic in the validator, but I wanted to do a preliminary preprocessing step in the reader to avoid creating obviously invalid objects) and how to structure the required fields check cleanly
- **Documentation** — I used it to review docstrings and the README for clarity

All code was written, understood, and is explainable by me.
