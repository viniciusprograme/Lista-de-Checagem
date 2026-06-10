#!/bin/sh
# Simple rclone/awscli sync helper - expects AWS creds in env
if [ -z "${S3_BUCKET}" ]; then
  echo "S3_BUCKET not configured"
  exit 1
fi

if command -v aws >/dev/null 2>&1; then
  aws s3 sync /data/checklist s3://${S3_BUCKET}/data/checklist --delete
else
  echo "awscli not found"
  exit 1
fi
