FROM alpine:3.18
RUN apk add --no-cache bash postgresql-client tar gzip findutils
COPY backup.sh /backup/backup.sh
RUN chmod +x /backup/backup.sh
COPY s3-sync.sh /backup/s3-sync.sh
RUN chmod +x /backup/s3-sync.sh
CMD ["/backup/backup.sh"]
