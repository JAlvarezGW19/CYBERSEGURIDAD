#!/usr/bin/env bash
set -euo pipefail

# Get the directory where the script is located
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

# Ensure update_repo.sh exists and is executable
if [ ! -f "./update_repo.sh" ]; then
  echo "Error: update_repo.sh not found in $SCRIPT_DIR"
  exit 1
fi
chmod +x ./update_repo.sh

# Verificar que estamos dentro de un repositorio Git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: $SCRIPT_DIR no es un repositorio Git válido."
  exit 1
fi

# Detect current branch (defaults to main if detection fails)
CURRENT_BRANCH=$(git symbolic-ref --quiet --short HEAD || echo "main")
# Permitir un mensaje de commit personalizado como primer argumento
COMMIT_MSG="${1:-WIP: guardar cambios antes de pull}"

echo "Starting update for branch: $CURRENT_BRANCH"

# Commit local changes before pulling (WIP)
git add -A
if ! git diff --staged --quiet; then
  echo "Realizando commit: $COMMIT_MSG"
  git commit -m "$COMMIT_MSG" || true
else
  echo "No local changes to commit (pre-check)."
fi

# Call update_repo.sh
./update_repo.sh --remote origin --branch "$CURRENT_BRANCH" --push
