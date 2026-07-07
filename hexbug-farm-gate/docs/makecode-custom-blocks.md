# MakeCode Custom Blocks

## Short answer

Yes, we can create custom blocks for this project in MakeCode for micro:bit.

There are two practical paths:

1. add local custom blocks inside a MakeCode project using `custom.ts`
2. create a reusable MakeCode extension backed by a GitHub repository

## Why this matters

Custom blocks would let students use friendly, task-focused blocks such as:

- `open gate`
- `close gate`
- `stop gate`
- `is gate blocked`
- `set gate speed`
- `when sensor triggered`

This can hide low-level details like pin control, servo angles, and timing.

## Best path for this project

Use a staged approach:

1. start with a normal MakeCode project
2. define a few custom blocks in `custom.ts`
3. test the block names and teaching flow with students
4. move the blocks into a reusable extension if they work well

That keeps the early work simple while still leaving room to grow into a cleaner package later.

## What a reusable extension would contain

A MakeCode extension usually includes:

- `pxt.json`
- one or more TypeScript files
- exported functions inside a namespace
- block metadata using `//%` annotations

The block annotations define how functions appear in the block toolbox.

## Example shape

This is the kind of API we could build later:

```ts
/**
 * Gate control blocks.
 */
//% color=#0fbc11 icon="\uf085" weight=80
namespace gate {
    /**
     * Open the gate.
     */
    //% blockId=gate_open block="open gate"
    export function open(): void {
        // servo logic here
    }

    /**
     * Close the gate.
     */
    //% blockId=gate_close block="close gate"
    export function close(): void {
        // servo logic here
    }
}
```

## Likely block groups for this project

We should probably separate blocks into a small number of beginner-friendly categories:

- setup
- gate actions
- sensor checks
- events
- status

Possible examples:

- `initialize gate on pin P0`
- `open gate`
- `close gate`
- `move gate to %angle`
- `set open angle to %angle`
- `set close angle to %angle`
- `if gate is blocked`
- `when animal detected`

## Good design rule

The blocks should describe behavior in plain language, not hardware details first.

For example, students will understand:

- `open gate`

more easily than:

- `write servo 90 to pin P0`

We can still keep advanced blocks for teachers or debugging.

## Limits and considerations

- The extension can provide custom blocks, but it still runs within normal micro:bit limits.
- Servo control, timing, and sensor polling must be simple and robust.
- If the shield uses standard servo and sensor pins, MakeCode should handle this well.
- If we need special hardware support, we may need a slightly richer extension API.

## Recommended next step

Before implementing blocks, define:

1. which sensors will be connected
2. which pin drives the servo
3. what the gate states are
4. what student-facing behaviors should exist

After that, we can draft a first MakeCode block set and a matching TypeScript API.

## References

- [Microsoft MakeCode for micro:bit](https://makecode.microbit.org/)
- [Building your own extension](https://makecode.microbit.org/extensions/build-your-own)
- [Defining blocks](https://makecode.com/defining-blocks)
- [Custom blocks](https://makecode.microbit.org/v0/blocks/custom)
