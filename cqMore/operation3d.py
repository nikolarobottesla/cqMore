from cadquery import (
    Vector, 
    Edge, 
    Wire, 
    Solid, 
    Shell, 
    Face, 
    DirectionSelector
)

def _polyhedron(points, faces):
    def _edges(vectors, face_indices):
        leng_vertices = len(face_indices)   
        return (
            Edge.makeLine(
                vectors[face_indices[i]], 
                vectors[face_indices[(i + 1) % leng_vertices]]
            ) 
            for i in range(leng_vertices)
        )

    vectors = [Vector(*p) for p in points]

    return Solid.makeSolid(
        Shell.makeShell(
            Face.makeFromWires(
                Wire.assembleEdges(
                    _edges(vectors, face_indices)
                )
            )
            for face_indices in faces
        )
    )
    
def polyhedron(workplane, points, faces, combine = True, clean = True):
    poly = _polyhedron(points, faces)
    poly_all = workplane.eachpoint(lambda loc: poly.moved(loc), True)
    
    if not combine:
        return poly_all
    else:
        return workplane.union(poly_all, clean=clean)
    
def surface(workplane, points, thickness, combine = True, clean = True):
    def _surface(points, thickness):
        leng_row = len(points)
        leng_col = len(points[0])
        leng_pts = leng_col * leng_row

        def _all_pts():
            half_thickness = thickness / 2

            vectors = [[Vector(*p) for p in row] for row in points]
            face = Face.makeSplineApprox([[
                         Vector(*points[ri][ci]) 
                    for ri in range(leng_row)
                ] for ci in range(leng_col)]
            )

            front_thicken_pts = [] 
            back_thicken_pts = [] 
            for row in vectors:
                for vt in row:
                    n = face.normalAt(vt).normalized()
                    v = vt + n.multiply(half_thickness)
                    front_thicken_pts.append([v.x, v.y, v.z])
                    v = vt + n.multiply(-half_thickness)
                    back_thicken_pts.append([v.x, v.y, v.z])
            return front_thicken_pts + back_thicken_pts

        def _all_faces():
            front_faces = []
            for ri in range(leng_row - 1):
                for ci in range(leng_col - 1):
                    front_faces.append([ci + leng_col * ri, (ci + 1) + leng_col * ri, (ci + 1) + leng_col * (ri + 1)])
                    front_faces.append([ci + leng_col * ri, (ci + 1) + leng_col * (ri + 1), ci + leng_col * (ri + 1)])

            back_faces = [[f[2] + leng_pts, f[1] + leng_pts, f[0] + leng_pts] for f in front_faces]

            side_faces1 = []
            for ci in range(leng_col - 1):
                side_faces1.append([ci, ci + leng_pts, ci + 1])
                side_faces1.append([ci + leng_pts, ci + leng_pts + 1, ci + 1])

            side_faces2 = []
            rx = leng_col - 1
            for ri in range(leng_row - 1):
                side_faces2.append([rx + (ri + 1) * leng_col + leng_pts, rx + (ri + 1) * leng_col, rx + ri * leng_col])
                side_faces2.append([rx + ri * leng_row + leng_pts, rx + (ri + 1) * leng_col + leng_pts, rx + ri * leng_col])

            side_faces3 = []
            for ci in range(leng_pts - leng_col, leng_pts - 1):
                side_faces3.append([ci + 1, ci + leng_pts, ci])
                side_faces3.append([ci + 1, ci + leng_pts + 1, ci + leng_pts])

            side_faces4 = []
            for ri in range(leng_row - 1):
                side_faces4.append([ri * leng_col, (ri + 1) * leng_col, (ri + 1) * leng_col + leng_pts])
                side_faces4.append([ri * leng_col, (ri + 1) * leng_col + leng_pts, ri * leng_row + leng_pts])

            return front_faces + back_faces + side_faces1 + side_faces2 + side_faces3 + side_faces4

        return _polyhedron(_all_pts(), _all_faces())

    sf = _surface(points, thickness)
    sf_all = workplane.eachpoint(lambda loc: sf.moved(loc), True)
    
    if not combine:
        return sf_all
    else:
        return workplane.union(sf_all, clean=clean)