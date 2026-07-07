param(
    [switch]$SetUpstream
)

$token = $env:CODE4FUN_GITHUB_TOKEN
if (-not $token) {
    Write-Error @"
CODE4FUN_GITHUB_TOKEN is not set.

Create a PAT on the peter-vargovcik-tus GitHub account, then run:

  `$env:CODE4FUN_GITHUB_TOKEN = "ghp_..."

See docs/GITHUB.md
"@
    exit 1
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot

$pushUrl = "https://peter-vargovcik-tus:${token}@github.com/peter-vargovcik-tus/Code4Fun.git"

try {
    if ($SetUpstream) {
        git push -u $pushUrl HEAD:main
    } else {
        git push $pushUrl HEAD:main
    }

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host "Push OK (TUS token, no credentials stored in git remote)."
}
finally {
    Pop-Location
}
