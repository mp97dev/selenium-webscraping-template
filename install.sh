#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"

command -v python3 >/dev/null 2>&1 || { echo "python3 not found"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 not found"; exit 1; }

python3 -m venv "${VENV_DIR}"
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
if [ -f "${PROJECT_ROOT}/requirements.txt" ]; then
    python -m pip install -r "${PROJECT_ROOT}/requirements.txt"
fi

echo "Virtual environment created at ${VENV_DIR}"
echo "Run: source ${VENV_DIR}/bin/activate"