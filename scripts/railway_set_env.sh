#!/usr/bin/env bash
# Script para sincronizar variáveis do arquivo infra/.env com o Railway (CLI)
# Uso: ./scripts/railway_set_env.sh [-f path/to/.env] [--apply]
# --apply: tenta aplicar as variáveis automaticamente via `railway` CLI

set -euo pipefail
ENV_FILE="${1:-infra/.env}"
APPLY=false
if [[ "${1:-}" == "--apply" || "${2:-}" == "--apply" ]]; then
  APPLY=true
  # allow specifying file as second param
  if [[ -n "${2:-}" && "${2:-}" != "--apply" ]]; then
    ENV_FILE="${2}" || true
  fi
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Arquivo de ambiente não encontrado: $ENV_FILE"
  exit 1
fi

OUT_SH="infra/railway_env_commands.sh"
: > "$OUT_SH"
chmod +x "$OUT_SH"

echo "# Railway env commands generated from $ENV_FILE" > "$OUT_SH"

# helper to strip surrounding quotes
strip_quotes() {
  local v="$1"
  v="${v%\"}"; v="${v#\"}"
  v="${v%\'}"; v="${v#\'}"
  printf "%s" "$v"
}

# Parse ENV file
while IFS= read -r line || [[ -n "$line" ]]; do
  # skip empty and comments
  [[ -z "$line" ]] && continue
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  if [[ "$line" =~ ^[[:space:]]*([^=[:space:]]+)[[:space:]]*=(.*)$ ]]; then
    key="${BASH_REMATCH[1]}"
    val="${BASH_REMATCH[2]}"
    # trim whitespace
    val="$(echo "$val" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    val="$(strip_quotes "$val")"
    # skip blank values if desired? we include them
    printf "railway variables set %s '%s'\n" "$key" "${val//'/\'"'"\'}" >> "$OUT_SH"
  fi
done < "$ENV_FILE"

echo "Gerado comandos em $OUT_SH"

if [ "$APPLY" = true ]; then
  if ! command -v railway >/dev/null 2>&1; then
    echo "O CLI 'railway' não foi encontrado no PATH. Rode o script sem --apply para gerar os comandos e aplique manualmente." >&2
    exit 2
  fi

  echo "Tentando aplicar variáveis via Railway CLI..."
  # Reuse the generated commands
  while IFS= read -r cmd || [[ -n "$cmd" ]]; do
    # skip shebang / comments
    [[ "$cmd" =~ ^# ]] && continue
    echo "Executando: $cmd"
    # Attempt 1: as-is
    if eval "$cmd"; then
      continue
    fi
    # Attempt 2: try alternative syntax 'railway env set KEY VALUE'
    if [[ "$cmd" =~ ^railway[[:space:]]variables[[:space:]]set[[:space:]]([^[:space:]]+)[[:space:]]'(.+)'$ ]]; then
      k="${BASH_REMATCH[1]}"
      v="${BASH_REMATCH[2]}"
      altcmd=(railway env set "$k" "$v")
      echo "Tentando alternativa: \\${altcmd[*]}"
      if "${altcmd[@]}"; then
        continue
      fi
    fi
    echo "Falha ao aplicar: $cmd" >&2
  done < "$OUT_SH"
  echo "Aplicação concluída (verifique mensagens acima para erros)."
else
  echo "Revise o arquivo $OUT_SH e execute manualmente (ou reexecute com --apply)."
fi
