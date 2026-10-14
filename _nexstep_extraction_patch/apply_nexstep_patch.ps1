$ErrorActionPreference = 'Stop'

# Run this script from the NexStep project root. The patch ZIP should first
# be extracted to .\_nexstep_extraction_patch.
$ProjectRoot = (Get-Location).Path
$PatchRoot = $PSScriptRoot

$Files = @(
    'backend\app\ai\extraction\pipeline.py',
    'backend\app\ai\providers\openrouter_provider.py',
    'backend\app\ai\source_verification.py',
    'backend\app\services\ai_exam_discovery_service.py'
)

foreach ($RelativePath in $Files) {
    $Source = Join-Path $PatchRoot $RelativePath
    $Destination = Join-Path $ProjectRoot $RelativePath
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Patch file is missing: $Source"
    }
    if (-not (Test-Path -LiteralPath $Destination -PathType Leaf)) {
        throw "Expected project file is missing: $Destination. Run this script from the NexStep project root."
    }
}

$BackupRoot = Join-Path $ProjectRoot ("_nexstep_extraction_backup_{0}" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
New-Item -ItemType Directory -Path $BackupRoot | Out-Null

foreach ($RelativePath in $Files) {
    $Source = Join-Path $PatchRoot $RelativePath
    $Destination = Join-Path $ProjectRoot $RelativePath
    $Backup = Join-Path $BackupRoot $RelativePath
    $BackupDirectory = Split-Path -Parent $Backup
    New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
    Copy-Item -LiteralPath $Destination -Destination $Backup
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    Write-Host "Patched: $RelativePath" -ForegroundColor Green
}

Write-Host "`nPatch applied. Original files are backed up at: $BackupRoot" -ForegroundColor Cyan
Write-Host 'Next: run the syntax check and follow PATCH_README.md.' -ForegroundColor Cyan
