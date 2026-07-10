const GATE_PIN = AnalogPin.P0
const SENSOR_PIN = DigitalPin.P1
const SHEEP_LIMIT = 3

let sheepCount = 0
let gateOpened = false
let finished = false
let wasBlocked = false

code4fun.initializeGate(GATE_PIN)
basic.showNumber(0)

basic.forever(function () {
    let blocked = pins.digitalReadPin(SENSOR_PIN) == 0

    if (!finished && blocked && !wasBlocked) {
        sheepCount += 1
        basic.showNumber(sheepCount)

        if (!gateOpened) {
            code4fun.gateOpen(GATE_PIN)
            gateOpened = true
        }

        if (sheepCount >= SHEEP_LIMIT) {
            code4fun.gateClose(GATE_PIN)
            gateOpened = false
            finished = true
        }

        basic.pause(300)
    }

    wasBlocked = blocked
    basic.pause(50)
})

input.onButtonPressed(Button.A, function () {
    sheepCount = 0
    gateOpened = false
    finished = false
    wasBlocked = false
    code4fun.gateClose(GATE_PIN)
    basic.showNumber(0)
})
