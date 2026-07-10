const GATE_ID = 1
const SENSOR_PIN = DigitalPin.P1
const SHEEP_LIMIT = 3

code4fun.setupSheepPen(GATE_ID, SENSOR_PIN, SHEEP_LIMIT)
basic.showNumber(0)

basic.forever(function () {
    let count = code4fun.updateSheepPen(GATE_ID)
    basic.showNumber(count)
    basic.pause(50)
})

input.onButtonPressed(Button.A, function () {
    code4fun.resetSheepPen(GATE_ID)
    basic.showNumber(0)
})
