# blenderShapeFitter
Fit primitive shapes to vertex selections in Blender.

## General Usage
1. Enter Edit Mode on your mesh object.
2. Select the vertices you want to use for fitting.
3. In the ShapeFitter panel (View3D > Sidebar > ShapeFitter), select the shape you want.
4. Choose the **Centering Method** (Average or Midpoint) for Sphere, Plane, Cylinder, and 2-condyle cylinder.
5. Click **Calculate**.

![Screenshot 2025-04-29 103737](https://github.com/user-attachments/assets/9fc1cd9c-9255-44e3-8a62-80f82d665d0f)

## Centering Method
- **Average:** Uses the centroid (average position) of the selected vertices or regions.
- **Midpoint:** Uses the midpoint of the bounding box or height span, projected onto the shape's axis or plane.


All shapes have local axes oriented correctly.
---

## Shape Instructions

### Sphere
- **Minimum vertices:** 4
- **Steps:**
  1. Enter Edit Mode and select at least 4 vertices.
  2. Choose **Sphere** from the Shape dropdown.
  3. Click **Calculate**. A sphere will be fit to the selected vertices.

### Plane
- **Minimum vertices:** 3
- **Steps:**
  1. Enter Edit Mode and select at least 3 vertices.
  2. Choose **Plane** from the Shape dropdown.
  3. Choose a centering method.
  4. Click **Calculate**. A plane will be fit to the selected vertices.

### Cylinder
- **Minimum vertices:** 6
- **Steps:**
  1. Enter Edit Mode and select at least 6 vertices.
  2. Choose **Cylinder** from the Shape dropdown.
  3. Choose a centering method.
  4. Click **Calculate**. A cylinder will be fit to the selected vertices.
  5. *Note:* Cylinder fitting now uses the full height span of selected vertices for improved accuracy.

### 2 Condyle Cylinder
- **Minimum vertices:** 3 per condyle (two sets)
- **Steps:**
  1. Enter Edit Mode and select at least 3 vertices for the first condyle region.
  2. In the ShapeFitter panel, click **Add** under "Condyle 1 Vertices" to store the selection.
  3. Select at least 3 vertices for the second condyle region.
  4. Click **Add** under "Condyle 2 Vertices" to store the second set.
  5. Choose **2 condyle cylinder** from the Shape dropdown.
  6. Choose a centering method.
  7. Click **Calculate**. A cylinder will be fit using both condyle vertex sets, with height based on the full span of all vertices.
  8. Use **Clear** to reset either condyle set if needed.

---

## Troubleshooting
- Make sure you are in Edit Mode and have a mesh object selected.
- Ensure you have selected enough vertices for the chosen shape.
- For 2 condyle cylinder, both condyle sets must be added before calculating.

---

Cylinder fitting may be less robust due to geometric ambiguity.
