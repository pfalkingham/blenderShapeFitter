import bpy
from . import fitSphere, fitPlane, fitCylinder, fitCondyleCylinder

class SHAPEFITTER_OT_add_condyle1(bpy.types.Operator):
    bl_idname = "shapefitter.add_condyle1"
    bl_label = "Add Condyle 1"
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected.")
            return {'CANCELLED'}
        if not obj.mode == 'EDIT':
            self.report({'WARNING'}, "Object must be in Edit Mode.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        coll = context.scene.condyle1_verts
        coll.clear()
        for v in obj.data.vertices:
            if v.select:
                item = coll.add()
                item.index = v.index
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class SHAPEFITTER_OT_clear_condyle1(bpy.types.Operator):
    bl_idname = "shapefitter.clear_condyle1"
    bl_label = "Clear Condyle 1"
    def execute(self, context):
        context.scene.condyle1_verts.clear()
        return {'FINISHED'}

class SHAPEFITTER_OT_add_condyle2(bpy.types.Operator):
    bl_idname = "shapefitter.add_condyle2"
    bl_label = "Add Condyle 2"
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected.")
            return {'CANCELLED'}
        if not obj.mode == 'EDIT':
            self.report({'WARNING'}, "Object must be in Edit Mode.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        coll = context.scene.condyle2_verts
        coll.clear()
        for v in obj.data.vertices:
            if v.select:
                item = coll.add()
                item.index = v.index
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class SHAPEFITTER_OT_clear_condyle2(bpy.types.Operator):
    bl_idname = "shapefitter.clear_condyle2"
    bl_label = "Clear Condyle 2"
    def execute(self, context):
        context.scene.condyle2_verts.clear()
        return {'FINISHED'}

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
        shape = context.scene.shapefitter_shape
        if shape == 'SPHERE':
            selected_verts = [v.co for v in obj.data.vertices if v.select]
            if not selected_verts:
                self.report({'WARNING'}, "No vertices selected.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            fitSphere.fit_sphere(selected_verts, obj)
        elif shape == 'PLANE':
            selected_verts = [v.co for v in obj.data.vertices if v.select]
            if not selected_verts:
                self.report({'WARNING'}, "No vertices selected.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            fitPlane.fit_plane(selected_verts, obj)
        elif shape == 'CYLINDER':
            selected_verts = [v.co for v in obj.data.vertices if v.select]
            if not selected_verts:
                self.report({'WARNING'}, "No vertices selected.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            fitCylinder.fit_cylinder(selected_verts, obj)
        elif shape == 'CONDYLE_CYLINDER':
            coll1 = context.scene.condyle1_verts
            coll2 = context.scene.condyle2_verts
            if not coll1 or not coll2:
                self.report({'WARNING'}, "Both condyle vertex sets must be added.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            verts1 = [obj.data.vertices[item.index].co.copy() for item in coll1]
            verts2 = [obj.data.vertices[item.index].co.copy() for item in coll2]
            fitCondyleCylinder.fit_condyle_cylinder(verts1, verts2, obj)
            # Clear condyle vertex sets after calculation
            coll1.clear()
            coll2.clear()
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SHAPEFITTER_OT_add_condyle1)
    bpy.utils.register_class(SHAPEFITTER_OT_clear_condyle1)
    bpy.utils.register_class(SHAPEFITTER_OT_add_condyle2)
    bpy.utils.register_class(SHAPEFITTER_OT_clear_condyle2)
    bpy.utils.register_class(SHAPEFITTER_OT_calculate)


def unregister():
    bpy.utils.unregister_class(SHAPEFITTER_OT_add_condyle1)
    bpy.utils.unregister_class(SHAPEFITTER_OT_clear_condyle1)
    bpy.utils.unregister_class(SHAPEFITTER_OT_add_condyle2)
    bpy.utils.unregister_class(SHAPEFITTER_OT_clear_condyle2)
    bpy.utils.unregister_class(SHAPEFITTER_OT_calculate)
