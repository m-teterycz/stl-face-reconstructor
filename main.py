import stl_reader
from mesh import Mesh
import triangle
from step_writer import StepEntity, StepWriter
from face import Face
from step_writer import CartesianPoint, Direction, VertexPoint


data = stl_reader.read_data('cube.stl')
triangles = triangle.create_triangles(data)

mesh = Mesh(triangles)
mesh.find_neighbours()

co_planar_groups = mesh.find_all_planar_regions()

for i in range(len(co_planar_groups)):
    face = Face(co_planar_groups[i])
    mesh.faces.append(face)

stepwriter = StepWriter(mesh)

for vertex in mesh.vertices: # Register all unique vertices in the mesh to the step file
    Cartesian_Point = CartesianPoint(vertex)
    stepwriter.register(Cartesian_Point) # Generates an id

    Vertex_Point = VertexPoint(f"#{Cartesian_Point.id}")
    stepwriter.register(Vertex_Point)

for face in mesh.faces:
    Direction1 = Direction(face.edges[0])
    stepwriter.register(Direction1)


stepwriter.write_data(open("OUTPUT.step", "w"))