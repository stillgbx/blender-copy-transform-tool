"""
Copy Transform Tool — Properties

Clipboard data is stored on WindowManager: session-persistent, not saved with the .blend file.
Settings (which channels to copy/paste) are stored on WindowManager too.
"""

import bpy
from bpy.props import BoolProperty, FloatVectorProperty
from bpy.types import WindowManager


def register():
    # Clipboard content (always stores all three channels)
    WindowManager.ctt_has_data = BoolProperty(default=False)
    WindowManager.ctt_clip_location = FloatVectorProperty(size=3, default=(0.0, 0.0, 0.0))
    WindowManager.ctt_clip_rotation = FloatVectorProperty(size=3, default=(0.0, 0.0, 0.0))
    WindowManager.ctt_clip_scale = FloatVectorProperty(size=3, default=(1.0, 1.0, 1.0))

    # Channel toggles — which channels will be copied/pasted
    WindowManager.ctt_do_location = BoolProperty(name="Location", default=True)
    WindowManager.ctt_do_rotation = BoolProperty(name="Rotation", default=True)
    WindowManager.ctt_do_scale = BoolProperty(name="Scale", default=False)


def unregister():
    del WindowManager.ctt_has_data
    del WindowManager.ctt_clip_location
    del WindowManager.ctt_clip_rotation
    del WindowManager.ctt_clip_scale
    del WindowManager.ctt_do_location
    del WindowManager.ctt_do_rotation
    del WindowManager.ctt_do_scale
