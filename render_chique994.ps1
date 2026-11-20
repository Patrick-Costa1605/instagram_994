$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $root
$ErrorActionPreference = "Stop"

foreach ($parte in @(
    "parte_01.json"
)) {
    python "src/gerar.py" "series/chique_994/partes/$parte"
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao renderizar $parte"
    }
}
