param(
    [Parameter(Position = 0)]
    [string]$Component = "Gate"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $root
$source = Join-Path $root $Component
$extensionTarget = Join-Path $root "Extension\Code4Fun"
$gateSource = Join-Path $source "gate.ts"
$importBundle = Join-Path $extensionTarget "import-bundle"
$dist = Join-Path $extensionTarget "dist"

if (-not (Test-Path $gateSource)) {
    Write-Error "gate.ts not found in $source"
    exit 1
}

New-Item -ItemType Directory -Force -Path $extensionTarget | Out-Null
New-Item -ItemType Directory -Force -Path $importBundle | Out-Null
New-Item -ItemType Directory -Force -Path $dist | Out-Null

Copy-Item -Path $gateSource -Destination (Join-Path $extensionTarget "gate.ts") -Force
Copy-Item -Path $gateSource -Destination (Join-Path $importBundle "gate.ts") -Force
Copy-Item -Path $gateSource -Destination (Join-Path $repoRoot "gate.ts") -Force
Copy-Item -Path (Join-Path $extensionTarget "pxt.json") -Destination (Join-Path $repoRoot "pxt.json") -Force

Write-Host "Deployed $Component -> Extension\Code4Fun\gate.ts"
Write-Host "Deployed gate.ts + pxt.json -> repo root (for GitHub extension import)"
Write-Host "Updated import-bundle\gate.ts"

Push-Location $importBundle
try {
    $shareOutput = npx -y makecode share 2>&1 | Out-String
    Write-Host $shareOutput
    if ($shareOutput -match "https://makecode\.microbit\.org/_\w+") {
        $url = $Matches[0]
        Set-Content -Path (Join-Path $extensionTarget "SHARE_URL.txt") -Value $url
        Write-Host "Saved share URL to Extension\Code4Fun\SHARE_URL.txt"
    }

    npx -y makecode build
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Import bundle build failed"
        exit 1
    }
    Copy-Item -Path "built\binary.hex" -Destination (Join-Path $dist "code4fun-flash-only.hex") -Force
    Write-Host "Built Extension\Code4Fun\dist\code4fun-flash-only.hex (flash only, not for MakeCode import)"
}
finally {
    Pop-Location
}

Push-Location (Join-Path $root $Component)
try {
    npx -y makecode build
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Gate dev build failed"
        exit 1
    }
    Write-Host "Built Gate\built\binary.hex (demo project)"
}
finally {
    Pop-Location
}

Write-Host "Done."
