# Power and Servo Wiring

## Keyestudio Sensor Shield V2 (KS0360)

For this camp setup with the Keyestudio shield:

1. Insert the micro:bit into the shield.
2. Connect the servo to the **P0** 3-pin header:
   - **Signal** (orange/yellow) -> **S**
   - **V+** (red) -> **VCC**
   - **GND** (brown/black) -> **G**
3. Set jumper caps **V1** and **V2** to **5V** (servos need ~5V, not 3.3V).
4. Power the **shield** via:
   - the black **DC jack** (7-9V recommended), or
   - the shield **USB** port (5V)

Do not rely on only the micro:bit’s own battery connector to run a servo. The shield is meant to supply sensor/servo power separately.

See the [Keyestudio Sensor Shield V2 wiki](https://wiki.keyestudio.com/Ks0360_Keyestudio_Sensor_Shield_V2_for_BBC_micro:bit).

## Why the micro:bit may reset or get hot

A 9g servo can draw **much more current** than the micro:bit regulator can supply, especially when:

- the servo is starting to move
- the servo is holding position under load
- the code sends many rapid position updates
- the servo is powered from the micro:bit 3V output

The micro:bit 3V supply is only safe for small loads (on the order of tens to low hundreds of mA depending on model and power source). A servo can easily exceed that.

## Correct wiring

Use this pattern:

- **Servo signal** -> micro:bit `P0`
- **Servo GND** -> common ground with micro:bit
- **Servo V+ (red)** -> external **5V** supply, not the micro:bit 3V pin

The micro:bit should only control the signal pin. The servo motor power should come from a separate 5V source such as:

- a USB power bank through a 5V regulator
- a bench supply
- a battery pack that feeds the Keyestudio shield servo rail, if that rail is truly 5V and not taken from the micro:bit regulator

Always connect grounds together.

## Software power-saving rules

For camp demos, prefer:

1. move in **coarse steps** (for example 8 to 10 degrees)
2. use a **short pause** between steps
3. call **`pins.analogWritePin(P0, 0)`** after the move to stop the PWM pulse
4. do **not** keep sending servo pulses while idle
5. avoid LED animations during movement unless needed

No MakeCode **Servo extension** is required. Use the built-in blocks/API:

- `pins servo write pin ... with value ...`
- `pins analog write pin ... to 0` (stop pulse)

After stopping the pulse, the gate may relax slightly because the servo is no longer holding torque. That is normal and much safer for the board.

## References

- [BBC micro:bit support: Using a servo](https://support.microbit.org/support/solutions/articles/19000101864-using-a-servo-with-the-micro-bit)
- [MakeCode Servos reference](https://makecode.microbit.org/reference/servos)
