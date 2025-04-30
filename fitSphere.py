import bpy
import mathutils

try:
    import numpy as np
except ImportError:
    np = None

def fit_sphere(verts, obj, operator=None):
    if len(verts) < 4:
        if operator is not None:
            operator.report({'WARNING'}, "Need at least 4 vertices to fit a sphere.")
        return
    # Convert verts to world coordinates
    world_verts = [obj.matrix_world @ v for v in verts]
    if np:
        # Algebraic sphere fit: (x-a)^2 + (y-b)^2 + (z-c)^2 = r^2
        A = []
        B = []
        for v in world_verts:
            x, y, z = v.x, v.y, v.z
            A.append([2*x, 2*y, 2*z, 1])
            B.append(x*x + y*y + z*z)
        A = np.array(A)
        B = np.array(B)
        sol, *_ = np.linalg.lstsq(A, B, rcond=None)
        center = sol[:3]
        radius = np.sqrt(sol[3] + center.dot(center))
    else:
        # Fallback: centroid and average distance
        center = mathutils.Vector((0,0,0))
        for v in world_verts:
            center += v
        center /= len(world_verts)
        radius = sum((v - center).length for v in world_verts) / len(world_verts)
    # Add sphere at center with radius
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=center)
