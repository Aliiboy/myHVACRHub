set -e
set -x

# setup for python-anywhere.com
echo "=== lancement du setup ==="
uv sync
uv pip compile pyproject.toml -o requirements.txt
echo "=== end ==="

