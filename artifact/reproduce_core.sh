#!/usr/bin/env bash

set -euo pipefail

echo "=== Berliant / SCIF v0.0.4 ==="

echo
echo "1. Quality checks"
uv run ruff check .
uv run mypy src
uv run pytest -q

echo
echo "2. Statistical audit"
uv run python experiments/statistical_audit.py

echo
echo "3. Quantitative claim audit"
uv run python experiments/quantitative_claim_audit.py

echo
echo "4. Generate paper figures"
uv run python experiments/make_paper_figures.py

echo
echo "5. Rebuild manuscript"
uv run python experiments/build_manuscript.py

echo
echo "Core artifact reproduction completed."
