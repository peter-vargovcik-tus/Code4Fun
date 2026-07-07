# TUS Code4Fun

Code and resources for the TUS Code4Fun camp — autonomous hexbug / bristlebot pen projects.

## MakeCode extension (micro:bit)

Students add the **Code4Fun** blocks in [MakeCode for micro:bit](https://makecode.microbit.org/):

1. Open a project → **Extensions**
2. Paste: `https://github.com/peter-vargovcik-tus/Code4Fun`
3. Add **tus-code4fun**

Toolbox category **Code4Fun** → **Gate** → `gate open`, `gate close`, …

See [microbit/Extension/Code4Fun/IMPORT.md](microbit/Extension/Code4Fun/IMPORT.md) for offline and share-link options.

## Repository layout

```text
gate.ts / pxt.json     ← MakeCode extension (deployed from microbit/)
microbit/              ← extension development
hexbug-farm-gate/      ← legacy CAD / docs
```

## Develop the Gate extension

```powershell
cd microbit
.\deploy-extension.ps1
```

This updates `gate.ts` and `pxt.json` at the repo root and rebuilds local test hex files.

## Hardware

Keyestudio Sensor Shield V2, servo on **P0**, jumpers **V1/V2** to **5V**, external shield power.  
See [hexbug-farm-gate/docs/power-and-servo.md](hexbug-farm-gate/docs/power-and-servo.md).
