# auto-lab environment check
#Requires -Version 5.1

param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$GeneratePy = Join-Path $Root "scripts\\generate_images.py"
$EnvFile = Join-Path $Root ".env"
$EnvExample = Join-Path $Root ".env.example"
$MiniMaxSkill = Join-Path $Root "vendor\\minimax-docx\\SKILL.md"

$script:Status = "READY"
$script:Warnings = 0

function Ok($msg)   { Write-Host "[OK]    $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "[WARN]  $msg" -ForegroundColor Yellow; $script:Warnings++ }
function Fail($msg) { Write-Host "[FAIL]  $msg" -ForegroundColor Red; $script:Status = "NOT READY" }
function Info($msg) { Write-Host "[INFO]  $msg" -ForegroundColor Cyan }

function Read-EnvKeys([string]$Path) {
    $map = @{}
    if (-not (Test-Path $Path)) { return $map }
    foreach ($line in Get-Content $Path -Encoding UTF8) {
        $trim = $line.Trim()
        if (-not $trim -or $trim.StartsWith("#")) { continue }
        $delimiter = if ($trim.Contains("=")) { "=" } elseif ($trim.Contains(":")) { ":" } else { $null }
        if (-not $delimiter) { continue }
        $parts = $trim.Split($delimiter, 2)
        if ($parts.Count -eq 2) {
            $map[$parts[0].Trim()] = $parts[1].Trim()
        }
    }
    return $map
}

Write-Host "=== auto-lab Environment Check ==="
Write-Host "Root: $Root"
Write-Host ""

if (Get-Command python -ErrorAction SilentlyContinue) {
    $pyVersion = & python --version 2>&1
    Ok "python $pyVersion"
} else {
    Fail "python not found"
}

if (Get-Command dotnet -ErrorAction SilentlyContinue) {
    $dotnetVersion = & dotnet --version 2>&1
    Ok "dotnet $dotnetVersion"
} else {
    Fail "dotnet not found"
}

if (Test-Path $GeneratePy) {
    Ok "scripts\\generate_images.py found"
} else {
    Fail "scripts\\generate_images.py missing at $GeneratePy"
}

if (Test-Path $MiniMaxSkill) {
    Ok "minimax-docx skill found"
} else {
    Fail "minimax-docx skill missing at $MiniMaxSkill"
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    try {
        & python -W ignore -c "import json, pathlib, requests, concurrent.futures, docx; print('ok')" *> $null
        if ($LASTEXITCODE -eq 0) {
            Ok "python modules available: requests, python-docx"
        } else {
            Fail "python module check failed"
        }
    } catch {
        Fail "python module check failed: $($_.Exception.Message)"
    }
}

$envKeys = Read-EnvKeys $EnvFile
if (Test-Path $EnvFile) {
    if ($envKeys.ContainsKey("BASEURL") -and $envKeys.ContainsKey("APIKEY")) {
        Ok ".env contains BASEURL and APIKEY"
    } else {
        Fail ".env exists but BASEURL/APIKEY are incomplete"
    }
} else {
    Fail ".env missing"
    if (Test-Path $EnvExample) {
        Warn "copy .env.example to .env and fill real values"
    }
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    try {
        & python (Join-Path $PSScriptRoot "init_run.py") --help *> $null
        if ($LASTEXITCODE -eq 0) {
            Ok "init_run.py executable"
        } else {
            Fail "init_run.py help command failed"
        }
    } catch {
        Fail "init_run.py not executable: $($_.Exception.Message)"
    }

    try {
        & python (Join-Path $PSScriptRoot "run_workflow.py") --help *> $null
        if ($LASTEXITCODE -eq 0) {
            Ok "run_workflow.py executable"
        } else {
            Fail "run_workflow.py help command failed"
        }
    } catch {
        Fail "run_workflow.py not executable: $($_.Exception.Message)"
    }
}

Write-Host ""
if ($script:Status -eq "READY") {
    if ($script:Warnings -gt 0) {
        Write-Host "Status: READY (with $script:Warnings warning(s))" -ForegroundColor Yellow
    } else {
        Write-Host "Status: READY" -ForegroundColor Green
    }
} else {
    Write-Host "Status: NOT READY" -ForegroundColor Red
    exit 1
}
