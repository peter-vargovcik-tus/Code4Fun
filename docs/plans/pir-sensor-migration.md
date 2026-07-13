# Code4Fun extension — HaloHD-style sensor blocks (v1)

**Status:** Planned — not yet implemented  
**Last updated:** 2026-07-13

## Decisions

- **Drop:** FC-51 laser beam sensor (unreliable in practice)
- **Use:** PIR for sheep/motion detection at the gate
- **Toolbox style:** HaloHD sidebar sub-menus via `//% subcategory="..."` (not `groups`)
- **v1 sub-menus:** Gate, PIR Motion, Ultrasonic, Limit Switch, Light (expand later)
- **Hardware:** Adeept BBC Micro:bit Sensor Starter Kit (ADB003) expansion board

## Implementation todos

- [ ] Refactor extension to use `//% subcategory` (HaloHD pattern): Gate, PIR Motion, Ultrasonic, Limit Switch, Light
- [ ] Add `sensors.ts` with digital/analog wrapper blocks and pin pickers; update `pxt.json` files list
- [ ] Update `microbit/Gate/main.ts` to use `code4fun.pirMotion(P1)`; motion==1, edge-trigger + debounce
- [ ] Add `hexbug-farm-gate/docs/pir-sensor-wiring.md` and `microbit/Extension/Code4Fun/TOOLBOX.md`
- [ ] Update README.md, power-and-servo.md, gate-controller-context.md, IMPORT.md
- [ ] Run `deploy-extension.ps1` and verify toolbox sub-menus in MakeCode

## HaloHD vs current Code4Fun

| Mechanism | Where it appears | Code4Fun today |
|-----------|------------------|----------------|
| `//% subcategory="Name"` | **Left toolbox** — clickable sub-items under Code4Fun | Not used |
| `//% groups='[...]'` + `//% group="..."` | **Flyout labels** inside one category panel | Gate, Configuration |
| `//% advanced=true` | Blocks under **More...** in a subcategory | Used for gate config |

Reference: [Kitronik HaloHD halohd.ts](https://github.com/KitronikLtd/pxt-kitronik-halohd/blob/master/halohd.ts)

## How v1 will appear in MakeCode

Left toolbox (sidebar):

```text
  ...
  Radio
  Code4Fun          ◄── main category (purple)
    … Gate
    … PIR Motion
    … Ultrasonic
    … Limit Switch
    … Light
```

## Proposed block API (v1)

### Gate (`gate.ts` — migrate from `group` to `subcategory`)

| Block | Type |
|-------|------|
| `initialize gate on pin %pin` | command |
| `gate open on pin %pin` | command |
| `gate close on pin %pin` | command |
| `gate on pin %pin is open` | boolean |
| `gate on pin %pin is closed` | boolean |
| Config blocks (angles, step, delay) | command, `advanced=true` |

### Sensors (`sensors.ts` — new file)

| Subcategory | Block | Read type |
|-------------|-------|-----------|
| PIR Motion | `PIR motion on pin %pin` | digital `== 1` |
| Ultrasonic | `distance (cm) trig %trig echo %echo` | pulse timing |
| Ultrasonic | `obstacle closer than %cm cm trig %trig echo %echo` | boolean |
| Limit Switch | `limit switch pressed on pin %pin` | digital `== 1` |
| Light | `light level on pin %pin` | analog 0–1023 |
| Light | `is dark on pin %pin` | analog < threshold |

## File structure

```text
microbit/Gate/
  gate.ts       ← gate subcategory blocks
  sensors.ts    ← PIR, Ultrasonic, Limit Switch, Light
  main.ts       ← demo uses code4fun.pirMotion(P1)
  pxt.json      ← files: ["gate.ts", "sensors.ts", "main.ts"]
```

Update `deploy-extension.ps1` to copy `sensors.ts` to extension package and repo root.

## Wiring (Adeept ADB003)

```text
Servo:         signal P0, V+ 5V, GND
PIR:           S → P1, VCC → 3V, GND
Limit switch:  S → P1 (alt demo)
Photoresistor: S → P2, VCC → 3V, GND
Ultrasonic:    Trig → P1, Echo → P2
```

## v2 expansion (later)

Soil Moisture, Water Level, Flame, Line Finder, Buttons, Potentiometer, Joystick, Rotary Encoder, outputs (LED, Buzzer, Motor).

## Verify

```powershell
cd microbit
.\deploy-extension.ps1
```

In MakeCode: add extension → confirm 5 sub-menus under Code4Fun → test PIR reporter in demo project.
