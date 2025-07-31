import bpy
import mathutils
import numpy as np

def fit_cylinder(verts, obj, operator=None, centering='AVERAGE'):
    if len(verts) < 6:
        if operator is not None:
            operator.report({'WARNING'}, "Need at least 6 vertices to fit a cylinder.")
        return
    # Convert verts to world coordinates
    world_verts = [obj.matrix_world @ v for v in verts]
    points = np.array([[v.x, v.y, v.z] for v in world_verts])
    centroid = points.mean(axis=0)
    centered = points - centroid
    # PCA: axis is first principal component
    _, _, vh = np.linalg.svd(centered)
    axis = vh[0, :]
    axis = axis / np.linalg.norm(axis)
    # Build orthonormal basis (axis, u, v)
    u = vh[1, :]
    v = vh[2, :]
    # Ensure axis is Z, u is X, v is Y for Blender convention
    z_axis = axis
    x_axis = u
    y_axis = v
    # Project points onto plane perpendicular to axis
    proj = np.dot(points - centroid, np.vstack([u, v]).T)
    x = proj[:, 0]
    y = proj[:, 1]
    # Fit circle to projected points
    A = np.c_[2*x, 2*y, np.ones_like(x)]
    B = x**2 + y**2
    sol, *_ = np.linalg.lstsq(A, B, rcond=None)
    center2d = sol[:2]
    radius = np.sqrt(sol[2] + center2d.dot(center2d))
    center3d = centroid + center2d[0]*u + center2d[1]*v
    # Height: full span of points projected onto axis
    heights = np.dot(points - center3d, axis)
    height = heights.max() - heights.min()
    if centering == 'MIDPOINT':
        mid_height = (heights.max() + heights.min()) / 2
        location = center3d + axis * mid_height
    else:
        location = centroid
    # Add cylinder at center3d_cyl, aligned to axis, with radius and height
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=location)
    cyl = bpy.context.active_object
    up = mathutils.Vector((0,0,1))
    n = mathutils.Vector(axis)
    if n.length > 0:
        n.normalize()
        rot = up.rotation_difference(n)
        cyl.rotation_euler = rot.to_euler()
    # Add cylinder at center3d_cyl, aligned to axis, with radius and height
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=location)
    cyl = bpy.context.active_object
    up = mathutils.Vector((0,0,1))
    n = mathutils.Vector(axis)
    if n.length > 0:
        n.normalize()
        rot = up.rotation_difference(n)
        cyl.rotation_euler = rot.to_euler()
