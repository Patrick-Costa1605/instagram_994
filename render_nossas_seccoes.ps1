$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $root
$ErrorActionPreference = "Stop"

foreach ($parte in @(
    "1_lobitos.json",
    "2_exploradores.json",
    "3_pioneiros.json",
    "4_caminheiros.json"
)) {
    python "src\gerar.py" "series\nossas_seccoes\partes\$parte"
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao renderizar $parte"
    }
}
