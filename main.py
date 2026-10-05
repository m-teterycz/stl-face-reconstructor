import stl_reader
from mesh import Mesh
import triangle
from step_writer import StepWriter
from face import Face
from step_writer import CartesianPoint, Direction, VertexPoint, Line, Vector, EdgeCurve, OrientedEdge, EdgeLoop, FaceOuterBound, AXIS2_PLACEMENT_3D, Normal, Plane, AdvancedFace, ClosedShell, ManifoldSolidBrep
import geometry_math


data = stl_reader.read_data('square_pyramid.stl')
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
    stepwriter.cartesian_registry_i[Cartesian_Point.id] = vertex

    Vertex_Point = VertexPoint(f"#{Cartesian_Point.id}")
    stepwriter.register(Vertex_Point)
    stepwriter.vertex_registry[vertex] = Vertex_Point.id

for face in mesh.faces:
    OrientedEdges = []
    Normal1 = Normal(face.normal)
    stepwriter.register(Normal1)
    stepwriter.normal_registry[Normal1.normal] = Normal1.id

    for edge in face.edges:
        magnitude = geometry_math.magnitude(geometry_math.vector(edge[0], edge[1]))
        data = frozenset(edge)
        if data not in stepwriter.direction_registry:
            Direction1 = Direction(edge)
            stepwriter.register(Direction1)
            stepwriter.direction_registry[data] = Direction1.id
            stepwriter.direction_registry_i[Direction1.id] = data

            Vector1 = Vector(Direction1.id, magnitude)
            stepwriter.register(Vector1)
            stepwriter.vector_registry[data] = Vector1.id

            Line1 = Line(f"#{stepwriter.cartesian_registry[edge[0]]}", f"#{stepwriter.current_id}")
            stepwriter.register(Line1)
            stepwriter.line_registry[data] = Line1.id

        data = frozenset((stepwriter.vertex_registry[edge[0]], stepwriter.vertex_registry[edge[1]]))
        
        if data not in stepwriter.edgecurve_registry:
            EdgeCurve1 = EdgeCurve(stepwriter.vertex_registry[edge[0]], stepwriter.vertex_registry[edge[1]], Line1.id)
            stepwriter.register(EdgeCurve1)
            stepwriter.edgecurve_registry[data] = EdgeCurve1.id
            stepwriter.edgecurve_direction[data] = (edge[0], edge[1])
            stepwriter.edgecurve_registry_i[EdgeCurve1.id] = data


        EdgeCurveid = stepwriter.edgecurve_registry[data]
        original_edge = stepwriter.edgecurve_direction[data]

        if original_edge == (edge[0], edge[1]):
            ending = ".T."
        else:
            ending = ".F."
        OrientedEdge1 = OrientedEdge(EdgeCurveid, ending)
        stepwriter.register(OrientedEdge1)
        stepwriter.orientededge_registry[OrientedEdge1] = OrientedEdge1.id 

        OrientedEdges.append(OrientedEdge1.id)     
            
    EdgeLoop1 =  EdgeLoop(OrientedEdges)
    stepwriter.register(EdgeLoop1)
    stepwriter.edgeloop_registry[EdgeLoop1] = EdgeLoop1.id

    FaceOuterBound1 = FaceOuterBound(EdgeLoop1.id)
    stepwriter.register(FaceOuterBound1)
    stepwriter.faceouterbound_registry[FaceOuterBound1] = FaceOuterBound1.id

    Axis2_Placement_3D = AXIS2_PLACEMENT_3D(stepwriter.cartesian_registry[face.vertices[0]], stepwriter.normal_registry[face.normal], stepwriter.direction_registry[frozenset(face.edges[0])])
    stepwriter.register(Axis2_Placement_3D)
    stepwriter.Axis2_Placement_3D_registry[Axis2_Placement_3D] = Axis2_Placement_3D.id

    Plane1 = Plane(Axis2_Placement_3D.id)
    stepwriter.register(Plane1)
    stepwriter.plane_registry[Plane1] = Plane1.id

Advanced_Faces = []

for i in range(len(stepwriter.faceouterbound_registry)):
    AdvancedFace1 = AdvancedFace(list(stepwriter.faceouterbound_registry.values())[i], list(stepwriter.plane_registry.values())[i])
    stepwriter.register(AdvancedFace1)
    stepwriter.plane_registry[AdvancedFace1] = AdvancedFace1.id
    Advanced_Faces.append(AdvancedFace1.id)

ClosedShell1 = ClosedShell(Advanced_Faces)
stepwriter.register(ClosedShell1)

ManifoldSolidBrep1 = ManifoldSolidBrep("cube", ClosedShell1.id)
stepwriter.register(ManifoldSolidBrep1)

stepwriter.write_data(open("OUTPUT.step", "w"))