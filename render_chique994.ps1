$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $root
$ErrorActionPreference = "Stop"

foreach ($parte in @(
    "parte_03.json"
)) {
    python "src/gerar.py" "series/dicionario_escutista/partes/$parte"
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao renderizar $parte"
    }
}
