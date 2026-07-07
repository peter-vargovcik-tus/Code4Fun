# Gate component (development)

Develop and test the Gate logic here. The polished **Code4Fun** extension is built from this folder.

## Demo

```powershell
cd microbit\Gate
npx makecode build
```

Flash `built\binary.hex` — **A** open, **B** close.

## Deploy extension

```powershell
cd microbit
.\deploy-extension.ps1
```

Updates `Extension/Code4Fun/` and builds `code4fun-extension.hex`.

## Blocks (in Code4Fun extension)

**Gate group:** `gate open`, `gate close`, `gate is open`, `gate is closed`

**Configuration group:** optional pin and angle settings (defaults work out of the box).
