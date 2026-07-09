# TUS Code4Fun

Code and resources for the TUS Code4Fun camp — autonomous hexbug / bristlebot pen projects.

## MakeCode extension (micro:bit)

Students add the **Code4Fun** blocks in [MakeCode for micro:bit](https://makecode.microbit.org/):

1. Open a project → **Extensions**
2. Paste: `https://github.com/peter-vargovcik-tus/Code4Fun`
3. Add **tus-code4fun**

Toolbox category **Code4Fun** → **Gate** blocks.

See [microbit/Extension/Code4Fun/IMPORT.md](microbit/Extension/Code4Fun/IMPORT.md) for offline and share-link options.

## Repository layout

```text
gate.ts / pxt.json / icon.png   ← MakeCode extension (deployed from microbit/)
microbit/              ← extension development
hexbug-farm-gate/      ← legacy CAD / docs
```

Root `icon.png` is the MakeCode-ready extension icon asset.

## Push to GitHub (TUS token)

Do not use personal GitHub credentials. See [docs/GITHUB.md](docs/GITHUB.md).

```powershell
$env:CODE4FUN_GITHUB_TOKEN = "ghp_..."
.\scripts\push.ps1 -SetUpstream
```

```powershell
cd microbit
.\deploy-extension.ps1
```

This updates `gate.ts` and `pxt.json` at the repo root and rebuilds local test hex files.

## Hardware

Keyestudio Sensor Shield V2, servo on **P0**, jumpers **V1/V2** to **5V**, external shield power.  
See [hexbug-farm-gate/docs/power-and-servo.md](hexbug-farm-gate/docs/power-and-servo.md).
