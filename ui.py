import bpy

class SHAPEFITTER_PT_panel(bpy.types.Panel):
    bl_label = "Shape Fitter"
    bl_idname = "SHAPEFITTER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ShapeFitter'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "shapefitter_shape", expand=True)
        layout.operator("shapefitter.calculate", text="Calculate")

def register():
    bpy.types.Scene.shapefitter_shape = bpy.props.EnumProperty(
        name="Shape",
        description="Primitive to fit",
        items=[
            ('SPHERE', "Sphere", "Fit a sphere"),
            ('PLANE', "Plane", "Fit a plane"),
            ('CYLINDER', "Cylinder", "Fit a cylinder")
        ],
        default='SPHERE'
    )
    bpy.utils.register_class(SHAPEFITTER_PT_panel)

def unregister():
    del bpy.types.Scene.shapefitter_shape
    bpy.utils.unregister_class(SHAPEFITTER_PT_panel)
