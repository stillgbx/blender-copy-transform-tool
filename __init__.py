"""
Copy Transform Tool - Blender Addon
Copy and paste location, rotation and scale between objects.
"""

bl_info = {
    "name": "Copy Transform Tool",
    "author": "stillgbx",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Copy Transform",
    "description": "Copy and paste location, rotation and scale between objects",
    "category": "Object",
}

from . import properties
from . import operators
from . import panels


def register():
    properties.register()
    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    operators.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()
