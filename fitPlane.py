import bpy
import mathutils

try:
    import numpy as np
except ImportError:
    np = None

def fit_plane(verts, obj):
    if len(verts) < 3:
        bpy.ops.message.box('INVOKE_DEFAULT', message="Need at least 3 vertices to fit a plane.")
        return
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
    bpy.ops.mesh.primitive_plane_add(size=1, location=centroid)
    plane = bpy.context.active_object
    # Align plane normal
    up = mathutils.Vector((0,0,1))
    n = mathutils.Vector(normal)
    if n.length > 0:
        n.normalize()
        rot = up.rotation_difference(n)
        plane.rotation_euler = rot.to_euler()
    # Optionally scale plane to fit points (not implemented)
