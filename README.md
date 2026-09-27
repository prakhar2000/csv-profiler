# CSV profiler

A small tool for the G.E.R.S.O.N. publish flow. `tool.yaml` at the repo root tells the portal the input, the output, and how to build the image.

It reads one CSV and reports the row count, plus how many cells are filled, how many are blank, and one sample value for each column.

## Run locally

```bash
python profile.py --table examples/holdings.csv --out out/profile.json
```

## Run the image

```bash
docker build -t csv-profiler .
docker run --rm \
  -v "$PWD/examples/holdings.csv:/inputs/table:ro" \
  -v "$PWD/out:/outputs" \
  csv-profiler
```

The JSON report is written to `/outputs/profile.json`.
