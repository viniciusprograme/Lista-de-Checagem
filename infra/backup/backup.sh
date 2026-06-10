#!/bin/sh
set -e

# Basic backup script: dumps Postgres and archives static files, then optionally syncs to S3/MinIO
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR=/backup
DB_NAME=${POSTGRES_DB:-checklist_db}
DB_USER=${POSTGRES_USER:-checklist_admin}
DB_PASS=${POSTGRES_PASSWORD}

mkdir -p ${BACKUP_DIR}

# Dump DB
export PGPASSWORD=${DB_PASS}
pg_dump -U ${DB_USER} -F c -b -v -f "${BACKUP_DIR}/db_${TIMESTAMP}.dump" ${DB_NAME}

# Archive static files
tar czf "${BACKUP_DIR}/files_${TIMESTAMP}.tar.gz" -C /data/checklist .

# Retention
find ${BACKUP_DIR} -type f -mtime +90 -delete

# Optionally sync to S3 using awscli (if configured)
if [ -n "${S3_BUCKET}" ]; then
  if command -v aws >/dev/null 2>&1; then
    aws s3 cp ${BACKUP_DIR}/db_${TIMESTAMP}.dump s3://${S3_BUCKET}/backups/
    aws s3 cp ${BACKUP_DIR}/files_${TIMESTAMP}.tar.gz s3://${S3_BUCKET}/backups/
  fi
fi

# Sleep until next run; this container is intended to be scheduled by the host or a cron job in production

