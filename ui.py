import bpy

class CondyleVertex(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()

class SHAPEFITTER_PT_panel(bpy.types.Panel):
    bl_label = "Shape Fitter"
    bl_idname = "SHAPEFITTER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ShapeFitter'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "shapefitter_shape", text="Shape")
        if scene.shapefitter_shape == 'CONDYLE_CYLINDER':
            box = layout.box()
            box.label(text="Condyle 1 Vertices:")
            row = box.row(align=True)
            row.label(text=f"Count: {len(scene.condyle1_verts)}")
            row.operator("shapefitter.add_condyle1", text="Add")
            row.operator("shapefitter.clear_condyle1", text="Clear")
            box.label(text="Condyle 2 Vertices:")
            row = box.row(align=True)
            row.label(text=f"Count: {len(scene.condyle2_verts)}")
            row.operator("shapefitter.add_condyle2", text="Add")
            row.operator("shapefitter.clear_condyle2", text="Clear")
        layout.operator("shapefitter.calculate", text="Calculate")


def register():
    bpy.utils.register_class(CondyleVertex)
    bpy.types.Scene.shapefitter_shape = bpy.props.EnumProperty(
        name="Shape",
        description="Primitive to fit",
        items=[
            ('SPHERE', "Sphere", "Fit a sphere"),
            ('PLANE', "Plane", "Fit a plane"),
            ('CYLINDER', "Cylinder", "Fit a cylinder"),
            ('CONDYLE_CYLINDER', "2 condyle cylinder", "Fit a cylinder using two condyle vertex sets")
        ],
        default='SPHERE'
    )
    bpy.types.Scene.condyle1_verts = bpy.props.CollectionProperty(type=CondyleVertex)
    bpy.types.Scene.condyle2_verts = bpy.props.CollectionProperty(type=CondyleVertex)
    bpy.utils.register_class(SHAPEFITTER_PT_panel)


def unregister():
    bpy.utils.unregister_class(CondyleVertex)
    del bpy.types.Scene.shapefitter_shape
    del bpy.types.Scene.condyle1_verts
    del bpy.types.Scene.condyle2_verts
    bpy.utils.unregister_class(SHAPEFITTER_PT_panel)
