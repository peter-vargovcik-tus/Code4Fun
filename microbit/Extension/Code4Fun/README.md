# Code4Fun MakeCode extension

Student-facing extension package. Appears in the toolbox as **Code4Fun**, similar to **Servos**.

## Blocks

### Gate (main toolbox)

- `initialize gate on pin P0` — gently cycles open/closed to seat the servo safely
- `gate open on pin P0` / `gate close on pin P0`
- `gate on pin P0 is open` / `gate on pin P0 is closed`

Each gate is one 3D-printed unit with its own servo pin.

### Configuration (under **More...**)

- `set gate on pin P0 closed angle to ...`
- `set gate on pin P0 open angle to ...`
- `set gate on pin P0 step size to ... degrees`
- `set gate on pin P0 move delay to ... ms`

Run `initialize gate on pin ...` on start before normal gate use.

Sensor logic (for example counting sheep) belongs in the student project, not in the extension.

## Publish to GitHub

Push this folder to a public GitHub repo. Repo root should contain `pxt.json`, `gate.ts`, and `icon.png`.

Students add it in MakeCode:

1. **Extensions**
2. Paste the GitHub URL in the search box
3. Select **code4fun**

## Import file (offline / classroom)

See [IMPORT.md](IMPORT.md).
