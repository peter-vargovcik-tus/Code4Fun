# Repository Context

## Current state

This repository started as a CAD-first project for a miniature automated gate used in a `Code4Fun` camp activity. The original goal was a farm or crossing-style gate for a small autonomous pen where `Hexbug` or bristlebot toys represent animals.

The current codebase is still mostly mechanical-design code:

- `params.py` contains shared gate dimensions.
- `cadquery/generate_gate.py` generates CAD parts as STEP files.
- `cadquery/animate_gate.py` and `cadquery/animate_gate_physics.py` simulate gate motion.
- `fusion/build_gate.py` is a separate Fusion 360 script path.

There is currently no embedded or control software in the repository.

## Important project shift

The existing CAD design is no longer considered accurate enough to be the main source for the physical build. A manual redesign will be done outside this code path.

Because of that, the main value of this repository going forward is expected to shift from:

- CAD generation

to:

- control logic
- sensor and actuator behavior
- student-friendly software structure
- micro:bit MakeCode experimentation

## What is still useful from the existing code

Even though the CAD is no longer the main deliverable, the current Python files still provide useful context:

- They describe the intended gate behavior: closed, opening, open.
- They encode useful mechanical assumptions such as servo-driven upward motion.
- They help define the vocabulary we should keep consistent in software:
  - `gate`
  - `open`
  - `close`
  - `servo`
  - `sensor`
  - `blocked`
  - `idle`

## Software direction

The likely software target is:

- hardware: Keyestudio Sensor Shield V2 for BBC micro:bit
- editor/runtime: Microsoft MakeCode for micro:bit

That suggests future code will probably be organized around:

1. input sensing
2. gate state management
3. actuator output
4. timing and safety rules
5. simple student-facing blocks or helper APIs

## Recommended next software folders

When software work starts, add dedicated folders instead of mixing it into the CAD scripts:

- `microbit/Gate/` for MakeCode development and demos
- `microbit/Extension/` for student-facing extension packages
- `hexbug-farm-gate/docs/` for hardware mapping and behavior specs

## Suggested first software artifacts

The first software design items should probably be:

1. a hardware map for pins, sensors, and servo wiring
2. a gate state model
3. a simple behavior spec for open and close decisions
4. a first MakeCode proof of concept

## Notes on legacy files

- `cadquery/output/` and `rev2/output/` are generated artifacts.
- `rev2/` looks experimental and should not be treated as the software baseline.
- `docs/import-and-assembly.md` contains assembly guidance for the old CAD path and may not match future hardware exactly.
