param(
    [Parameter(Position = 0)]
    [string]$Component = "All"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $root
$extensionTarget = Join-Path $root "Extension\Code4Fun"
$importBundle = Join-Path $extensionTarget "import-bundle"
$dist = Join-Path $extensionTarget "dist"

$extensionSources = @(
    @{ Folder = "Gate"; File = "gate.ts" },
    @{ Folder = "LaserSensor"; File = "laserSensor.ts" }
)

New-Item -ItemType Directory -Force -Path $extensionTarget | Out-Null
New-Item -ItemType Directory -Force -Path $importBundle | Out-Null
New-Item -ItemType Directory -Force -Path $dist | Out-Null

foreach ($source in $extensionSources) {
    $srcPath = Join-Path (Join-Path $root $source.Folder) $source.File
    if (-not (Test-Path $srcPath)) {
        Write-Error "$($source.File) not found in $($source.Folder)"
        exit 1
    }

    Copy-Item -Path $srcPath -Destination (Join-Path $extensionTarget $source.File) -Force
    Copy-Item -Path $srcPath -Destination (Join-Path $importBundle $source.File) -Force
    Copy-Item -Path $srcPath -Destination (Join-Path $repoRoot $source.File) -Force
    Write-Host "Deployed $($source.Folder)\$($source.File) -> Extension\Code4Fun\"
}

Copy-Item -Path (Join-Path $extensionTarget "pxt.json") -Destination (Join-Path $repoRoot "pxt.json") -Force
Write-Host "Deployed pxt.json -> repo root (for GitHub extension import)"

$gateSource = Join-Path $root "Gate\gate.ts"
$laserDevGate = Join-Path $root "LaserSensor\gate.ts"
if ((Test-Path $gateSource) -and (Test-Path (Join-Path $root "LaserSensor"))) {
    Copy-Item -Path $gateSource -Destination $laserDevGate -Force
    Write-Host "Synced Gate\gate.ts -> LaserSensor\gate.ts (dev project)"
}

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

$devProjects = @("Gate", "LaserSensor")
if ($Component -ne "All") {
    $devProjects = @($Component)
}

foreach ($project in $devProjects) {
    $projectPath = Join-Path $root $project
    if (-not (Test-Path $projectPath)) {
        Write-Warning "Skipping missing dev project: $project"
        continue
    }

    Push-Location $projectPath
    try {
        npx -y makecode build
        if ($LASTEXITCODE -ne 0) {
            Write-Error "$project dev build failed"
            exit 1
        }
        Write-Host "Built $project\built\binary.hex (demo project)"
    }
    finally {
        Pop-Location
    }
}

Write-Host "Done."
