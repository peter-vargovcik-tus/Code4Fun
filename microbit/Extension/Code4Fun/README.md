# Code4Fun MakeCode extension

Student-facing extension package. Appears in the toolbox as **Code4Fun**, similar to **Servos**.

## Blocks

### Gate (main toolbox)

- `gate 1 open` / `gate 1 close`
- `gate 1 is open` / `gate 1 is closed`
- Gates **1–4** are supported (one servo per 3D-printed gate unit)

### Sheep pen (main toolbox)

- `set up gate 1 sheep counter sensor P1 for 3 sheep`
- `count sheep at gate 1`
- `sheep count at gate 1`
- `reset sheep counter at gate 1`

First sheep opens the gate, the gate closes after the chosen number of sheep pass.

### Configuration (under **More...**)

- `set gate 1 servo pin to ...`
- `set gate 1 closed angle to ...`
- `set gate 1 open angle to ...`
- `set gate 1 step size to ... degrees`
- `set gate 1 move delay to ... ms`

Students can use `gate 1 close` immediately — no setup required.

## Publish to GitHub

Push this folder to a public GitHub repo. Repo root should contain `pxt.json`, `gate.ts`, `sheepPen.ts`, and `icon.png`.

Students add it in MakeCode:

1. **Extensions**
2. Paste the GitHub URL in the search box
3. Select **code4fun**

## Import file (offline / classroom)

See [IMPORT.md](IMPORT.md).
