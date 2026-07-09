class LaserSensorController {
    private transmitterPin: DigitalPin
    private receiverPin: AnalogPin
    private threshold: number
    private clearAboveThreshold: boolean
    private transmitterOn: boolean
    private initialized: boolean

    constructor() {
        this.transmitterPin = DigitalPin.P2
        this.receiverPin = AnalogPin.P1
        this.threshold = 500
        this.clearAboveThreshold = true
        this.transmitterOn = false
        this.initialized = false
    }

    setTransmitterPin(pin: DigitalPin) {
        this.transmitterPin = pin
        this.transmitterOn = false
        this.initialized = false
    }

    setReceiverPin(pin: AnalogPin) {
        this.receiverPin = pin
        this.initialized = false
    }

    setThreshold(value: number) {
        if (value < 0) {
            this.threshold = 0
        } else if (value > 1023) {
            this.threshold = 1023
        } else {
            this.threshold = value
        }
    }

    setClearAboveThreshold(clearAbove: boolean) {
        this.clearAboveThreshold = clearAbove
    }

    turnOn() {
        pins.digitalWritePin(this.transmitterPin, 1)
        this.transmitterOn = true
        this.initialized = true
    }

    turnOff() {
        pins.digitalWritePin(this.transmitterPin, 0)
        this.transmitterOn = false
    }

    readLevel(): number {
        this.ensureReady()
        return pins.analogReadPin(this.receiverPin)
    }

    isBeamBlocked(): boolean {
        return !this.isBeamClear()
    }

    isBeamClear(): boolean {
        let level = this.readLevel()
        if (this.clearAboveThreshold) {
            return level >= this.threshold
        }
        return level < this.threshold
    }

    private ensureReady() {
        if (!this.initialized) {
            this.turnOn()
        }
    }
}

let _laser = new LaserSensorController()

namespace code4fun {
    /**
     * Turn the laser transmitter on.
     */
    //% blockId=code4fun_laser_on block="laser on"
    //% group="Laser"
    //% weight=95
    export function laserOn(): void {
        _laser.turnOn()
    }

    /**
     * Turn the laser transmitter off.
     */
    //% blockId=code4fun_laser_off block="laser off"
    //% group="Laser"
    //% weight=94
    export function laserOff(): void {
        _laser.turnOff()
    }

    /**
     * Check whether the laser beam is blocked.
     */
    //% blockId=code4fun_laser_beam_blocked block="laser beam blocked"
    //% group="Laser"
    //% weight=90
    export function laserBeamBlocked(): boolean {
        return _laser.isBeamBlocked()
    }

    /**
     * Check whether the laser beam is clear.
     */
    //% blockId=code4fun_laser_beam_clear block="laser beam clear"
    //% group="Laser"
    //% weight=89
    export function laserBeamClear(): boolean {
        return _laser.isBeamClear()
    }

    /**
     * Read the raw analog sensor level (0-1023).
     */
    //% blockId=code4fun_laser_sensor_value block="laser sensor value"
    //% group="Laser"
    //% weight=87
    //% advanced=true
    export function laserSensorValue(): number {
        return _laser.readLevel()
    }

    /**
     * Run code when the laser beam becomes blocked.
     */
    //% blockId=code4fun_on_laser_beam_blocked block="when laser beam blocked"
    //% group="Laser"
    //% weight=88
    //% blockGap=8
    export function onLaserBeamBlocked(handler: () => void): void {
        control.inBackground(function () {
            let wasBlocked = false
            while (true) {
                let blocked = _laser.isBeamBlocked()
                if (blocked && !wasBlocked) {
                    handler()
                }
                wasBlocked = blocked
                basic.pause(50)
            }
        })
    }

    /**
     * Set which pin the laser transmitter is connected to.
     */
    //% blockId=code4fun_set_laser_transmitter_pin block="set laser transmitter pin to %pin"
    //% group="Configuration"
    //% advanced=true
    //% weight=45
    export function setLaserTransmitterPin(pin: DigitalPin): void {
        _laser.setTransmitterPin(pin)
    }

    /**
     * Set which pin the laser receiver is connected to.
     */
    //% blockId=code4fun_set_laser_receiver_pin block="set laser receiver pin to %pin"
    //% group="Configuration"
    //% advanced=true
    //% weight=44
    export function setLaserReceiverPin(pin: AnalogPin): void {
        _laser.setReceiverPin(pin)
    }

    /**
     * Set the analog threshold for beam clear vs blocked (0-1023).
     */
    //% blockId=code4fun_set_laser_threshold block="set laser threshold to %threshold"
    //% group="Configuration"
    //% advanced=true
    //% threshold.min=0 threshold.max=1023
    //% weight=43
    export function setLaserThreshold(threshold: number): void {
        _laser.setThreshold(threshold)
    }

    /**
     * Set whether the beam is clear when the reading is above the threshold.
     */
    //% blockId=code4fun_set_laser_clear_above block="set laser clear when reading is above threshold %clearAbove"
    //% group="Configuration"
    //% advanced=true
    //% clearAbove.defl=true
    //% weight=42
    export function setLaserClearAboveThreshold(clearAbove: boolean): void {
        _laser.setClearAboveThreshold(clearAbove)
    }
}
