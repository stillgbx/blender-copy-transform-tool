"""
Copy Transform Tool — UI Panel

Locations:
  - View3D > Sidebar (N) > Copy Transform  (CTT_PT_main)
  - Outliner right-click on object          (_draw_outliner_menu appended to OUTLINER_MT_object)
"""

import math

import bpy
from bpy.types import Panel


class CTT_PT_main(Panel):
    bl_label = "Copy Transform"
    bl_idname = "CTT_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Copy Transform"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        wm = context.window_manager

        # ── Channel toggles ──────────────────────────────────────────────────
        row = layout.row(align=True)
        row.prop(wm, "ctt_do_location", toggle=True, icon='CON_LOCLIKE')
        row.prop(wm, "ctt_do_rotation", toggle=True, icon='CON_ROTLIKE')
        row.prop(wm, "ctt_do_scale", toggle=True, icon='CON_SIZELIKE')

        layout.separator()

        # ── Copy button ───────────────────────────────────────────────────────
        row = layout.row()
        row.scale_y = 1.4
        row.operator("ctt.copy_transform", icon='COPYDOWN')

        # ── Clipboard preview ────────────────────────────────────────────────
        if wm.ctt_has_data:
            box = layout.box()
            col = box.column(align=True)
            col.scale_y = 0.75

            loc = wm.ctt_clip_location
            rot = wm.ctt_clip_rotation
            scl = wm.ctt_clip_scale

            col.label(
                text=f"Loc  {loc[0]:.3f}  {loc[1]:.3f}  {loc[2]:.3f}",
                icon='CON_LOCLIKE',
            )
            col.label(
                text=(
                    f"Rot  {math.degrees(rot[0]):.1f}\u00b0"
                    f"  {math.degrees(rot[1]):.1f}\u00b0"
                    f"  {math.degrees(rot[2]):.1f}\u00b0"
                ),
                icon='CON_ROTLIKE',
            )
            col.label(
                text=f"Scl  {scl[0]:.3f}  {scl[1]:.3f}  {scl[2]:.3f}",
                icon='CON_SIZELIKE',
            )

        layout.separator()

        # ── Paste button ──────────────────────────────────────────────────────
        row = layout.row()
        row.scale_y = 1.4
        row.enabled = wm.ctt_has_data
        row.operator("ctt.paste_transform", icon='PASTEDOWN')


classes = (CTT_PT_main,)


# ── Outliner context menu ────────────────────────────────────────────────────

def _draw_outliner_menu(self, context: bpy.types.Context) -> None:
    """Appended to OUTLINER_MT_object: adds Copy/Paste entries in the right-click menu."""
    wm = context.window_manager
    layout = self.layout
    layout.separator()
    layout.operator("ctt.copy_transform", icon='COPYDOWN')
    row = layout.row()
    row.enabled = wm.ctt_has_data
    row.operator("ctt.paste_transform", icon='PASTEDOWN')


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.OUTLINER_MT_object.append(_draw_outliner_menu)


def unregister():
    bpy.types.OUTLINER_MT_object.remove(_draw_outliner_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
