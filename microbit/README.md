# TUS Code4Fun micro:bit software

MakeCode extensions for the Code4Fun camp projects.

## Layout

```text
microbit/
  Gate/                          # develop & test the Gate component
    gate.ts                      # controller + Code4Fun blocks
    main.ts                      # demo (A=open, B=close)
    pxt.json
  Extension/
    Code4Fun/                    # polished extension package (like Servos)
      gate.ts                    # extension source
      pxt.json
      dist/
        code4fun-extension.hex   # import via Extensions → Import file
      import-bundle/             # used to build the hex above
      IMPORT.md                  # student/teacher import guide
  deploy-extension.ps1
```

## Quick start

```powershell
cd microbit
.\deploy-extension.ps1
```

This:

1. Copies `Gate/gate.ts` → `Extension/Code4Fun/`
2. Builds `Extension/Code4Fun/dist/code4fun-extension.hex`
3. Builds `Gate/built/binary.hex` (demo)

## Add Code4Fun blocks in MakeCode

See [Extension/Code4Fun/IMPORT.md](Extension/Code4Fun/IMPORT.md).

**Students:** Extensions → **Import file** → `code4fun-extension.hex`

**Online:** Extensions → paste GitHub URL (after publishing `Extension/Code4Fun/`)

## Toolbox

After import, students see a **Code4Fun** category (like **Servos**) with:

- **Gate** — `gate open`, `gate close`, `gate is open`, `gate is closed`
- **Configuration** — optional pin and angle settings
