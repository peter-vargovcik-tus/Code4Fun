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
    private seated: boolean
    private state: GateState

    constructor(servoPin: AnalogPin) {
        this.servoPin = servoPin
        this.openAngle = 90
        this.closedAngle = 10
        this.moveDelayMs = 60
        this.stepDegrees = 10
        this.currentAngle = 90
        this.initialized = false
        this.seated = false
        this.state = GateState.Closed
    }

    matchesPin(pin: AnalogPin): boolean {
        return this.servoPin == pin
    }

    setOpenAngle(angle: number) {
        this.openAngle = this.clampAngle(angle)
    }

    setClosedAngle(angle: number) {
        this.closedAngle = this.clampAngle(angle)
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

    initialize() {
        let savedStep = this.stepDegrees
        let savedDelay = this.moveDelayMs

        this.stepDegrees = 5
        this.moveDelayMs = 100
        this.currentAngle = this.logicalCloseAngle()
        this.initialized = true
        this.state = GateState.Closed

        this.state = GateState.Opening
        this.moveTo(this.logicalOpenAngle())
        basic.pause(300)

        this.state = GateState.Closing
        this.moveTo(this.logicalCloseAngle())
        this.state = GateState.Closed
        this.seated = true

        this.stepDegrees = savedStep
        this.moveDelayMs = savedDelay
        this.stopServo()
    }

    open() {
        this.ensureSeated()
        this.state = GateState.Opening
        this.moveTo(this.logicalOpenAngle())
        this.state = GateState.Open
    }

    close() {
        this.ensureSeated()
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

    private ensureSeated() {
        if (!this.seated) {
            this.initialize()
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

let _gateList: GateController[] = []

function gateByPin(pin: AnalogPin): GateController {
    for (let i = 0; i < _gateList.length; i++) {
        if (_gateList[i].matchesPin(pin)) {
            return _gateList[i]
        }
    }

    let gate = new GateController(pin)
    _gateList.push(gate)
    return gate
}

/**
 * TUS Code4Fun extension blocks.
 * Each gate is one 3D-printed unit with its own servo on a chosen pin.
 * Servo mounting is fixed in hardware: logical open/close are mapped accordingly.
 */
//% color=#7B2CBF icon="\uf19d" weight=96 block="Code4Fun"
namespace code4fun {
    /**
     * Gently cycle a gate open and closed to seat the servo safely.
     */
    //% blockId=code4fun_gate_init_pin block="initialize gate on pin %pin"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% weight=101
    export function initializeGate(pin: AnalogPin): void {
        gateByPin(pin).initialize()
    }

    /**
     * Open a gate on the given pin.
     */
    //% blockId=code4fun_gate_open_pin block="gate open on pin %pin"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% weight=100
    export function gateOpen(pin: AnalogPin): void {
        gateByPin(pin).open()
    }

    /**
     * Close a gate on the given pin.
     */
    //% blockId=code4fun_gate_close_pin block="gate close on pin %pin"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% weight=99
    export function gateClose(pin: AnalogPin): void {
        gateByPin(pin).close()
    }

    /**
     * Check whether a gate on the given pin is open.
     */
    //% blockId=code4fun_gate_is_open_pin block="gate on pin %pin is open"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% weight=80
    export function gateIsOpen(pin: AnalogPin): boolean {
        return gateByPin(pin).isOpen()
    }

    /**
     * Check whether a gate on the given pin is closed.
     */
    //% blockId=code4fun_gate_is_closed_pin block="gate on pin %pin is closed"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% weight=79
    export function gateIsClosed(pin: AnalogPin): boolean {
        return gateByPin(pin).isClosed()
    }

    /**
     * Set the closed angle for a gate on the given pin.
     */
    //% blockId=code4fun_set_closed_angle_pin block="set gate on pin %pin closed angle to %angle"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% advanced=true
    //% weight=49
    export function setGateClosedAngle(pin: AnalogPin, angle: number): void {
        gateByPin(pin).setClosedAngle(angle)
    }

    /**
     * Set the open angle for a gate on the given pin.
     */
    //% blockId=code4fun_set_open_angle_pin block="set gate on pin %pin open angle to %angle"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% advanced=true
    //% weight=48
    export function setGateOpenAngle(pin: AnalogPin, angle: number): void {
        gateByPin(pin).setOpenAngle(angle)
    }

    /**
     * Set how many degrees a gate moves per step.
     */
    //% blockId=code4fun_set_step_degrees_pin block="set gate on pin %pin step size to %degrees degrees"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% advanced=true
    //% weight=47
    export function setGateStepSize(pin: AnalogPin, degrees: number): void {
        gateByPin(pin).setStepDegrees(degrees)
    }

    /**
     * Set the delay between gate movement steps.
     */
    //% blockId=code4fun_set_move_delay_pin block="set gate on pin %pin move delay to %delayMs ms"
    //% subcategory="Gate"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% advanced=true
    //% weight=46
    export function setGateMoveDelay(pin: AnalogPin, delayMs: number): void {
        gateByPin(pin).setMoveDelay(delayMs)
    }

    /**
     * Read distance from an ultrasonic sensor (HC-SR04 style). Always returns centimeters.
     */
    //% blockId=code4fun_ultrasonic_cm block="distance (cm) trig %trig echo %echo"
    //% subcategory="Ultrasonic"
    //% trig.fieldEditor=pinpicker
    //% trig.fieldOptions.columns=4
    //% trig.fieldOptions.tooltips=false
    //% trig.defl=DigitalPin.P15
    //% echo.fieldEditor=pinpicker
    //% echo.fieldOptions.columns=4
    //% echo.fieldOptions.tooltips=false
    //% echo.defl=DigitalPin.P14
    //% weight=90
    export function ultrasonicDistanceCm(trig: DigitalPin, echo: DigitalPin): number {
        pins.digitalWritePin(trig, 0)
        control.waitMicros(2)

        pins.digitalWritePin(trig, 1)
        control.waitMicros(10)
        pins.digitalWritePin(trig, 0)

        // Timeout 30ms ~= 5m max range
        const pulse = pins.pulseIn(echo, PulseValue.High, 30000)
        if (pulse <= 0) return 0

        // Convert microseconds to centimeters (approx.)
        return Math.idiv(pulse, 58)
    }

    /**
     * Check if an obstacle is closer than a given distance (cm) using an ultrasonic sensor.
     */
    //% blockId=code4fun_ultrasonic_obstacle_lt_cm block="obstacle closer than %cm cm trig %trig echo %echo"
    //% subcategory="Ultrasonic"
    //% trig.fieldEditor=pinpicker
    //% trig.fieldOptions.columns=4
    //% trig.fieldOptions.tooltips=false
    //% trig.defl=DigitalPin.P15
    //% echo.fieldEditor=pinpicker
    //% echo.fieldOptions.columns=4
    //% echo.fieldOptions.tooltips=false
    //% echo.defl=DigitalPin.P14
    //% cm.min=1 cm.max=300 cm.defl=20
    //% weight=89
    export function ultrasonicObstacleCloserThanCm(cm: number, trig: DigitalPin, echo: DigitalPin): boolean {
        const d = ultrasonicDistanceCm(trig, echo)
        return d > 0 && d < cm
    }

    /**
     * Read light level from a photoresistor module. Returns 0-1023.
     */
    //% blockId=code4fun_light_level block="light level on pin %pin"
    //% subcategory="Light"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% weight=88
    export function lightLevel(pin: AnalogPin): number {
        return pins.analogReadPin(pin)
    }

    /**
     * Check if it is dark on a photoresistor module.
     */
    //% blockId=code4fun_is_dark block="is dark on pin %pin"
    //% subcategory="Light"
    //% pin.fieldEditor=pinpicker
    //% pin.fieldOptions.columns=4
    //% pin.fieldOptions.tooltips=false
    //% pin.defl=AnalogPin.P0
    //% weight=87
    export function isDark(pin: AnalogPin): boolean {
        return pins.analogReadPin(pin) < 300
    }
}
