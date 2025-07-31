import bpy
import numpy as np
import mathutils

def fit_ellipsoid(verts, obj, operator=None, centering=None):
    # centering is now passed explicitly
    if len(verts) < 9:
        if operator:
            operator.report({'WARNING'}, "Need at least 9 vertices to fit an ellipsoid.")
        return

    # Convert verts (object-space) to world coordinates and numpy array
    world_verts = [obj.matrix_world @ v for v in verts]
    points = np.array([[v.x, v.y, v.z] for v in world_verts])

    # Determine center based on centering method
    if centering == 'MIDPOINT':
        min_corner = points.min(axis=0)
        max_corner = points.max(axis=0)
        center = (min_corner + max_corner) / 2
    else:  # Default to centroid
        center = points.mean(axis=0)

    # PCA: axes, radii
    centered = points - center
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    axes = Vt  # principal axes
    # Project points onto principal axes
    proj = centered @ axes.T
    # Radii: half the range along each principal axis (bounding box fit)
    radii = (proj.max(axis=0) - proj.min(axis=0)) / 2

    # Create ellipsoid as a scaled sphere at origin
    import mathutils
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0,0,0), segments=32, ring_count=16)
    ellipsoid = bpy.context.active_object
    ellipsoid.scale = tuple(np.abs(radii))
    # Align axes
    rot = mathutils.Matrix(axes.T)
    ellipsoid.rotation_euler = rot.to_euler()
    # Set location
    ellipsoid.location = tuple(center.tolist())
    ellipsoid.name = 'FittedEllipsoid'
