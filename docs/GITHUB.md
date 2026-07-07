# GitHub push (TUS token only)

Use a **Personal Access Token** from the **`peter-vargovcik-tus`** GitHub account.  
Do not use your personal `peter-vargovcik` credentials for this repo.

## 1. Create a token (one-time)

1. Sign in to GitHub as **peter-vargovcik-tus**
2. **Settings** → **Developer settings** → **Personal access tokens**
3. Create a token (classic is fine) with scope:
   - `repo` (full control of private repositories)
4. Copy the token — you will not see it again

## 2. Store the token locally (not in git)

In PowerShell, set an environment variable for your session:

```powershell
$env:CODE4FUN_GITHUB_TOKEN = "ghp_your_token_here"
```

Optional — persist for your Windows user only (still separate from personal GitHub):

```powershell
[System.Environment]::SetEnvironmentVariable("CODE4FUN_GITHUB_TOKEN", "ghp_your_token_here", "User")
```

**Never** commit the token or put it in a file in this repository.

## 3. Push

From the repo root:

```powershell
.\scripts\push.ps1
```

Or with upstream tracking on first push:

```powershell
.\scripts\push.ps1 -SetUpstream
```

The script pushes using the TUS token only. The `origin` remote URL stays without embedded credentials.

## 4. MakeCode extension URL (after push)

Students add in **Extensions**:

`https://github.com/peter-vargovcik-tus/Code4Fun`

## Troubleshooting

| Error | Fix |
|-------|-----|
| `denied to peter-vargovcik` | Wrong GitHub account cached — use token script, not default credentials |
| `CODE4FUN_GITHUB_TOKEN` not set | Run the `$env:CODE4FUN_GITHUB_TOKEN = "..."` line first |
| `Repository not found` | Token missing `repo` scope or wrong account |

To clear old personal GitHub credentials (optional):

**Windows Credential Manager** → remove `git:https://github.com` entries for the personal account, then use the token script only for this repo.
