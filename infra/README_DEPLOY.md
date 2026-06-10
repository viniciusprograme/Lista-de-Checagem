Deploy checklist infra (Ubuntu 24.04)

1. Install Docker & Docker Compose

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
```

2. Copy env

```bash
cd infra
cp .env.example .env
# edit .env
```

3. Build & up

```bash
docker compose up -d --build
```

4. Obtain TLS certs (example)

```bash
sudo ./scripts/setup-letsencrypt.sh example.com admin@example.com
# copy certs to infra/nginx/certs or mount /etc/letsencrypt
```

5. Optional: configure AWS CLI for backups

```bash
sudo apt install -y awscli
aws configure
```

6. Check services:
- Web: http://localhost
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

7. Restore example

```bash
./scripts/restore.sh /path/db.dump /path/files.tar.gz
```
