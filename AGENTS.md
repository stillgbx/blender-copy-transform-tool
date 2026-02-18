# AGENTS.md — Copy Transform Tool Blender Addon

Instructions for AI agents (LLMs) working on this project.

---

## Project Context

Blender addon (Python) that copies and pastes local transforms (location, rotation, scale)
between objects. No external dependencies.

- **Minimum Blender**: 5.0+
- **Code language**: English (docstrings, variables, comments)
- **Documentation language**: English (README.md, AGENTS.md, inline comments)
- **Communication language with the user**: French

---

## File Architecture

```
blender-copy-transform-tool/
├── __init__.py      # bl_info, register/unregister (import order matters)
├── properties.py    # WindowManager properties: clipboard + channel toggles
├── operators.py     # CTT_OT_copy_transform, CTT_OT_paste_transform
├── panels.py        # CTT_PT_main (View3D > Sidebar > Copy Transform)
├── README.md        # User documentation
└── AGENTS.md        # This file
```

---

## Code Conventions

### Python / Blender API

- Use **type annotations** in signatures.
- Prefix internal helpers with `_`.
- Blender classes follow `CTT_OT_xxx`, `CTT_PT_xxx` naming.
- `bl_idname` uses the `ctt.` prefix (e.g. `ctt.copy_transform`).

### Clipboard Storage

Properties are stored on `bpy.types.WindowManager`:
- Session-persistent (survives undo), not saved with the `.blend` file.
- `ctt_has_data` (bool): True once at least one copy has been performed.
- `ctt_clip_location` (FloatVector 3): copied location.
- `ctt_clip_rotation` (FloatVector 3): copied rotation stored as **XYZ Euler (radians)**.
- `ctt_clip_scale` (FloatVector 3): copied scale.
- `ctt_do_location/rotation/scale` (bool): which channels to apply on paste.

### Rotation Handling

The clipboard always stores rotation as XYZ Euler (radians) regardless of the source
object's `rotation_mode`. On paste, the value is converted to the target's rotation mode
to avoid overwriting the wrong slot.

---

## Modification Rules

### Before Modifying Code

1. **Read the file** in its entirety before editing it.
2. Keep all `bpy.types.WindowManager` property additions/deletions in sync between
   `properties.register()` and `properties.unregister()`.

### After Each Modification

1. **Reload the addon** in Blender (Edit > Preferences > Add-ons) to verify no errors.
2. **Update README.md** if a new feature or operator is added.
3. **Update this file** if the file architecture or conventions change.

### What NOT to Do

- **Never** use external dependencies (pip) — no imports beyond Blender's stdlib + mathutils.
- **Never** store clipboard data on `Scene` (avoids polluting saved files).
- **Never** use `bpy.ops` inside `execute()` for pure data operations — set properties directly.
- **Never** break Blender 5.0+ compatibility without discussion.
