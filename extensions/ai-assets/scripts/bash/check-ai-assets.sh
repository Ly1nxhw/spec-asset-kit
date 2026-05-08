#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${PWD}"
FEATURE_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json)
      shift
      ;;
    --feature-dir)
      FEATURE_DIR="${2:-}"
      shift 2
      ;;
    *)
      ROOT_DIR="$1"
      shift
      ;;
  esac
done

if [[ -n "$FEATURE_DIR" ]]; then
  python "$SCRIPT_DIR/../check_ai_assets.py" "$ROOT_DIR" --feature-dir "$FEATURE_DIR"
else
  python "$SCRIPT_DIR/../check_ai_assets.py" "$ROOT_DIR"
fi
