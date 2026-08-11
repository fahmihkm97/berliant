#!/usr/bin/env bash

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
OUTPUT="$ROOT/build/anonymous-artifact"

rm -rf "$OUTPUT"
mkdir -p "$OUTPUT"

git archive HEAD \
  | tar -x -C "$OUTPUT"

rm -f \
  "$OUTPUT/paper/venue_strategy.md"

echo
echo "Anonymous artifact created:"
echo "$OUTPUT"

echo
echo "Running identity audit..."

uv run python \
  experiments/identity_audit.py \
  --root "$OUTPUT"

echo
echo "Anonymous artifact audit passed."
