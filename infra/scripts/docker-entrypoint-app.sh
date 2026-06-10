#!/bin/sh
# Example entrypoint for app container: run migrations, create folders
set -e

# create storage dirs
mkdir -p /data/checklist/uploads/imagens
mkdir -p /data/checklist/uploads/assinaturas
mkdir -p /data/checklist/pdfs

# run migrations here if using alembic

exec "$@"
