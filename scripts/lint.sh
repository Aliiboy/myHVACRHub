set -e
set -x

echo " === lancement des linters ==="
mypy src
ruff check src
ruff format src --check
echo "=== end ==="