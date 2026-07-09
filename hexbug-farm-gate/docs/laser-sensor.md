# Laser Beam Sensor

## Module

Camp kits use a low-cost **KY-008** laser transmitter and a separate **LDR receiver** module with analog and digital outputs, as described in the [SriTu Hobby Arduino tutorial](https://srituhobby.com/laser-transmitter-and-receiver-module-with-arduino/).

## Analog sensing (recommended)

The micro:bit reads the receiver **AO** (analog) pin on **P1** (0–1023).

| Condition | How to decide |
|-----------|----------------|
| Beam **clear** | reading vs threshold (depends on module) |
| Beam **blocked** | opposite side of threshold |

Default: beam clear when `reading >= 500`. Calibrate per kit:

1. Note reading with beam clear (button A in test program).
2. Note reading with beam blocked.
3. Set threshold halfway between.
4. Use `set laser clear when reading is above threshold` if clear reads **higher**; set to **false** if clear reads **lower**.

## Wiring on Keyestudio Sensor Shield V2

| Module pin | Connect to |
|------------|------------|
| Transmitter GND | G |
| Transmitter VCC | 5V (shield rail) |
| Transmitter S (signal) | **P2** (default) |
| Receiver GND | G |
| Receiver VCC | 5V |
| Receiver **AO** | **P1** (default) |

Gate servo remains on **P0**. Leave receiver **DO** unconnected when using analog mode.

## Software defaults

- Transmitter pin: **P2**
- Receiver pin: **P1** (analog)
- Threshold: **500**
- Clear when reading **above** threshold: **true**
- Laser auto-on when the first beam check runs

## Safety

Laser modules can harm eyes. Supervise alignment and keep modules away from faces.

## Test program

See [microbit/LaserSensor/test-sensor/README.md](../../microbit/LaserSensor/test-sensor/README.md) for a plain MakeCode test without the extension.
