enum GateState {
    Closed = 0,
    Opening = 1,
    Open = 2,
    Closing = 3
}

const MAX_GATES = 4

class GateController {
    private servoPin: AnalogPin
    private openAngle: number
    private closedAngle: number
    private moveDelayMs: number
    private stepDegrees: number
    private currentAngle: number
    private initialized: boolean
    private state: GateState

    constructor(servoPin: AnalogPin) {
        this.servoPin = servoPin
        this.openAngle = 90
        this.closedAngle = 10
        this.moveDelayMs = 60
        this.stepDegrees = 10
        this.currentAngle = 10
        this.initialized = false
        this.state = GateState.Closed
    }

    setServoPin(pin: AnalogPin) {
        this.servoPin = pin
        this.initialized = false
    }

    setOpenAngle(angle: number) {
        this.openAngle = this.clampAngle(angle)
    }

    setClosedAngle(angle: number) {
        this.closedAngle = this.clampAngle(angle)
        if (!this.initialized) {
            this.currentAngle = this.logicalCloseAngle()
        }
    }

    setMoveDelay(delayMs: number) {
        if (delayMs < 1) {
            this.moveDelayMs = 1
        } else {
            this.moveDelayMs = delayMs
        }
    }

    setStepDegrees(degrees: number) {
        if (degrees < 1) {
            this.stepDegrees = 1
        } else {
            this.stepDegrees = degrees
        }
    }

    open() {
        this.ensureInitialized()
        this.state = GateState.Opening
        this.moveTo(this.logicalOpenAngle())
        this.state = GateState.Open
    }

    close() {
        this.ensureInitialized()
        this.state = GateState.Closing
        this.moveTo(this.logicalCloseAngle())
        this.state = GateState.Closed
    }

    isOpen(): boolean {
        return this.state == GateState.Open
    }

    isClosed(): boolean {
        return this.state == GateState.Closed
    }

    private logicalOpenAngle(): number {
        return this.closedAngle
    }

    private logicalCloseAngle(): number {
        return this.openAngle
    }

    private moveTo(targetAngle: number) {
        let target = this.clampAngle(targetAngle)

        while (this.currentAngle < target) {
            this.currentAngle += this.stepDegrees
            if (this.currentAngle > target) {
                this.currentAngle = target
            }
            pins.servoWritePin(this.servoPin, this.currentAngle)
            basic.pause(this.moveDelayMs)
        }

        while (this.currentAngle > target) {
            this.currentAngle -= this.stepDegrees
            if (this.currentAngle < target) {
                this.currentAngle = target
            }
            pins.servoWritePin(this.servoPin, this.currentAngle)
            basic.pause(this.moveDelayMs)
        }

        this.stopServo()
    }

    private stopServo() {
        pins.analogWritePin(this.servoPin, 0)
    }

    private ensureInitialized() {
        if (!this.initialized) {
            this.currentAngle = this.logicalCloseAngle()
            this.state = GateState.Closed
            this.initialized = true
            this.stopServo()
        }
    }

    private clampAngle(angle: number): number {
        if (angle < 0) {
            return 0
        }

        if (angle > 180) {
            return 180
        }

        return angle
    }
}

let _gates: GateController[] = []

function clampGateId(gateId: number): number {
    if (gateId < 1) {
        return 1
    }

    if (gateId > MAX_GATES) {
        return MAX_GATES
    }

    return gateId
}

function defaultServoPin(gateId: number): AnalogPin {
    if (gateId == 1) {
        return AnalogPin.P0
    }

    if (gateId == 2) {
        return AnalogPin.P2
    }

    if (gateId == 3) {
        return AnalogPin.P8
    }

    return AnalogPin.P12
}

function gateById(gateId: number): GateController {
    let id = clampGateId(gateId)
    let index = id - 1

    if (!_gates[index]) {
        _gates[index] = new GateController(defaultServoPin(id))
    }

    return _gates[index]
}

/**
 * TUS Code4Fun extension blocks.
 * Each gate is one 3D-printed unit with its own servo.
 * Servo mounting is fixed in hardware: logical open/close are mapped accordingly.
 */
//% color=#7B2CBF icon="\uf19d" weight=96 block="Code4Fun"
//% groups='["Gate", "Sheep pen", "Configuration"]'
namespace code4fun {
    /**
     * Open a gate.
     */
    //% blockId=code4fun_gate_open block="gate %gateId open"
    //% group="Gate"
    //% gateId.min=1 gateId.max=4 defl=1
    //% weight=100
    export function gateOpen(gateId: number = 1): void {
        gateById(gateId).open()
    }

    /**
     * Close a gate.
     */
    //% blockId=code4fun_gate_close block="gate %gateId close"
    //% group="Gate"
    //% gateId.min=1 gateId.max=4 defl=1
    //% weight=99
    export function gateClose(gateId: number = 1): void {
        gateById(gateId).close()
    }

    /**
     * Check whether a gate is open.
     */
    //% blockId=code4fun_gate_is_open block="gate %gateId is open"
    //% group="Gate"
    //% gateId.min=1 gateId.max=4 defl=1
    //% weight=80
    export function gateIsOpen(gateId: number = 1): boolean {
        return gateById(gateId).isOpen()
    }

    /**
     * Check whether a gate is closed.
     */
    //% blockId=code4fun_gate_is_closed block="gate %gateId is closed"
    //% group="Gate"
    //% gateId.min=1 gateId.max=4 defl=1
    //% weight=79
    export function gateIsClosed(gateId: number = 1): boolean {
        return gateById(gateId).isClosed()
    }

    /**
     * Set which pin a gate servo is connected to.
     */
    //% blockId=code4fun_set_servo_pin block="set gate %gateId servo pin to %pin"
    //% group="Configuration"
    //% gateId.min=1 gateId.max=4 defl=1
    //% advanced=true
    //% weight=50
    export function setGateServoPin(gateId: number, pin: AnalogPin): void {
        gateById(gateId).setServoPin(pin)
    }

    /**
     * Set the closed angle for a gate.
     */
    //% blockId=code4fun_set_closed_angle block="set gate %gateId closed angle to %angle"
    //% group="Configuration"
    //% gateId.min=1 gateId.max=4 defl=1
    //% advanced=true
    //% weight=49
    export function setGateClosedAngle(gateId: number, angle: number): void {
        gateById(gateId).setClosedAngle(angle)
    }

    /**
     * Set the open angle for a gate.
     */
    //% blockId=code4fun_set_open_angle block="set gate %gateId open angle to %angle"
    //% group="Configuration"
    //% gateId.min=1 gateId.max=4 defl=1
    //% advanced=true
    //% weight=48
    export function setGateOpenAngle(gateId: number, angle: number): void {
        gateById(gateId).setOpenAngle(angle)
    }

    /**
     * Set how many degrees a gate moves per step.
     */
    //% blockId=code4fun_set_step_degrees block="set gate %gateId step size to %degrees degrees"
    //% group="Configuration"
    //% gateId.min=1 gateId.max=4 defl=1
    //% advanced=true
    //% weight=47
    export function setGateStepSize(gateId: number, degrees: number): void {
        gateById(gateId).setStepDegrees(degrees)
    }

    /**
     * Set the delay between gate movement steps.
     */
    //% blockId=code4fun_set_move_delay block="set gate %gateId move delay to %delayMs ms"
    //% group="Configuration"
    //% gateId.min=1 gateId.max=4 defl=1
    //% advanced=true
    //% weight=46
    export function setGateMoveDelay(gateId: number, delayMs: number): void {
        gateById(gateId).setMoveDelay(delayMs)
    }
}
