param([Parameter(ValueFromRemainingArguments=$true)][string[]]$LabArgs)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Chay .\setup.ps1 truoc de tao moi truong Python cua Day 7.'
}
Push-Location $projectRoot
try {
    & $pythonPath -B -X utf8 -m src.run @LabArgs
    if ($LASTEXITCODE -ne 0) { throw "Lab failed with exit code $LASTEXITCODE" }
} finally { Pop-Location }
