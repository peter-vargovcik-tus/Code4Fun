# Gate Controller Context

## Purpose

This document defines the first software slice for the `TUS Code4Fun` gate project.

The immediate goal is intentionally small:

- create a first `GateController`
- support manual `open` and `close`
- keep the API simple enough for future MakeCode blocks

## Hardware assumptions for v1

The first version assumes:

- BBC micro:bit as the controller
- Keyestudio Sensor Shield V2 or equivalent breakout
- one servo driving the gate
- laser beam sensor added later for automation

This first step does not implement sensing yet. It only establishes reliable gate movement.

## Software scope for v1

The controller should provide:

1. gate setup
2. open command
3. close command
4. simple gate state tracking
5. configurable open and closed angles

This should become the base for later features such as:

- auto open on beam break
- delayed close
- blocked-path safety logic
- student-friendly custom blocks

## Initial state model

The first state model is:

- `closed`
- `opening`
- `open`
- `closing`

This is enough for the first manual-control milestone.

## Design choices

- Use a single servo output pin.
- Move the servo in coarse steps for lower power use.
- Stop the servo pulse after each move with `pins.analogWritePin(pin, 0)`.
- Keep pin setup and angle calibration explicit.
- Use plain-language block names that can later appear in MakeCode.

## First extension surface

The first student-facing actions should be:

- `initialize gate on pin ...`
- `open gate`
- `close gate`
- `gate state`

Calibration helpers can exist but should stay secondary:

- `set gate open angle`
- `set gate closed angle`
- `set gate move delay`

## Out of scope for this step

These items should come after the first open and close milestone works:

- laser beam sensing
- automatic mode
- obstacle or blocked-path handling
- classroom examples
- full reusable extension packaging and publishing flow
