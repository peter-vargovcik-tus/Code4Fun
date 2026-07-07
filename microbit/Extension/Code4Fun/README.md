# Code4Fun MakeCode extension

Student-facing extension package. Appears in the toolbox as **Code4Fun**, similar to **Servos**.

## Blocks

### Gate

- `gate open`
- `gate close`
- `gate is open`
- `gate is closed`

### Configuration

- `set gate servo pin to ...` (default P0)
- `set gate closed angle to ...` (default 10)
- `set gate open angle to ...` (default 90)
- `set gate step size to ... degrees` (default 10)
- `set gate move delay to ... ms` (default 60)

Students can use `gate close` immediately — no setup required.

## Publish to GitHub

Push this folder to a public GitHub repo (repo root should contain `pxt.json` and `gate.ts`).

Students add it in MakeCode:

1. **Extensions**
2. Paste the GitHub URL in the search box
3. Select **code4fun**

## Import file (offline / classroom)

See [IMPORT.md](IMPORT.md).
