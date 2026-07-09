# Code4Fun MakeCode extension

Student-facing extension package. Appears in the toolbox as **Code4Fun**, similar to **Servos**.

## Blocks

### Gate (main toolbox)

- `gate open`
- `gate close`
- `gate is open`
- `gate is closed`

### Laser (main toolbox)

- `laser on` / `laser off`
- `laser beam blocked` / `laser beam clear`
- `when laser beam blocked`

### Configuration (under **More...**)

- `set gate servo pin to ...`
- `set gate closed angle to ...`
- `set gate open angle to ...`
- `set gate step size to ... degrees`
- `set gate move delay to ... ms`
- `set laser transmitter pin to ...`
- `set laser receiver pin to ...` (analog)
- `set laser threshold to ...` (0–1023)
- `set laser clear when reading is above threshold ...`

Students can use `gate close` and `laser beam blocked` immediately — no setup required.

## Publish to GitHub

Push this folder to a public GitHub repo. Repo root should contain `pxt.json`, `gate.ts`, `laserSensor.ts`, and `icon.png`.

Students add it in MakeCode:

1. **Extensions**
2. Paste the GitHub URL in the search box
3. Select **code4fun**

## Import file (offline / classroom)

See [IMPORT.md](IMPORT.md).
