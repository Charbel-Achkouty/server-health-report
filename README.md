# Server Health Report

A small Python script that reads a list of servers from a JSON file, flags the ones that are down or running a high CPU load, and writes the result to a text report.

It skips entries with missing or invalid data instead of crashing, and tells you which entry was skipped and why.

## How it works

1. Reads `servers.json`.
2. Classifies each server:

| Condition | Level |
|---|---|
| Status is `down`, **or** CPU is above 80% | `CRITICAL` |
| CPU is above 70% (and not critical) | `WARNING` |
| Anything else | `OK` (not written to the report) |

3. Writes every `CRITICAL` and `WARNING` server to `report.txt`, followed by a total.
4. Prints how many servers were flagged and how many were skipped.

## Requirements

- Python 3.8 or newer
- No external libraries (standard library only)

## Usage

```
python server_report.py
```

The script reads `servers.json` and writes `report.txt` in the same folder.

## Input format

`servers.json`:

```json
{"servers": [
  {"name": "srv-01", "cpu": 91, "status": "up"},
  {"name": "db-01",  "cpu": 78, "status": "down"},
  {"name": "db-02",  "status": "down"}
]}
```

Each server needs a `name`, a `status` (`up` or `down`) and a numeric `cpu` value.

## Example output

Terminal:

```
Skipping a server, bad data: ValueError("could not convert string to float: 'high'")
Skipping a server, bad data: KeyError('cpu')
Done. Flagged: 4, skipped: 2
```

`report.txt`:

```
srv-01 - CPU 91% - up - CRITICAL
db-01 - CPU 78% - down - CRITICAL
web-01 - CPU 80% - up - WARNING
web-02 - CPU 81% - up - CRITICAL
Total flagged: 4
```

## Error handling

- Missing input file: prints an error that names the file and exits.
- Invalid JSON: prints the error with the line and column and exits.
- A server with a missing key or a non-numeric CPU value: skipped, counted and reported, and the rest of the list is still processed.

## Project structure

```
server-health-report/
  server_report.py   # the script
  servers.json       # sample data
  README.md
  .gitignore         # ignores the generated report.txt
```

## Notes

- All server names and values in `servers.json` are fictional sample data.
- Built while learning Python for infrastructure automation.

## Possible improvements

- Read the file names and thresholds from command-line arguments (`argparse`).
- Add tests with `pytest`.
- Read live server data from an API instead of a JSON file.
- Send the report by email.
