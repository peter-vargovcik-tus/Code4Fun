# LaserSensor component

KY-008 laser transmitter + LDR receiver blocks for the TUS Code4Fun extension.

## Hardware

Based on the [SriTu Hobby laser module tutorial](https://srituhobby.com/laser-transmitter-and-receiver-module-with-arduino/):

- **Transmitter** — visible red laser, 5V, digital on/off on **P2**
- **Receiver** — LDR module; use **AO** (analog) on **P1**, not **DO**

Sensing uses `pins.analogReadPin` (0–1023) and a configurable threshold.

## Default wiring (Keyestudio Sensor Shield V2)

| Part | Pin | Notes |
|------|-----|-------|
| Servo (gate) | P0 | Gate component |
| Laser receiver **AO** | **P1** | analog input |
| Laser transmitter **S** | **P2** | digital output |

Power both modules from the shield **5V** rail (V1/V2 jumpers to 5V).

**Safety:** keep the laser away from eyes and small children.

## Blocks

### Laser

- `laser on` / `laser off`
- `laser beam blocked` / `laser beam clear`
- `when laser beam blocked`
- `laser sensor value` (advanced — raw 0–1023)

### Configuration (More...)

- `set laser threshold to ...`
- `set laser clear when reading is above threshold ...`
- `set laser transmitter pin to ...`
- `set laser receiver pin to ...`

## Test without extension

See [test-sensor/README.md](test-sensor/README.md) to calibrate threshold before using blocks.

## Demo

`main.ts` turns the laser on and shows tick/cross from extension blocks.

```powershell
cd microbit
.\deploy-extension.ps1 -Component LaserSensor
```
