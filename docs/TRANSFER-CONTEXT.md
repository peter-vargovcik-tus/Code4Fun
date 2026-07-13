# Transfer context — continue on desktop

**Date:** 2026-07-13  
**Repo:** `https://github.com/peter-vargovcik-tus/Code4Fun`  
**Local path (laptop):** `C:\Users\peter\Cursor\Code4Fun`

Use this file to pick up where the laptop session left off on your home desktop.

---

## What this project is

TUS **Code4Fun** camp project: micro:bit MakeCode extension for a Hexbug/bristlebot “sheep pen” with a servo-driven gate.

- **Extension:** `gate.ts` at repo root (published for GitHub import as `tus-code4fun` v0.5.0)
- **Dev:** `microbit/Gate/` (source + demo `main.ts`)
- **Deploy:** `cd microbit; .\deploy-extension.ps1`
- **Push:** `$env:CODE4FUN_GITHUB_TOKEN = "ghp_..."; .\scripts\push.ps1` — see [`docs/GITHUB.md`](GITHUB.md)

---

## What we did this session

1. **Explored the repo** — gate extension, CAD legacy, micro:bit workflow
2. **Set up git** — installed Git 2.55, remote `origin` → GitHub, synced to `main` @ `c8cd432`
3. **Hardware shift** — moving from Keyestudio shield + FC-51 laser to **Adeept ADB003** kit
4. **Dropped laser beam** — FC-51 not working reliably; skip it
5. **Chose PIR** — passive IR motion sensor for counting sheep at gate (digital, P1)
6. **Designed extension v1** — HaloHD-style **subcategory** sub-menus (not `groups`)

---

## Current plan

Full plan: [`docs/plans/pir-sensor-migration.md`](plans/pir-sensor-migration.md)

### Phased delivery (latest)

1. **Phase 1 — Sensor APIs** — `sensors.ts` with TypeScript read functions, **no MakeCode blocks yet**; test on hardware via `main.ts`
2. **Phase 2 — Push** — commit + push after hardware test passes
3. **Phase 3 — Blocks** — add `//% subcategory` blocks (HaloHD style), deploy extension

### TUS logo

- **Extension tile:** yes — use `https://tus.ie/app/themes/app-theme/assets/main/fav/apple-touch-icon.png` as repo `icon.png`
- **Toolbox category:** Font Awesome only (not custom PNG); use TUS bronze colour `#9B7B4B` + FA icon

### v1 scope (agreed)

Five MakeCode sidebar sub-menus under **Code4Fun**:

| Sub-menu | Purpose | Digital/Analog |
|----------|---------|----------------|
| Gate | Servo open/close/init (existing blocks) | PWM |
| PIR Motion | Sheep / motion detection | Digital |
| Ultrasonic | Distance, obstacle warning | Pulse |
| Limit Switch | Contact / collision | Digital |
| Light | Photoresistor environment | Analog |

### Key technical decision

Use `//% subcategory="PIR Motion"` on blocks (HaloHD pattern) for **left toolbox sub-items**.  
Current code uses `//% groups` which only labels sections inside the flyout.

### Wiring defaults

```text
Servo  → P0 (5V on expansion board)
PIR    → P1 (3V)
Light  → P2 (3V)
Ultrasonic → Trig P1, Echo P2 (avoid clashes in multi-sensor builds)
```

### Demo logic change (`microbit/Gate/main.ts`)

```typescript
// OLD (FC-51): pins.digitalReadPin(P1) == 0
// NEW (PIR):    code4fun.pirMotion(DigitalPin.P1)  // true when == 1
```

Sheep counting stays in `main.ts`, not the extension.

---

## Next steps on desktop

1. **Clone or pull** the repo:
   ```powershell
   git clone https://github.com/peter-vargovcik-tus/Code4Fun.git
   # or: git pull
   ```

2. **Read the plan:** `docs/plans/pir-sensor-migration.md`

3. **Tell Cursor:** “Implement the plan in `docs/plans/pir-sensor-migration.md`”

4. **Implementation order:**
   - Add `microbit/Gate/sensors.ts` with PIR, Ultrasonic, Limit Switch, Light blocks
   - Refactor `gate.ts`: `group` → `subcategory="Gate"`
   - Update `pxt.json` and `deploy-extension.ps1` for `sensors.ts`
   - Update `main.ts` demo for PIR
   - Update docs (README, PIR wiring, TOOLBOX.md)
   - Run `deploy-extension.ps1`, test in MakeCode

---

## Adeept kit sensor reference

**Digital (0/1):** PIR, buttons, touch, limit switch, line finder, flame  
**Analog (0–1023):** photoresistor, potentiometers, soil moisture, water level, joystick  
**Special:** ultrasonic (pulse), rotary encoder, I2C LCD, NeoPixel ring

Kit docs: https://www.adeept.com/learn/tutorial-112.html

---

## Git state at handoff

- Branch: `main`, tracking `origin/main`
- Remote: `https://github.com/peter-vargovcik-tus/Code4Fun.git`
- Git installed on laptop; set `user.name` / `user.email` locally if not done yet

---

## Open questions for home

- Exact desktop repo path (clone fresh or existing copy?)
- Test PIR with real Hexbugs — may need sensor close to path (low heat)
- PIR warm-up ~30–60 s after power-on
