<#
PowerShell script to sync infra/.env variables into Railway using the CLI.
Usage: .\scripts\railway_set_env.ps1 [-EnvFile path] [-Apply]
-Apply: attempt to run the commands using 'railway' CLI (must be installed and linked)
#>
param(
    [string]$EnvFile = "infra/.env",
    [switch]$Apply
)

if (-not (Test-Path $EnvFile)) {
    Write-Error "Arquivo de ambiente '$EnvFile' não encontrado."
    exit 1
}

$outFile = "infra/railway_env_commands.ps1"
"# Railway env commands generated from $EnvFile" | Out-File -FilePath $outFile -Encoding utf8

Get-Content $EnvFile | ForEach-Object {
    $line = $_.Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { return }
    if ($line.StartsWith('#')) { return }
    if ($line -match '^[\s]*([^=\s]+)\s*=\s*(.*)$') {
        $key = $matches[1]
        $val = $matches[2].Trim()
        if (($val.StartsWith('"') -and $val.EndsWith('"')) -or ($val.StartsWith("'") -and $val.EndsWith("'"))) {
            $val = $val.Substring(1, $val.Length - 2)
        }
        $escaped = $val.Replace("'","''")
        $cmd = "railway variables set $key '$escaped'"
        $cmd | Out-File -FilePath $outFile -Append -Encoding utf8
    }
}

Write-Host "Gerado comandos em $outFile"

if ($Apply) {
    if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
        Write-Error "O CLI 'railway' não foi encontrado. Instale e autentique antes de usar -Apply."
        exit 2
    }
    Write-Host "Aplicando variáveis via Railway CLI..."
    Get-Content $outFile | ForEach-Object {
        if ($_ -match '^#' -or [string]::IsNullOrWhiteSpace($_)) { return }
        Write-Host "Executando: $_"
        try {
            iex $_
        } catch {
            Write-Warning "Falha ao executar: $_ - $_"
        }
    }
    Write-Host "Concluído. Verifique os logs da Railway para confirmar."
} else {
    Write-Host "Reveja $outFile e execute manualmente, ou reexecute com -Apply para tentar aplicar automaticamente."
}
