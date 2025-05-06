import bpy
import mathutils
import random

try:
    import numpy as np
except ImportError:
    np = None

def fit_plane(verts, obj, subsample=True, operator=None):
    if len(verts) < 3:
        if operator is not None:
            operator.report({'WARNING'}, "Need at least 3 vertices to fit a plane.")
        return
    # Subsample if requested and too many verts
    max_points = 10000
    if subsample and len(verts) > max_points:
        verts = random.sample(verts, max_points)
    # Convert verts to world coordinates
    world_verts = [obj.matrix_world @ v for v in verts]
    if np:
        points = np.array([[v.x, v.y, v.z] for v in world_verts])
        centroid = points.mean(axis=0)
        centered = points - centroid
        _, _, vh = np.linalg.svd(centered)
        normal = vh[2, :]
    else:
        centroid = mathutils.Vector((0,0,0))
        for v in world_verts:
            centroid += v
        centroid /= len(world_verts)
        cov = mathutils.Matrix(((0,0,0), (0,0,0), (0,0,0)))
        for v in world_verts:
            d = v - centroid
            for i in range(3):
                for j in range(3):
                    cov[i][j] += d[i]*d[j]
        # Fallback: use Z axis as normal
        normal = mathutils.Vector((0,0,1))
    # Add plane at centroid
    # Compute plane size to fit points
    # Project all points onto the plane
    if np:
        # normal and centroid already computed
        plane_normal = normal / np.linalg.norm(normal)
        diffs = points - centroid
        # Project diffs onto plane
        dists = diffs - np.outer(np.dot(diffs, plane_normal), plane_normal)
        # Plane axes: use SVD's first two principal axes
        axis1 = vh[0, :]
        axis2 = vh[1, :]
        # Project points onto these axes
        coords1 = np.dot(dists, axis1)
        coords2 = np.dot(dists, axis2)
        size1 = coords1.max() - coords1.min()
        size2 = coords2.max() - coords2.min()
        plane_size = max(size1, size2)
        # Add a small margin
        plane_size *= 1.05
        bpy.ops.mesh.primitive_plane_add(size=plane_size, location=centroid)
        plane = bpy.context.active_object
        # Set orientation: local Z = normal, X = axis1, Y = axis2
        rot_mat = mathutils.Matrix([
            mathutils.Vector(axis1),
            mathutils.Vector(axis2),
            mathutils.Vector(plane_normal)
        ]).transposed()
        plane.matrix_world = rot_mat.to_4x4()
        plane.location = centroid
    else:
        # fallback: use bounding box in local coordinates
        local_points = [v - centroid for v in world_verts]
        size1 = max(v.x for v in local_points) - min(v.x for v in local_points)
        size2 = max(v.y for v in local_points) - min(v.y for v in local_points)
        plane_size = max(size1, size2) * 1.05
        bpy.ops.mesh.primitive_plane_add(size=plane_size, location=centroid)
        plane = bpy.context.active_object
        # Fallback: align Z to normal (if not default)
        up = mathutils.Vector((0,0,1))
        n = mathutils.Vector(normal)
        if n.length > 0:
            n.normalize()
            rot = up.rotation_difference(n)
            plane.rotation_euler = rot.to_euler()
