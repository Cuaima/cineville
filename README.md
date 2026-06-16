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

## How to run

Install dependencies with UV:

```bash
uv install --dev
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

It also prints summary stats to stdout:

- Top 5 members by visit count
- Total walk-in count (empty `reservation_id`)

## Testing

```bash
uv run pytest
```

## Notes on AI usage

I used an AI assistant to review the project structure and edge cases while writing the code. All code was written, verified, and understood by me.
