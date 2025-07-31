import bpy
import mathutils
import numpy as np

def fit_sphere(verts, obj, operator=None):
    if len(verts) < 4:
        if operator is not None:
            operator.report({'WARNING'}, "Need at least 4 vertices to fit a sphere.")
        return
    # Convert verts to world coordinates
    world_verts = [obj.matrix_world @ v for v in verts]
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
    # Add sphere at center with radius
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=center)
