import bpy
import mathutils

try:
    import numpy as np
except ImportError:
    np = None

def fit_cylinder(verts, obj, operator=None):
    if len(verts) < 6:
        if operator is not None:
            operator.report({'WARNING'}, "Need at least 6 vertices to fit a cylinder.")
        return
    # Convert verts to world coordinates
    world_verts = [obj.matrix_world @ v for v in verts]
    if np:
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
        # 3D center of the circle (on the plane)
        center3d = centroid + center2d[0]*u + center2d[1]*v
        # Height: span of points along axis
        heights = np.dot(points - center3d, axis)
        height = heights.max() - heights.min()
        # Place cylinder at center of span
        center3d_cyl = center3d + axis * (heights.max() + heights.min())/2
    else:
        # Fallback: use bounding box and centroid
        centroid = mathutils.Vector((0,0,0))
        for v in world_verts:
            centroid += v
        centroid /= len(world_verts)
        axis = mathutils.Vector((0,0,1))
        radius = sum((v - centroid).length for v in world_verts) / len(world_verts)
        height = max((v - centroid).dot(axis) for v in world_verts) - min((v - centroid).dot(axis) for v in world_verts)
        center3d_cyl = centroid
    # Add cylinder at center3d_cyl, aligned to axis, with radius and height
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=center3d_cyl)
    cyl = bpy.context.active_object
    up = mathutils.Vector((0,0,1))
    n = mathutils.Vector(axis)
    if n.length > 0:
        n.normalize()
        rot = up.rotation_difference(n)
        cyl.rotation_euler = rot.to_euler()
