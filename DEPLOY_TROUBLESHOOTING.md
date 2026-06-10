# DEPLOY_TROUBLESHOOTING.md

# Correção Automática de Falhas de Deploy

## Objetivo
Garantir que a aplicação Python (FastAPI/Flask) consiga iniciar corretamente em ambientes de hospedagem como:

- Railway
- Render
- Fly.io
- VPS Linux
- AWS
- Azure
- Google Cloud

O sistema deve detectar, registrar e corrigir automaticamente erros comuns de implantação.

---

# Problema Identificado
Mensagem apresentada:

```
Application failed to respond

This error appears to be caused by the application.
```
Isso indica que a plataforma conseguiu iniciar o container ou processo, porém a aplicação não respondeu dentro do tempo esperado.

---

# Correções Obrigatórias

## 1. Porta Dinâmica
A aplicação NUNCA deverá utilizar porta fixa.

ERRADO:

```
uvicorn.run(app, host="0.0.0.0", port=8000)
```
CORRETO:

```
import os

PORT = int(os.environ.get("PORT", 8000))

uvicorn.run(
    app,
    host="0.0.0.0",
    port=PORT
)
```

---

# 2. Health Check
Criar endpoint obrigatório:

```
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }
```
Objetivo:

Permitir que Railway, Render e Load Balancers validem que a aplicação está funcionando.

---

# 3. Startup Seguro
Evitar execução pesada durante inicialização.

NÃO EXECUTAR:

- Geração de relatórios.
- Backup.
- Leitura de milhares de arquivos.
- Processamento de imagens.
- Envio de e-mails.

durante:

```
startup()
```
Essas tarefas deverão ser movidas para:

- Background Tasks
- Celery
- Redis Queue

---

# 4. Dependências
Criar arquivo:

```
requirements.txt
```
Gerado automaticamente:

```
pip freeze > requirements.txt
```
Verificar obrigatoriamente:

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-multipart
jinja2
reportlab
openpyxl
pillow
python-dotenv
passlib
bcrypt
```

---

# 5. Banco de Dados

## Desenvolvimento
Permitir SQLite.

## Produção
Utilizar PostgreSQL.

Leitura:

```
DATABASE_URL = os.getenv("DATABASE_URL")
```
Se inexistente:

```
usar SQLite
```
Se existir:

```
usar PostgreSQL
```

---

# 6. Variáveis de Ambiente
Implementar validação automática.

Exemplo:

```
required_vars = [
    "JWT_SECRET"
]

for var in required_vars:
    if not os.getenv(var):
        raise RuntimeError(
            f"Variável obrigatória ausente: {var}"
        )
```

---

# 7. Logs
Criar logs estruturados.

Arquivo:

```
logs/app.log
```
Registrar:

- Inicialização.
- Falhas.
- Uploads.
- Envio de e-mails.
- Erros SQL.

---

# 8. Tratamento de Exceções
Criar middleware global.

Exemplo:

```
@app.exception_handler(Exception)
async def global_exception_handler(
    request,
    exc
):
    logger.error(str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc)
        }
    )
```

---

# 9. Docker
Obrigatório.

Arquivo:

```
Dockerfile
```
Exemplo:

```
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

CMD ["uvicorn",
     "main:app",
     "--host",
     "0.0.0.0",
     "--port",
     "8000"]
```

---

# 10. Docker Compose
Criar:

```
docker-compose.yml
```
Serviços:

- app
- postgres
- redis

---

# 11. Arquivos Persistentes
Criar volumes para:

```
/uploads
/pdfs
/logs
/backups
```
Nunca armazenar arquivos importantes apenas dentro do container.

---

# 12. Verificação Automática
Ao iniciar:

```
Verificar:
```

- Banco acessível.
- Diretórios existentes.
- SMTP configurado.
- Espaço em disco.
- Permissões de escrita.

---

# 13. SMTP
Caso SMTP falhe:

NÃO derrubar aplicação.

Registrar erro:

```
Falha SMTP
```
e continuar execução.

---

# 14. Uploads
Validar:

Extensões:

```
jpg
jpeg
png
webp
pdf
```
Limite:

```
10 MB
```

---

# 15. Monitoramento
Criar endpoint:

```
/health
```
Criar endpoint:

```
/metrics
```
Compatível com:

- Prometheus
- Grafana

---

# 16. Recuperação Automática
Implementar reinício automático.

Docker:

```
restart: unless-stopped
```

---

# 17. Segurança
Implementar:

- HTTPS
- JWT
- bcrypt
- CORS controlado
- Rate Limit

---

# 18. Teste Pré-Deploy
Executar automaticamente:

```
pytest
```
e

```
python -m compileall .
```
Falha em qualquer teste:

```
Bloquear deploy
```

---

# Critérios de Aceitação
A aplicação somente poderá ser considerada pronta para produção quando:

✓ Iniciar sem erros.

✓ Responder em menos de 5 segundos.

✓ Health check retornar 200.

✓ Banco conectado.

✓ Logs funcionando.

✓ Upload funcionando.

✓ PDF funcionando.

✓ SMTP funcionando.

✓ Container reiniciar automaticamente.

✓ Deploy em Railway ou Render concluir sem apresentar:

"Application failed to respond".

✓ Todos os erros serem registrados em logs para diagnóstico futuro.
