#!/bin/sh
set -e
# Usage: restore.sh /path/to/db.dump /path/to/files.tar.gz
DB_DUMP=$1
FILES_ARCHIVE=$2
if [ -z "$DB_DUMP" ] || [ -z "$FILES_ARCHIVE" ]; then
  echo "Usage: $0 db.dump files.tar.gz"
  exit 1
fi

# Stop services that may write to DB/files before restore in production
# Example restore commands
pg_restore -U ${POSTGRES_USER:-checklist_admin} -d ${POSTGRES_DB:-checklist_db} -v $DB_DUMP

tar xzf $FILES_ARCHIVE -C /data/checklist

echo "Restore complete"
