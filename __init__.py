bl_info = {
    "name": "Blender Shape Fitter",
    "author": "Your Name",
    "version": (1, 2, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Tool Shelf",
    "description": "Fit primitives (sphere, plane, cylinder, ellipse, box) to selected vertices.",
    "category": "Mesh",
}

import bpy
from . import ui, operations

def register():
    ui.register()
    operations.register()

def unregister():
    ui.unregister()
    operations.unregister()

if __name__ == "__main__":
    register()
