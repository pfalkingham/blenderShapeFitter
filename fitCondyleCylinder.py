import bpy
import mathutils

try:
    import numpy as np
except ImportError:
    np = None

def fit_condyle_cylinder(verts1, verts2, obj, operator=None):
    """
    Fit a cylinder using two sets of condyle vertices.
    verts1, verts2: lists of mathutils.Vector (local coordinates)
    obj: Blender object
    """
    if len(verts1) < 3 or len(verts2) < 3:
        if operator is not None:
            operator.report({'WARNING'}, "Need at least 3 vertices per condyle.")
        return
    # Convert verts to world coordinates
    world_verts1 = [obj.matrix_world @ v for v in verts1]
    world_verts2 = [obj.matrix_world @ v for v in verts2]
    if np:
        # Fit sphere to each condyle to get center and radius
        def fit_sphere_np(verts):
            A = []
            B = []
            for v in verts:
                x, y, z = v.x, v.y, v.z
                A.append([2*x, 2*y, 2*z, 1])
                B.append(x*x + y*y + z*z)
            A = np.array(A)
            B = np.array(B)
            sol, *_ = np.linalg.lstsq(A, B, rcond=None)
            center = sol[:3]
            radius = np.sqrt(sol[3] + center.dot(center))
            return mathutils.Vector(center), radius
        center1, radius1 = fit_sphere_np(world_verts1)
        center2, radius2 = fit_sphere_np(world_verts2)
    else:
        # Fallback: centroid and average distance
        def fit_sphere_fallback(verts):
            center = mathutils.Vector((0,0,0))
            for v in verts:
                center += v
            center /= len(verts)
            radius = sum((v - center).length for v in verts) / len(verts)
            return center, radius
        center1, radius1 = fit_sphere_fallback(world_verts1)
        center2, radius2 = fit_sphere_fallback(world_verts2)
    # Cylinder axis: line from center1 to center2
    axis = center2 - center1
    height = axis.length
    if height == 0:
        if operator is not None:
            operator.report({'WARNING'}, "Condyle centers are coincident.")
        return
    axis_norm = axis.normalized()
    # Cylinder center: midpoint between centers
    cyl_center = (center1 + center2) / 2
    # Cylinder radius: average of condyle radii
    cyl_radius = (radius1 + radius2) / 2
    # Add cylinder at cyl_center, aligned to axis, with radius and height
    bpy.ops.mesh.primitive_cylinder_add(radius=cyl_radius, depth=height, location=cyl_center)
    cyl = bpy.context.active_object
    up = mathutils.Vector((0,0,1))
    n = axis_norm
    if n.length > 0:
        n.normalize()
        rot = up.rotation_difference(n)
        cyl.rotation_euler = rot.to_euler()
