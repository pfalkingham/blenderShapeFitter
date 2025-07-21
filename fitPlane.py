import bpy
import mathutils
import random

try:
    import numpy as np
except ImportError:
    np = None

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
    if np:
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
    else:
        centroid = mathutils.Vector((0,0,0))
        for v in world_verts:
            centroid += v
        centroid /= len(world_verts)
        # Centering logic
        if centering == 'MIDPOINT':
            min_x = min(v.x for v in world_verts)
            max_x = max(v.x for v in world_verts)
            min_y = min(v.y for v in world_verts)
            max_y = max(v.y for v in world_verts)
            min_z = min(v.z for v in world_verts)
            max_z = max(v.z for v in world_verts)
            midpoint = mathutils.Vector(((min_x+max_x)/2, (min_y+max_y)/2, (min_z+max_z)/2))
            # Project midpoint onto plane (using Z axis as normal)
            normal = mathutils.Vector((0,0,1))
            to_plane = midpoint - centroid
            dist = to_plane.dot(normal)
            location = midpoint - dist * normal
        else:
            location = centroid
        cov = mathutils.Matrix(((0,0,0), (0,0,0), (0,0,0)))
        for v in world_verts:
            d = v - centroid
            for i in range(3):
                for j in range(3):
                    cov[i][j] += d[i]*d[j]
        # Fallback: use Z axis as normal
        normal = mathutils.Vector((0,0,1))
        local_points = [v - centroid for v in world_verts]
        size1 = max(v.x for v in local_points) - min(v.x for v in local_points)
        size2 = max(v.y for v in local_points) - min(v.y for v in local_points)
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
