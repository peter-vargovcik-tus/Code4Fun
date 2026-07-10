class SheepPenController {
    private gatePin: AnalogPin
    private sensorPin: DigitalPin
    private limit: number
    private count: number
    private gateOpened: boolean
    private finished: boolean
    private wasBlocked: boolean
    private configured: boolean

    constructor() {
        this.gatePin = AnalogPin.P0
        this.sensorPin = DigitalPin.P1
        this.limit = 3
        this.count = 0
        this.gateOpened = false
        this.finished = false
        this.wasBlocked = false
        this.configured = false
    }

    matchesPins(gatePin: AnalogPin, sensorPin: DigitalPin): boolean {
        return this.gatePin == gatePin && this.sensorPin == sensorPin
    }

    configure(gatePin: AnalogPin, sensorPin: DigitalPin, limit: number) {
        this.gatePin = gatePin
        this.sensorPin = sensorPin
        if (limit < 1) {
            this.limit = 1
        } else {
            this.limit = limit
        }
        this.configured = true
    }

    tick(): number {
        if (!this.configured) {
            return this.count
        }

        let blocked = pins.digitalReadPin(this.sensorPin) == 0

        if (!this.finished && blocked && !this.wasBlocked) {
            this.count += 1

            if (!this.gateOpened) {
                code4fun.gateOpen(this.gatePin)
                this.gateOpened = true
            }

            if (this.count >= this.limit) {
                code4fun.gateClose(this.gatePin)
                this.gateOpened = false
                this.finished = true
            }

            basic.pause(300)
        }

        this.wasBlocked = blocked
        return this.count
    }

    getCount(): number {
        return this.count
    }

    isFinished(): boolean {
        return this.finished
    }

    reset(): void {
        this.count = 0
        this.gateOpened = false
        this.finished = false
        this.wasBlocked = false
        code4fun.gateClose(this.gatePin)
    }
}

let _sheepPenList: SheepPenController[] = []

function sheepPenByPins(gatePin: AnalogPin, sensorPin: DigitalPin): SheepPenController {
    for (let i = 0; i < _sheepPenList.length; i++) {
        if (_sheepPenList[i].matchesPins(gatePin, sensorPin)) {
            return _sheepPenList[i]
        }
    }

    let pen = new SheepPenController()
    pen.configure(gatePin, sensorPin, 3)
    _sheepPenList.push(pen)
    return pen
}

namespace code4fun {
    /**
     * Set up a sheep counter for a gate pin and sensor pin.
     */
    //% blockId=code4fun_setup_sheep_pen_pins block="set up sheep counter gate pin %gatePin sensor %sensorPin for %limit sheep"
    //% group="Sheep pen"
    //% gatePin.fieldEditor=gridpicker
    //% gatePin.fieldOptions.withPinRepeated=0
    //% gatePin.defl=AnalogPin.P0
    //% sensorPin.fieldEditor=gridpicker
    //% sensorPin.fieldOptions.withPinRepeated=0
    //% sensorPin.defl=DigitalPin.P1
    //% limit.min=1 limit.max=99 defl=3
    //% weight=70
    export function setupSheepPen(gatePin: AnalogPin, sensorPin: DigitalPin, limit: number): void {
        sheepPenByPins(gatePin, sensorPin).configure(gatePin, sensorPin, limit)
    }

    /**
     * Update the sheep counter. Call this inside a forever loop.
     */
    //% blockId=code4fun_update_sheep_pen_pins block="count sheep gate pin %gatePin sensor %sensorPin"
    //% group="Sheep pen"
    //% gatePin.fieldEditor=gridpicker
    //% gatePin.fieldOptions.withPinRepeated=0
    //% gatePin.defl=AnalogPin.P0
    //% sensorPin.fieldEditor=gridpicker
    //% sensorPin.fieldOptions.withPinRepeated=0
    //% sensorPin.defl=DigitalPin.P1
    //% weight=69
    export function updateSheepPen(gatePin: AnalogPin, sensorPin: DigitalPin): number {
        return sheepPenByPins(gatePin, sensorPin).tick()
    }

    /**
     * Get the current sheep count.
     */
    //% blockId=code4fun_sheep_count_pins block="sheep count gate pin %gatePin sensor %sensorPin"
    //% group="Sheep pen"
    //% gatePin.fieldEditor=gridpicker
    //% gatePin.fieldOptions.withPinRepeated=0
    //% gatePin.defl=AnalogPin.P0
    //% sensorPin.fieldEditor=gridpicker
    //% sensorPin.fieldOptions.withPinRepeated=0
    //% sensorPin.defl=DigitalPin.P1
    //% weight=68
    export function sheepCount(gatePin: AnalogPin, sensorPin: DigitalPin): number {
        return sheepPenByPins(gatePin, sensorPin).getCount()
    }

    /**
     * Reset the sheep counter.
     */
    //% blockId=code4fun_reset_sheep_pen_pins block="reset sheep counter gate pin %gatePin sensor %sensorPin"
    //% group="Sheep pen"
    //% gatePin.fieldEditor=gridpicker
    //% gatePin.fieldOptions.withPinRepeated=0
    //% gatePin.defl=AnalogPin.P0
    //% sensorPin.fieldEditor=gridpicker
    //% sensorPin.fieldOptions.withPinRepeated=0
    //% sensorPin.defl=DigitalPin.P1
    //% weight=67
    export function resetSheepPen(gatePin: AnalogPin, sensorPin: DigitalPin): void {
        sheepPenByPins(gatePin, sensorPin).reset()
    }
}
