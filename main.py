import stl_reader
from mesh import Mesh
import triangle
from step_writer import StepWriter
from face import Face
from step_writer import CartesianPoint, Direction, VertexPoint, Line
import geometry_math


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
    stepwriter.cartesian_registry[vertex] = Cartesian_Point.id

    Vertex_Point = VertexPoint(f"#{Cartesian_Point.id}")
    stepwriter.register(Vertex_Point)
    stepwriter.vertex_registry[vertex] = Vertex_Point.id

for edge in face.edges: # Add lines and direction
    Direction1 = Direction(edge)
    Line1 = Line(f"#{stepwriter.cartesian_registry[edge[0]]}", f"#{stepwriter.current_id + 1}")

    stepwriter.register(Direction1)
    stepwriter.register(Line1)

    stepwriter.direction_registry[Direction1] = Direction1.id
    stepwriter.line_registry[Line1] = Line1.id

stepwriter.write_data(open("OUTPUT.step", "w"))