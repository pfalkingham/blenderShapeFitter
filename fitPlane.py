
import bpy
import mathutils
import random
import numpy as np

def fit_plane(verts, obj, subsample=True, operator=None, centering='AVERAGE'):
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
    points = np.array([[v.x, v.y, v.z] for v in world_verts])
    centroid = points.mean(axis=0)
    centered = points - centroid
    _, _, vh = np.linalg.svd(centered)
    normal = vh[2, :]
    plane_normal = normal / np.linalg.norm(normal)
    # Centering logic
    if centering == 'MIDPOINT':
        min_xyz = points.min(axis=0)
        max_xyz = points.max(axis=0)
        midpoint = (min_xyz + max_xyz) / 2
        # Project midpoint onto plane
        to_plane = midpoint - centroid
        dist = np.dot(to_plane, plane_normal)
        location = midpoint - dist * plane_normal
    else:
        location = centroid
    diffs = points - centroid
    axis1 = vh[0, :]
    axis2 = vh[1, :]
    proj = diffs - np.outer(np.dot(diffs, plane_normal), plane_normal)
    coords1 = np.dot(proj, axis1)
    coords2 = np.dot(proj, axis2)
    size1 = coords1.max() - coords1.min()
    size2 = coords2.max() - coords2.min()
    plane_size = max(size1, size2) * 1.05
    bpy.ops.mesh.primitive_plane_add(size=plane_size, location=location)
    plane = bpy.context.active_object
    # Align plane normal
    up = mathutils.Vector((0,0,1))
    n = mathutils.Vector(normal)
    if n.length > 0:
        n.normalize()
        rot = up.rotation_difference(n)
        plane.rotation_euler = rot.to_euler()
    # Optionally scale plane to fit points (not implemented)
