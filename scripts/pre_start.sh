set -e
set -x

# a lancer sur python-anywhere.com


echo "Migration de la base de données..."
alembic upgrade head