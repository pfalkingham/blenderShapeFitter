import bpy
from . import fitSphere, fitPlane, fitCylinder

class SHAPEFITTER_OT_calculate(bpy.types.Operator):
    bl_idname = "shapefitter.calculate"
    bl_label = "Fit Shape to Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected.")
            return {'CANCELLED'}
        if not obj.mode == 'EDIT':
            self.report({'WARNING'}, "Object must be in Edit Mode.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_verts = [v.co for v in obj.data.vertices if v.select]
        if not selected_verts:
            self.report({'WARNING'}, "No vertices selected.")
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}
        shape = context.scene.shapefitter_shape
        if shape == 'SPHERE':
            fitSphere.fit_sphere(selected_verts, obj)
        elif shape == 'PLANE':
            fitPlane.fit_plane(selected_verts, obj)
        elif shape == 'CYLINDER':
            fitCylinder.fit_cylinder(selected_verts, obj)
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SHAPEFITTER_OT_calculate)

def unregister():
    bpy.utils.unregister_class(SHAPEFITTER_OT_calculate)
