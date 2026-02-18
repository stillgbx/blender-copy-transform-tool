# Copy Transform Tool

Blender addon to copy and paste local transforms (location, rotation, scale) between objects.

> 100% vibe coded with Claude Code

## Installation

1. In Blender: **Edit > Preferences > Add-ons > Install…**
2. Select the `blender-copy-transform-tool` folder (or a `.zip` of it).
3. Enable **Object: Copy Transform Tool**.

## Usage

Open the **N-panel** in the 3D Viewport (press `N`), go to the **Copy Transform** tab.

### Steps

1. **Select which channels** to copy/paste using the toggle buttons:
   `Location` | `Rotation` | `Scale`

2. **Select the source object** (active object) and click **Copy Transform**.
   The clipboard preview appears below the button showing the stored values.

3. **Select the target object(s)** and click **Paste Transform**.
   The checked channels are applied to all selected objects.

### Notes

- The clipboard persists for the whole session (survives undo) but is **not saved** with the `.blend` file.
- All rotation modes are supported (XYZ Euler, Quaternion, Axis Angle). Rotation is
  converted automatically between modes.
- Transforms are **local** (relative to the parent, as shown in the Properties panel).
- Pasting to multiple selected objects applies the same transform to all of them.

## Requirements

- Blender 5.0+
- No external dependencies.
