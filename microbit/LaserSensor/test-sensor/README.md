# Laser sensor — quick hardware test

Test the KY-008 transmitter + LDR receiver **before** using the Code4Fun extension.

## Which pins?

Use **P1** and **P2** so **P0** stays free for the gate servo later.

| Wire | Connect to shield |
|------|-------------------|
| Transmitter **GND** | **G** |
| Transmitter **VCC** | **5V** |
| Transmitter **S** (signal) | **P2** |
| Receiver **GND** | **G** |
| Receiver **VCC** | **5V** |
| Receiver **AO** (analog out) | **P1** |

Use **AO**, not **DO**. Digital **DO** often does not work reliably with the micro:bit; **AO** gives a 0–1023 level you can compare to a threshold.

Set jumpers **V1** and **V2** to **5V**. Power the shield via USB or DC jack.

**Do not look into the laser.** Align so the red dot hits the receiver LDR.

## Calibrate the threshold

1. Flash the test program below.
2. With the beam **clear**, press **A** — note the value (e.g. `720`).
3. **Block** the beam, press **A** — note the value (e.g. `280`).
4. Pick a **threshold** between them (e.g. `500`).
5. Set `CLEAR_ABOVE`:
   - `true` if clear readings are **higher** than blocked
   - `false` if clear readings are **lower** than blocked

## Option A — paste into MakeCode (JavaScript)

1. Open [makecode.microbit.org](https://makecode.microbit.org)
2. **+ Extensions** — do **not** add Code4Fun for this test
3. Switch to **JavaScript**
4. Paste the code below and adjust `THRESHOLD` / `CLEAR_ABOVE`
5. Download and flash

```javascript
const laserPin = DigitalPin.P2
const sensorPin = AnalogPin.P1
const THRESHOLD = 500      // calibrate with button A
const CLEAR_ABOVE = true     // false if clear reads lower than blocked

let laserOn = true
pins.digitalWritePin(laserPin, 1)

function isClear(level) {
    if (CLEAR_ABOVE) {
        return level >= THRESHOLD
    }
    return level < THRESHOLD
}

basic.forever(function () {
    let level = pins.analogReadPin(sensorPin)
    if (isClear(level)) {
        basic.showIcon(IconNames.Yes)
    } else {
        basic.showIcon(IconNames.No)
    }
    basic.pause(100)
})

input.onButtonPressed(Button.A, function () {
    basic.showNumber(pins.analogReadPin(sensorPin))
})

input.onButtonPressed(Button.B, function () {
    laserOn = !laserOn
    pins.digitalWritePin(laserPin, laserOn ? 1 : 0)
})
```

- **Button A** — show analog reading `0`–`1023`
- **Button B** — laser on/off while aligning

## Option B — build from this repo

```powershell
cd microbit\LaserSensor\test-sensor
npx -y makecode build
```

Flash `built\binary.hex`.

## Troubleshooting

- Reading never changes: check **AO** is on **P1**, laser aimed at LDR, 5V power on module
- Tick/cross swapped: flip `CLEAR_ABOVE` or move threshold
- Flickering: pick a threshold further from both readings, or increase `basic.pause`

When this works, add the **Code4Fun** extension and use `laser beam blocked` with `set laser threshold to ...` under **More...**.
