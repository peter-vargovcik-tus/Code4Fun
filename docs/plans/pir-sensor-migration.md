# Code4Fun extension — sensors first, then blocks (v1)

**Status:** In progress — Phase 1 (sensor APIs, no blocks)  
**Last updated:** 2026-07-13

## Phased delivery (agreed)

| Phase | What | Push? |
|-------|------|-------|
| **1 — Sensor APIs** | TypeScript read functions in `sensors.ts`, test from `main.ts` on hardware | After testing |
| **2 — Push** | Commit sensor logic + test demo + docs | Yes |
| **3 — Blocks** | Add `//% block` + `//% subcategory` annotations (HaloHD style) | After block QA in MakeCode |

Do **not** add block annotations until Phase 1 passes on real hardware.

---

## Decisions

- **Drop:** FC-51 laser beam sensor
- **Use:** PIR for sheep/motion at the gate
- **Hardware:** Adeept BBC Micro:bit Sensor Starter Kit (ADB003)
- **v1 sensors:** PIR, Ultrasonic, Limit Switch, Light (+ existing Gate in `gate.ts`)
- **Blocks (Phase 3):** HaloHD `//% subcategory` sub-menus under **Code4Fun**
- **Branding:** TUS logo as extension tile; toolbox category uses TUS colours + nearest Font Awesome icon

---

## Phase 1 — `sensors.ts` (API only, no blocks)

New file: [`microbit/Gate/sensors.ts`](../../microbit/Gate/sensors.ts)

Plain exported functions in the `code4fun` namespace (or `code4funSensors` if we want zero block risk — prefer **same namespace, no `//% block` lines** so nothing appears in toolbox yet).

### PIR Motion (digital)

```typescript
export function pirMotion(pin: DigitalPin): boolean {
    return pins.digitalReadPin(pin) == 1
}
```

### Limit Switch (digital)

```typescript
export function limitSwitchPressed(pin: DigitalPin): boolean {
    return pins.digitalReadPin(pin) == 1
}
```

### Light / photoresistor (analog)

```typescript
export function lightLevel(pin: AnalogPin): number {
    return pins.analogReadPin(pin)
}

export function isDark(pin: AnalogPin, threshold = 300): boolean {
    return pins.analogReadPin(pin) < threshold
}
```

### Ultrasonic (pulse timing)

```typescript
export function ultrasonicCm(trig: DigitalPin, echo: DigitalPin): number {
    pins.digitalWritePin(trig, 0)
    pins.digitalWritePin(trig, 1)
    control.waitMicros(10)
    pins.digitalWritePin(trig, 0)
    const pulse = pins.pulseIn(echo, PulseValue.High, 30000)
    if (pulse <= 0) return 0
    return Math.idiv(pulse * 34, 2000)  // cm, round-trip
}

export function obstacleCloserThanCm(
    trig: DigitalPin, echo: DigitalPin, cm: number
): boolean {
    const d = ultrasonicCm(trig, echo)
    return d > 0 && d < cm
}
```

### Pin defaults (testing)

| Sensor | Default pins |
|--------|----------------|
| Gate servo | P0 |
| PIR | P1 |
| Ultrasonic trig / echo | P1 / P2 |
| Limit switch | P1 |
| Photoresistor | P2 |

---

## Phase 1 — Test harness (`main.ts`)

Update [`microbit/Gate/main.ts`](../../microbit/Gate/main.ts) to exercise sensors before sheep demo:

**Option A — button cycle:** A = show PIR state, B = show light level, shake = ultrasonic cm  
**Option B — sheep demo:** swap FC-51 logic for `code4fun.pirMotion(P1)` with edge trigger

Build locally:

```powershell
cd microbit\Gate
npx makecode build
```

Flash `built/binary.hex` and verify each reading on the LED matrix or serial (if using edge connector serial).

---

## Phase 1 — `pxt.json` (dev project only)

```json
{
  "files": ["gate.ts", "sensors.ts", "main.ts"]
}
```

Extension root [`pxt.json`](../../pxt.json) unchanged until Phase 3 (or Phase 2 if we ship APIs without blocks to GitHub for early import — gate blocks still work).

Update [`deploy-extension.ps1`](../../microbit/deploy-extension.ps1) in Phase 2 to copy `sensors.ts` to extension package + repo root.

---

## Phase 3 — Blocks + sub-menus (after hardware test)

Add to each function:

```typescript
//% subcategory="PIR Motion"
//% blockId=code4fun_pir_motion block="PIR motion on pin %pin"
//% pin.fieldEditor=gridpicker
```

### v1 sub-menus

```text
Code4Fun
  … Gate
  … PIR Motion
  … Ultrasonic
  … Limit Switch
  … Light
```

See HaloHD reference: [`halohd.ts`](https://github.com/KitronikLtd/pxt-kitronik-halohd/blob/master/halohd.ts) uses `//% subcategory="ZIP LEDs"`.

Migrate `gate.ts` from `//% groups` to `//% subcategory="Gate"`.

---

## TUS university logo

### Yes — extension tile (`icon.png`)

MakeCode shows a custom PNG when users add the extension from GitHub.

- Source: [TUS apple-touch-icon](https://tus.ie/app/themes/app-theme/assets/main/fav/apple-touch-icon.png) (castle/gate logo, bronze on white)
- Save as repo root **`icon.png`**
- Reference in [`pxt.json`](../../pxt.json): `"icon": "./icon.png"` (optional but recommended)
- Official gallery approval wants **300×200 px**, &lt;100 KB — resize/pad the 180×180 favicon if submitting to MakeCode approved list
- **GitHub URL import works** with the favicon as-is for camp use

Also keep a source copy: `design/tus-logo.png`

### Toolbox category icon — Font Awesome only

The **left toolbox** category icon (`//% icon="..."` on the namespace) must be a **Font Awesome** unicode character, not a custom PNG.

Workaround for TUS branding:

| Element | Value |
|---------|--------|
| Category colour | `#9B7B4B` (TUS bronze/gold from logo) |
| Toolbox icon | `\uf66f` (university) or `\uf52f` (archway/gate feel) — pick closest FA icon |
| Category label | `block="Code4Fun"` or `block="TUS Code4Fun"` |

Students see the **real TUS logo** in Extensions search / project settings; toolbox uses bronze colour + FA icon.

### Branding note

Camp use under TUS is appropriate; for public extension gallery, follow [TUS brand guidelines](https://tus.ie) if publishing beyond the class repo.

---

## Wiring (Adeept ADB003)

```text
Servo:         signal P0, V+ 5V, GND
PIR:           S → P1, VCC → 3V, GND
Limit switch:  S → P1, VCC → 3V, GND
Photoresistor: S → P2, VCC → 3V, GND
Ultrasonic:    Trig → P1, Echo → P2
```

---

## Phase 1 todos

- [ ] Create `microbit/Gate/sensors.ts` with APIs above (no `//% block`)
- [ ] Add `sensors.ts` to `microbit/Gate/pxt.json`
- [ ] Update `main.ts` — PIR sheep demo + optional sensor test on buttons
- [ ] Download TUS favicon → `design/tus-logo.png` + `icon.png` at repo root
- [ ] Hardware test each sensor on laptop before push
- [ ] Push Phase 1 to GitHub

## Phase 3 todos (later)

- [ ] Add `//% subcategory` block annotations to `gate.ts` + `sensors.ts`
- [ ] Update root `pxt.json`, `deploy-extension.ps1`, version bump
- [ ] Add `TOOLBOX.md`, PIR wiring doc, README updates
- [ ] `deploy-extension.ps1` → verify 5 sub-menus in MakeCode

---

## v2 expansion

Soil Moisture, Water Level, Flame, Line Finder, Buttons, Potentiometer, Joystick, outputs (LED, Buzzer, Motor).
