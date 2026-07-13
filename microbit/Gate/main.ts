/**
 * Photoresistor (light) module test.
 *
 * Wiring (Adeept expansion board):
 * - S   -> P0
 * - VCC -> 3V
 * - GND -> GND
 *
 * Open MakeCode serial monitor to see readings (0-1023).
 * Brighter light usually gives a higher value.
 */

const LIGHT_PIN = AnalogPin.P0

basic.forever(function () {
    const level = code4fun.lightLevel(LIGHT_PIN)
    serial.writeLine("light_level=" + level)
    basic.pause(200)
})
