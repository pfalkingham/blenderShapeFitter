import bpy

class CondyleVertex(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()

class ShapeFitterProperties(bpy.types.PropertyGroup):
    shapefitter_shape: bpy.props.EnumProperty(
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
    shapefitter_plane_subsample: bpy.props.BoolProperty(
        name="Subsample for plane fitting",
        description="Randomly subsample up to 10,000 vertices for plane fitting (faster for large selections)",
        default=True
    )
    condyle1_verts: bpy.props.CollectionProperty(type=CondyleVertex)
    condyle2_verts: bpy.props.CollectionProperty(type=CondyleVertex)
    shapefitter_centering: bpy.props.EnumProperty(
        name="Centering Method",
        description="Method to center the shape",
        items=[
            ('AVERAGE', "Average", "Use average/centroid for location"),
            ('MIDPOINT', "Midpoint", "Use midpoint of bounding box/height span for location")
        ],
        default='MIDPOINT'
    )

class SHAPEFITTER_PT_panel(bpy.types.Panel):
    bl_label = "Shape Fitter"
    bl_idname = "SHAPEFITTER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ShapeFitter'

    def draw(self, context):
        layout = self.layout
        props = context.scene.shapefitter_props
        layout.prop(props, "shapefitter_shape", text="Shape")
        # Show centering method for all relevant shapes
        if props.shapefitter_shape in {'PLANE', 'CYLINDER', 'CONDYLE_CYLINDER'}:
            layout.prop(props, "shapefitter_centering", text="Centering Method")
        if props.shapefitter_shape == 'PLANE':
            layout.prop(props, "shapefitter_plane_subsample", text="Subsample for plane fitting (max 10,000)")
        if props.shapefitter_shape == 'CONDYLE_CYLINDER':
            box = layout.box()
            box.label(text="Condyle 1 Vertices:")
            row = box.row(align=True)
            row.label(text=f"Count: {len(props.condyle1_verts)}")
            row.operator("object.shapefitter_add_condyle1", text="Add")
            row.operator("object.shapefitter_clear_condyle1", text="Clear")
            box.label(text="Condyle 2 Vertices:")
            row = box.row(align=True)
            row.label(text=f"Count: {len(props.condyle2_verts)}")
            row.operator("object.shapefitter_add_condyle2", text="Add")
            row.operator("object.shapefitter_clear_condyle2", text="Clear")
        layout.operator("object.shapefitter_calculate", text="Calculate")


def register():
    bpy.utils.register_class(CondyleVertex)
    bpy.utils.register_class(ShapeFitterProperties)
    bpy.types.Scene.shapefitter_props = bpy.props.PointerProperty(type=ShapeFitterProperties)
    bpy.utils.register_class(SHAPEFITTER_PT_panel)


def unregister():
    bpy.utils.unregister_class(CondyleVertex)
    bpy.utils.unregister_class(ShapeFitterProperties)
    del bpy.types.Scene.shapefitter_props
    bpy.utils.unregister_class(SHAPEFITTER_PT_panel)
