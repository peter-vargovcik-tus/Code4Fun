class SheepPenController {
    private gateId: number
    private sensorPin: DigitalPin
    private limit: number
    private count: number
    private gateOpened: boolean
    private finished: boolean
    private wasBlocked: boolean
    private configured: boolean

    constructor() {
        this.gateId = 1
        this.sensorPin = DigitalPin.P1
        this.limit = 3
        this.count = 0
        this.gateOpened = false
        this.finished = false
        this.wasBlocked = false
        this.configured = false
    }

    configure(gateId: number, sensorPin: DigitalPin, limit: number) {
        this.gateId = gateId
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
                code4fun.gateOpen(this.gateId)
                this.gateOpened = true
            }

            if (this.count >= this.limit) {
                code4fun.gateClose(this.gateId)
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
        code4fun.gateClose(this.gateId)
    }
}

let _sheepPens: SheepPenController[] = []

function sheepPenById(gateId: number): SheepPenController {
    let id = gateId
    if (id < 1) {
        id = 1
    }

    if (id > MAX_GATES) {
        id = MAX_GATES
    }

    let index = id - 1

    if (!_sheepPens[index]) {
        _sheepPens[index] = new SheepPenController()
    }

    return _sheepPens[index]
}

namespace code4fun {
    /**
     * Set up a sheep counter for a gate and sensor.
     */
    //% blockId=code4fun_setup_sheep_pen block="set up gate %gateId sheep counter sensor %sensorPin for %limit sheep"
    //% group="Sheep pen"
    //% gateId.min=1 gateId.max=4 defl=1
    //% limit.min=1 limit.max=99 defl=3
    //% weight=70
    export function setupSheepPen(gateId: number, sensorPin: DigitalPin, limit: number): void {
        sheepPenById(gateId).configure(gateId, sensorPin, limit)
    }

    /**
     * Update the sheep counter for a gate. Call this inside a forever loop.
     */
    //% blockId=code4fun_update_sheep_pen block="count sheep at gate %gateId"
    //% group="Sheep pen"
    //% gateId.min=1 gateId.max=4 defl=1
    //% weight=69
    export function updateSheepPen(gateId: number): number {
        return sheepPenById(gateId).tick()
    }

    /**
     * Get the current sheep count for a gate.
     */
    //% blockId=code4fun_sheep_count block="sheep count at gate %gateId"
    //% group="Sheep pen"
    //% gateId.min=1 gateId.max=4 defl=1
    //% weight=68
    export function sheepCount(gateId: number): number {
        return sheepPenById(gateId).getCount()
    }

    /**
     * Reset the sheep counter for a gate.
     */
    //% blockId=code4fun_reset_sheep_pen block="reset sheep counter at gate %gateId"
    //% group="Sheep pen"
    //% gateId.min=1 gateId.max=4 defl=1
    //% weight=67
    export function resetSheepPen(gateId: number): void {
        sheepPenById(gateId).reset()
    }
}
