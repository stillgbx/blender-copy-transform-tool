"""
Copy Transform Tool — Operators

CTT_OT_copy_transform  : copies local transform from the active object into the clipboard.
CTT_OT_paste_transform : applies clipboard transform to all selected objects.

Rotation is stored internally as XYZ Euler (radians).
All three rotation modes are handled: EULER, QUATERNION, AXIS_ANGLE.
"""

import bpy
from bpy.types import Operator
from mathutils import Euler, Quaternion


class CTT_OT_copy_transform(Operator):
    bl_idname = "ctt.copy_transform"
    bl_label = "Copy Transform"
    bl_description = "Copy local location/rotation/scale from the active object to clipboard"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        obj = context.active_object
        wm = context.window_manager

        wm.ctt_clip_location = obj.location

        # Normalise rotation to XYZ Euler regardless of the object's rotation mode
        if obj.rotation_mode == 'QUATERNION':
            wm.ctt_clip_rotation = obj.rotation_quaternion.to_euler('XYZ')
        elif obj.rotation_mode == 'AXIS_ANGLE':
            angle = obj.rotation_axis_angle[0]
            axis = obj.rotation_axis_angle[1:]
            wm.ctt_clip_rotation = Quaternion(axis, angle).to_euler('XYZ')
        else:
            # Any Euler order: store as-is (XYZ approximation)
            wm.ctt_clip_rotation = obj.rotation_euler.to_quaternion().to_euler('XYZ')

        wm.ctt_clip_scale = obj.scale
        wm.ctt_has_data = True

        self.report({'INFO'}, f"Copied transform from '{obj.name}'")
        return {'FINISHED'}


class CTT_OT_paste_transform(Operator):
    bl_idname = "ctt.paste_transform"
    bl_label = "Paste Transform"
    bl_description = "Paste clipboard transform to all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        wm = context.window_manager
        return wm.ctt_has_data and len(context.selected_objects) > 0

    def execute(self, context: bpy.types.Context):
        wm = context.window_manager
        count = 0

        clip_euler = Euler(wm.ctt_clip_rotation, 'XYZ')

        for obj in context.selected_objects:
            if wm.ctt_do_location:
                obj.location = wm.ctt_clip_location

            if wm.ctt_do_rotation:
                if obj.rotation_mode == 'QUATERNION':
                    obj.rotation_quaternion = clip_euler.to_quaternion()
                elif obj.rotation_mode == 'AXIS_ANGLE':
                    quat = clip_euler.to_quaternion()
                    obj.rotation_axis_angle = [quat.angle, *quat.axis]
                else:
                    # Convert to the target's Euler order to minimise gimbal issues
                    obj.rotation_euler = clip_euler.to_quaternion().to_euler(obj.rotation_mode)

            if wm.ctt_do_scale:
                obj.scale = wm.ctt_clip_scale

            count += 1

        self.report({'INFO'}, f"Pasted transform to {count} object(s)")
        return {'FINISHED'}


classes = (
    CTT_OT_copy_transform,
    CTT_OT_paste_transform,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
