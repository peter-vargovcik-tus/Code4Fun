enum GateState {
    Closed = 0,
    Opening = 1,
    Open = 2,
    Closing = 3
}

class GateController {
    private servoPin: AnalogPin
    private openAngle: number
    private closedAngle: number
    private moveDelayMs: number
    private stepDegrees: number
    private currentAngle: number
    private initialized: boolean
    private state: GateState

    constructor() {
        this.servoPin = AnalogPin.P0
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
            this.currentAngle = this.closedAngle
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
        this.moveTo(this.openAngle)
        this.state = GateState.Open
    }

    close() {
        this.ensureInitialized()
        this.state = GateState.Closing
        this.moveTo(this.closedAngle)
        this.state = GateState.Closed
    }

    isOpen(): boolean {
        return this.state == GateState.Open
    }

    isClosed(): boolean {
        return this.state == GateState.Closed
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
            this.currentAngle = this.closedAngle
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

let _gate = new GateController()

/**
 * TUS Code4Fun extension blocks.
 * Defaults: servo P0, closed 10°, open 90°, step 10°, delay 60 ms.
 */
//% color=#7B2CBF icon="\uf19d" weight=96 block="Code4Fun"
//% groups='["Gate", "Laser", "Configuration"]'
namespace code4fun {
    /**
     * Open the gate.
     */
    //% blockId=code4fun_gate_open block="gate open"
    //% group="Gate"
    //% weight=100
    export function gateOpen(): void {
        _gate.open()
    }

    /**
     * Close the gate.
     */
    //% blockId=code4fun_gate_close block="gate close"
    //% group="Gate"
    //% weight=99
    export function gateClose(): void {
        _gate.close()
    }

    /**
     * Check whether the gate is open.
     */
    //% blockId=code4fun_gate_is_open block="gate is open"
    //% group="Gate"
    //% weight=80
    export function gateIsOpen(): boolean {
        return _gate.isOpen()
    }

    /**
     * Check whether the gate is closed.
     */
    //% blockId=code4fun_gate_is_closed block="gate is closed"
    //% group="Gate"
    //% weight=79
    export function gateIsClosed(): boolean {
        return _gate.isClosed()
    }

    /**
     * Set which pin the gate servo is connected to.
     */
    //% blockId=code4fun_set_servo_pin block="set gate servo pin to %pin"
    //% group="Configuration"
    //% advanced=true
    //% weight=50
    export function setGateServoPin(pin: AnalogPin): void {
        _gate.setServoPin(pin)
    }

    /**
     * Set the closed angle for the gate.
     */
    //% blockId=code4fun_set_closed_angle block="set gate closed angle to %angle"
    //% group="Configuration"
    //% advanced=true
    //% weight=49
    export function setGateClosedAngle(angle: number): void {
        _gate.setClosedAngle(angle)
    }

    /**
     * Set the open angle for the gate.
     */
    //% blockId=code4fun_set_open_angle block="set gate open angle to %angle"
    //% group="Configuration"
    //% advanced=true
    //% weight=48
    export function setGateOpenAngle(angle: number): void {
        _gate.setOpenAngle(angle)
    }

    /**
     * Set how many degrees the gate moves per step.
     */
    //% blockId=code4fun_set_step_degrees block="set gate step size to %degrees degrees"
    //% group="Configuration"
    //% advanced=true
    //% weight=47
    export function setGateStepSize(degrees: number): void {
        _gate.setStepDegrees(degrees)
    }

    /**
     * Set the delay between gate movement steps.
     */
    //% blockId=code4fun_set_move_delay block="set gate move delay to %delayMs ms"
    //% group="Configuration"
    //% advanced=true
    //% weight=46
    export function setGateMoveDelay(delayMs: number): void {
        _gate.setMoveDelay(delayMs)
    }
}
