# Add Code4Fun extension to MakeCode

## Quick start (works now)

1. Open [makecode.microbit.org](https://makecode.microbit.org/) → **New Project**
2. Click **Extensions**
3. Paste this URL in the search box:

   **https://makecode.microbit.org/_J80c5kDvEWHo**

4. Add the package → **Code4Fun** appears in the toolbox

Drag `gate close` under `on button B pressed` — done.

---

## Why the .hex import failed

CLI-built `.hex` files (from `deploy-extension.ps1`) **do not contain embedded source**. MakeCode shows:

> *This .hex file doesn't contain source*

For **Extensions → Import file**, the teacher must save a `.hex` from the **MakeCode website** after adding the extension once. See [Extension/Code4Fun/IMPORT.md](Extension/Code4Fun/IMPORT.md).

---

## Toolbox blocks

**Code4Fun** → **Gate**

- `gate open`
- `gate close`
- `gate is open`
- `gate is closed`

**Configuration** (optional)

- pin, angles, step size, delay

Defaults work without any Configuration blocks.
