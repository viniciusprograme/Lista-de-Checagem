Infraestrutura Docker para Checklist

Resumo rápido:
- Docker Compose com: nginx, web (FastAPI), postgres, redis, minio, backup, prometheus, grafana
- Volumes persistentes para banco, arquivos e MinIO
- Backup script em infra/backup/backup.sh (usa pg_dump e opcionalmente AWS CLI)

Ação rápida:
1. Copie `.env.example` para `.env` e ajuste variáveis.
2. Ajuste `nginx/conf.d/default.conf` para seu `server_name`.
3. Suba containers:

```bash
cd infra
docker compose up -d --build
```

SSL/Let's Encrypt:
- Este compose assume SSL gerenciado externamente. Para usar certbot, adicione um container certbot e monte `/var/www/certbot`.

S3 vs MinIO:
- MinIO incluído para testes locais. Para produção, configure `S3_BUCKET` + `S3_ACCESS_KEY` + `S3_SECRET_KEY` e altere `backup.sh` para usar AWS credentials.

Backups:
- O container `backup` executa `/backup/backup.sh`. Em produção, recomenda-se agendar com cron no host ou usar uma função Lambda / cronjob no orchestrator.

Monitoramento:
- Prometheus e Grafana incluídos; configure `web` para expor métricas Prometheus em `/metrics`.

Próximos passos:
- Integrar app FastAPI com storage (S3/MinIO) e banco
- Adicionar política de firewall e security group
- Adicionar Let's Encrypt certbot automation
- Testar restore de backup
