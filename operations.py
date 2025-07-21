import bpy
from . import fitSphere, fitPlane, fitCylinder, fitCondyleCylinder

class OBJECT_OT_shapefitter_add_condyle1(bpy.types.Operator):
    bl_idname = "object.shapefitter_add_condyle1"
    bl_label = "Add Condyle 1"
    def execute(self, context):
        props = context.scene.shapefitter_props
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected.")
            return {'CANCELLED'}
        if not obj.mode == 'EDIT':
            self.report({'WARNING'}, "Object must be in Edit Mode.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        coll = props.condyle1_verts
        coll.clear()
        for v in obj.data.vertices:
            if v.select:
                item = coll.add()
                item.index = v.index
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class OBJECT_OT_shapefitter_clear_condyle1(bpy.types.Operator):
    bl_idname = "object.shapefitter_clear_condyle1"
    bl_label = "Clear Condyle 1"
    def execute(self, context):
        props = context.scene.shapefitter_props
        props.condyle1_verts.clear()
        return {'FINISHED'}

class OBJECT_OT_shapefitter_add_condyle2(bpy.types.Operator):
    bl_idname = "object.shapefitter_add_condyle2"
    bl_label = "Add Condyle 2"
    def execute(self, context):
        props = context.scene.shapefitter_props
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected.")
            return {'CANCELLED'}
        if not obj.mode == 'EDIT':
            self.report({'WARNING'}, "Object must be in Edit Mode.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        coll = props.condyle2_verts
        coll.clear()
        for v in obj.data.vertices:
            if v.select:
                item = coll.add()
                item.index = v.index
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class OBJECT_OT_shapefitter_clear_condyle2(bpy.types.Operator):
    bl_idname = "object.shapefitter_clear_condyle2"
    bl_label = "Clear Condyle 2"
    def execute(self, context):
        props = context.scene.shapefitter_props
        props.condyle2_verts.clear()
        return {'FINISHED'}

class OBJECT_OT_shapefitter_calculate(bpy.types.Operator):
    bl_idname = "object.shapefitter_calculate"
    bl_label = "Fit Shape to Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.shapefitter_props
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected.")
            return {'CANCELLED'}
        if not obj.mode == 'EDIT':
            self.report({'WARNING'}, "Object must be in Edit Mode.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        shape = props.shapefitter_shape
        centering = props.shapefitter_centering
        if shape == 'SPHERE':
            selected_verts = [v.co for v in obj.data.vertices if v.select]
            if not selected_verts:
                self.report({'WARNING'}, "No vertices selected.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            fitSphere.fit_sphere(selected_verts, obj, self)
        elif shape == 'PLANE':
            selected_verts = [v.co for v in obj.data.vertices if v.select]
            if not selected_verts:
                self.report({'WARNING'}, "No vertices selected.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            subsample = props.shapefitter_plane_subsample
            fitPlane.fit_plane(selected_verts, obj, subsample=subsample, operator=self, centering=centering)
        elif shape == 'CYLINDER':
            selected_verts = [v.co for v in obj.data.vertices if v.select]
            if not selected_verts:
                self.report({'WARNING'}, "No vertices selected.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            fitCylinder.fit_cylinder(selected_verts, obj, self, centering=centering)
        elif shape == 'CONDYLE_CYLINDER':
            coll1 = props.condyle1_verts
            coll2 = props.condyle2_verts
            if not coll1 or not coll2:
                self.report({'WARNING'}, "Both condyle vertex sets must be added.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            verts1 = [obj.data.vertices[item.index].co.copy() for item in coll1]
            verts2 = [obj.data.vertices[item.index].co.copy() for item in coll2]
            fitCondyleCylinder.fit_condyle_cylinder(verts1, verts2, obj, self, centering=centering)
            # Clear condyle vertex sets after calculation
            coll1.clear()
            coll2.clear()
        elif shape == 'BOX':
            selected_verts = [v.co for v in obj.data.vertices if v.select]
            if not selected_verts:
                self.report({'WARNING'}, "No vertices selected.")
                bpy.ops.object.mode_set(mode='EDIT')
                return {'CANCELLED'}
            fitCube.fit_cube(selected_verts, obj, self)
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_shapefitter_add_condyle1)
    bpy.utils.register_class(OBJECT_OT_shapefitter_clear_condyle1)
    bpy.utils.register_class(OBJECT_OT_shapefitter_add_condyle2)
    bpy.utils.register_class(OBJECT_OT_shapefitter_clear_condyle2)
    bpy.utils.register_class(OBJECT_OT_shapefitter_calculate)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_shapefitter_add_condyle1)
    bpy.utils.unregister_class(OBJECT_OT_shapefitter_clear_condyle1)
    bpy.utils.unregister_class(OBJECT_OT_shapefitter_add_condyle2)
    bpy.utils.unregister_class(OBJECT_OT_shapefitter_clear_condyle2)
    bpy.utils.unregister_class(OBJECT_OT_shapefitter_calculate)
