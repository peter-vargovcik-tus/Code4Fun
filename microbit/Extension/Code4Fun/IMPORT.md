# Import Code4Fun extension into MakeCode

The error **"This .hex file doesn't contain source"** happens when importing a `.hex` built by the **mkc CLI**. Those files flash to the micro:bit but cannot be re-imported into MakeCode ([known limitation](https://github.com/Microsoft/pxt-microbit/issues/6676)).

Use one of the methods below instead.

---

## Method A — Extension URL (easiest right now)

1. Open [MakeCode micro:bit](https://makecode.microbit.org/) and create a project.
2. Click **Extensions**.
3. Paste this URL into the search box:

   **https://makecode.microbit.org/_J80c5kDvEWHo**

4. Press Enter and add the package when it appears.

The **Code4Fun** category should appear in the toolbox with **Gate** and **Configuration** groups.

> After you publish to GitHub, replace this URL with your GitHub repo URL (Method B).

---

## Method B — GitHub URL (recommended)

1. Push this repository to GitHub (root must contain `pxt.json` and `gate.ts`).
2. In MakeCode: **Extensions** → paste:

   **https://github.com/peter-vargovcik-tus/Code4Fun**

3. Add **tus-code4fun**.

After `deploy-extension.ps1`, `gate.ts` and `pxt.json` are copied to the repo root automatically.

Students can paste the GitHub URL or try searching **code4fun** / **tus** in the Extensions dialog (results depend on GitHub indexing).

---

## Method C — Import file (.hex) for offline classrooms

The import file **must be saved from the MakeCode website**, not from the CLI.

### Teacher setup (once, while online)

1. Add the extension using **Method A** or **Method B** above.
2. Create a **new empty project** (or use a project that only needs the extension).
3. Add the Code4Fun extension again via **Extensions**.
4. Click the **Save** icon (disk) at the bottom, or **Download**.
5. Save the file as e.g. `code4fun-extension.hex`.
6. Give **that** file to students.

### Student steps (can work offline)

1. Open MakeCode → open or create a project.
2. **Extensions** → **Import file**.
3. Select the teacher's `code4fun-extension.hex`.
4. **Code4Fun** appears in the toolbox.

**Do not use** `dist/code4fun-extension.hex` from this repo for MakeCode import — it is CLI-built and lacks embedded source. It is only useful if re-generated via the teacher workflow above.

---

## Method D — Open the shared demo project

To see the blocks and test quickly:

1. MakeCode **Home** → **Import** → **Import URL**
2. Paste: **https://makecode.microbit.org/_J80c5kDvEWHo**

This opens a project with the Code4Fun blocks available.

---

## Refresh after an extension update

If you still see old blocks like `gate open` **without a pin picker**:

1. Open your project in MakeCode.
2. Go to **Extensions** (gear icon).
3. **Remove** the old **tus-code4fun** / **Code4Fun** package.
4. Add it again: `https://github.com/peter-vargovcik-tus/Code4Fun`
5. Start a **new project** if old blocks still appear on the workspace.

You should see version **0.4.1** blocks with pin pickers, for example:

- `initialize gate on pin P0`
- `gate open on pin P0`
- `set up sheep counter gate pin P0 sensor P1 for 3 sheep`

---

## Verify it worked

You should see:

- A **Code4Fun** category in the toolbox (like **Servos**)
- **Gate** group: `initialize gate on pin ...`, `gate open on pin ...`, etc.
- **Sheep pen** group: sheep counter blocks with gate and sensor pins
- **More...** → **Configuration** group: optional settings

If blocks only appear in Explorer as `gate.ts` with no toolbox category, the extension was not added via **Extensions** — fix that first.

---

## Rebuild after code changes

```powershell
cd microbit
.\deploy-extension.ps1
```

Then update the MakeCode share URL (run from `import-bundle`):

```powershell
cd microbit\Extension\Code4Fun\import-bundle
npx makecode share
```

Paste the new URL into this file and give it to students.
