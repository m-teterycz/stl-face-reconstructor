import stl_reader
from mesh import Mesh
import triangle
from step_writer import StepWriter
from face import Face

data = stl_reader.read_data('cube.stl')
triangles = triangle.create_triangles(data)

mesh = Mesh(triangles)
mesh.find_neighbours()

co_planar_groups = mesh.find_all_planar_regions()
for i in range(len(co_planar_groups)):
    face = Face(co_planar_groups[i])
    mesh.faces.append(face)


StepWriter(triangles, co_planar_groups)