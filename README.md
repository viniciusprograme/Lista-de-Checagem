# Lista-de-Checagem

Sistema de Checklist de Manutenção (Scaffold)

Scaffold inicial de uma aplicação Flask para coleta de checklists com imagens e assinatura digital.

Setup rápido:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Criar o banco de dados (SQLite):

```powershell
python -m manutencao_checklist.database.init_db
```

Executar aplicação (desenvolvimento):

```powershell
python -m manutencao_checklist.app
```

Variáveis de ambiente (veja `.env.example`).

