#!/bin/bash
set -euo pipefail

source /root/openclaw/.leveia_paths 2>/dev/null || true
WORKSPACE_DIR="${WORKSPACE_DIR:-/root/openclaw}"
REPO_DIR="${REPO_DIR:-/root/repos/LeveIA_ERC8004}"
REPORT_RELATIVE_PATH="reports/alpha_prediction_latest.json"

cd "$WORKSPACE_DIR"
echo "--- Iniciando Sincronização Alpha Engine ($(date)) ---"
python3 scripts/alpha_engine_simple.py

mkdir -p "$REPO_DIR/reports"
cp "$WORKSPACE_DIR/$REPORT_RELATIVE_PATH" "$REPO_DIR/$REPORT_RELATIVE_PATH"

cd "$REPO_DIR"
git add "$REPORT_RELATIVE_PATH"
git commit -m "data: update alpha prediction $(date +'%Y-%m-%d %H:%M')" || echo "Nenhuma mudança para commit"
git push origin master

echo "--- Sincronização Concluída ---"
