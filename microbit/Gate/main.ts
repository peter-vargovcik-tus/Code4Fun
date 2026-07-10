const GATE_PIN = AnalogPin.P0
const SENSOR_PIN = DigitalPin.P1
const SHEEP_LIMIT = 3

code4fun.initializeGate(GATE_PIN)
code4fun.setupSheepPen(GATE_PIN, SENSOR_PIN, SHEEP_LIMIT)
basic.showNumber(0)

basic.forever(function () {
    let count = code4fun.updateSheepPen(GATE_PIN, SENSOR_PIN)
    basic.showNumber(count)
    basic.pause(50)
})

input.onButtonPressed(Button.A, function () {
    code4fun.resetSheepPen(GATE_PIN, SENSOR_PIN)
    basic.showNumber(0)
})
