/**
 * Laser sensor analog test — no Code4Fun extension needed.
 *
 * WIRING (Keyestudio Sensor Shield V2):
 *   Transmitter GND -> G
 *   Transmitter VCC -> 5V
 *   Transmitter S   -> P2
 *   Receiver GND    -> G
 *   Receiver VCC    -> 5V
 *   Receiver AO     -> P1   (analog out — not DO)
 *
 * CALIBRATION:
 *   1. Aim laser at receiver, press A to see reading when CLEAR
 *   2. Block beam with your hand, press A again — note the new reading
 *   3. Set THRESHOLD halfway between those two values (edit below)
 *   4. If tick/cross are swapped, set CLEAR_ABOVE to false
 *
 * Buttons:
 *   A = show current analog reading (0-1023)
 *   B = toggle laser on/off
 */

const laserPin = DigitalPin.P2
const sensorPin = AnalogPin.P1
const THRESHOLD = 500
const CLEAR_ABOVE = true

let laserOn = true

pins.digitalWritePin(laserPin, 1)

function isClear(level: number): boolean {
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
