import geometry_math
class StepWriter:
    def __init__(self, mesh):
        self.name = "YourName"
        self.application_name = "AppName"
        self.application = "YourApplication"
        self.file_name = "FileName"
        self.file_desc = "Description"
        self.faces = mesh.faces
        self.triangles = mesh.triangles
        self.current_id = 0
        self.registry = [] # Used to write in chronological order

        self.cartesian_registry = {}  # Use these to map a feature e.g coord into its id. _i means key and value pairs swapped around
        self.cartesian_registry_i = {}
        self.vertex_registry = {}     
        self.edge_registry = {}
        self.direction_registry = {}
        self.direction_registry_i = {}
        self.line_registry = {}
        self.vector_registry = {}      
        self.edgecurve_registry = {}
        self.edgecurve_direction = {}
        self.edgecurve_registry_i = {}
        self.orientededge_registry = {}
        self.edgeloop_registry = {}
        self.faceouterbound_registry = {}
        self.normal_registry = {} 
        self.Axis2_Placement_3D_registry = {}
        self.plane_registry = {}


    def build_product_structure(self):
        pass

    def build_representation_structure(self):
        pass

    def write_data(self, f):
        f.write('ISO-10303-21;\nHEADER;\n\n')
        f.write(f"FILE_DESCRIPTION(('{self.file_desc}'),'2;1');\nFILE_NAME('{self.file_name}','2026-08-16T09:00:00',('{self.name}'),('{self.application}'),'','','');\nFILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));\n\n")
        f.write("ENDSEC;\n\n")
        f.write("DATA;\n\n")

        self.build_product_structure()
        self.build_representation_structure()

        for entity in self.registry:
            f.write(entity.get_step_string())
        

        f.write('\nENDSEC;\n')
        f.write('END-ISO-10303-21;')

    def register(self, entity):
        self.current_id += 1

        entity.id = self.current_id
        self.registry.append(entity)

        return entity
         

class StepEntity: # Generic Step Entity
    def __init__(self, name):
        self.id = None
        self.type = name

class CartesianPoint(StepEntity):
    def __init__(self, vertex):
        super().__init__("CARTESIAN_POINT")
        self.coordinates = vertex

    def get_step_string(self):
        return f"#{self.id} = CARTESIAN_POINT('', {self.coordinates});\n"

class Direction(StepEntity):
    def __init__(self, edge):
        super().__init__("DIRECTION")
        self.vector = geometry_math.vector(edge[0], edge[1])
        self.vector = geometry_math.normalize(self.vector)

    def get_step_string(self):
        return f"#{self.id} = DIRECTION('', ({self.vector[0]}, {self.vector[1]}, {self.vector[2]}));\n"

class VertexPoint(StepEntity):
    def __init__(self, vertex):
            super().__init__("VERTEX_POINT")
            self.coordinates = vertex
    
    def get_step_string(self):
        return f"#{self.id} = VERTEX_POINT('', {self.coordinates});\n"

class Line(StepEntity):
    def __init__(self, coords, direction):
            super().__init__("LINE")
            self.coordinates = coords
            self.direction = direction
    
    def get_step_string(self):
        return f"#{self.id} = LINE('', {self.coordinates}, {self.direction});\n"


class Vector(StepEntity):
    def __init__(self,direction, magnitude):
            super().__init__("VECTOR")
            self.magnitude = magnitude
            self.direction = direction
    
    def get_step_string(self):
        return f"#{self.id} = VECTOR('', #{self.direction}, {self.magnitude});\n"

class EdgeCurve(StepEntity):
    def __init__(self, start_v, end_v, curve):
            super().__init__("EDGE_CURVE")
            self.start_v = start_v
            self.end_v = end_v
            self.curve = curve
    
    def get_step_string(self):
        return f"#{self.id} = EDGE_CURVE('', #{self.start_v}, #{self.end_v}, #{self.curve}, .T.);\n"

class OrientedEdge(StepEntity):
    def __init__(self, curve, ending):
            super().__init__("ORIENTED_EDGE")
            self.curve = curve
            self.ending = ending
    
    def get_step_string(self):
        return f"#{self.id} = ORIENTED_EDGE('', *, *, #{self.curve}, {self.ending});\n"

class EdgeLoop(StepEntity):
    def __init__(self, loop):
            super().__init__("EDGE_LOOP")
            self.loop = loop
            for i in range(len(self.loop)):
                 text = f"#{self.loop[i]}"
                 self.loop[i] = text
            self.loop = ", ".join(self.loop)

    def get_step_string(self):
        return f"#{self.id} = EDGE_LOOP('', ({self.loop}));\n"

class FaceOuterBound(StepEntity):
    def __init__(self, prev_id):
            super().__init__("FACE_OUTER_BOUND")
            self.prev_id = prev_id

    def get_step_string(self):
        return f"#{self.id} = FACE_OUTER_BOUND('', #{self.prev_id}, .T.);\n"

class AXIS2_PLACEMENT_3D(StepEntity):
    def __init__(self, location, normal, reference_direction):
            super().__init__("AXIS2_PLACEMENT_3D")
            self.location = location
            self.normal = normal
            self.reference_direction = reference_direction

    def get_step_string(self):
        return f"#{self.id} = AXIS2_PLACEMENT_3D('', #{self.location}, #{self.normal}, #{self.reference_direction});\n"

class Normal(StepEntity):
    def __init__(self, normal):
        super().__init__("DIRECTION")
        self.normal = normal

    def get_step_string(self):
        return f"#{self.id} = DIRECTION('', {self.normal});\n"

class Plane(StepEntity):
    def __init__(self, axis2):
        super().__init__("PLANE")
        self.axis2 = axis2

    def get_step_string(self):
        return f"#{self.id} = PLANE('', #{self.axis2});\n"

class AdvancedFace(StepEntity):
    def __init__(self, faceouterbound, plane):
        super().__init__("ADVANCED_FACE")
        self.faceouterbound = faceouterbound
        self.plane = plane

    def get_step_string(self):
        return f"#{self.id} = ADVANCED_FACE('', (#{self.faceouterbound}), #{self.plane}, .T.);\n"

class ClosedShell(StepEntity):
    def __init__(self, advanced_faces):
        super().__init__("CLOSED_SHELL")
        self.advanced_faces = advanced_faces
        for i,id in enumerate(self.advanced_faces):
            text = f"#{id}"
            self.advanced_faces[i] = text
        self.advanced_faces = ", ".join(self.advanced_faces)

    def get_step_string(self):
        return f"#{self.id} = CLOSED_SHELL('', ({self.advanced_faces}));\n"


class ManifoldSolidBrep(StepEntity):
    def __init__(self, name, closed_shell):
        super().__init__("MANIFOLD_SOLID_BREP")
        self.name = name
        self.closed_shell = closed_shell

    def get_step_string(self):
        return f"#{self.id} = MANIFOLD_SOLID_BREP({"'"+self.name+"'"}, #{self.closed_shell});\n"

class ApplicationContext(StepEntity):
    def __init__(self, name, description):
        super().__init__("APPLICATION_CONTEXT")
        self.description = description

    def get_step_string(self):
        return f"#{self.id} = APPLICATION_CONTEXT({self.description});\n"

class ApplicationProtocolDefinition(StepEntity):

    def __init__(self, status, application_protocol, year, context):
        super().__init__("APPLICATION_PROTOCOL_DEFINITION")
        self.status = status
        self.application_protocol = application_protocol
        self.year = year
        self.context = context

    def get_step_string(self):
        return (
            f"#{self.id} = APPLICATION_PROTOCOL_DEFINITION("
            f"'{self.status}', "
            f"'{self.application_protocol}', "
            f"{self.year}, "
            f"#{self.context});\n"
        )

class ProductContext(StepEntity):

    def __init__(self, discipline_type, application_context, discipline):
        super().__init__("PRODUCT_CONTEXT")
        self.discipline_type = discipline_type
        self.application_context = application_context
        self.discipline = discipline

    def get_step_string(self):
        return (
            f"#{self.id} = PRODUCT_CONTEXT("
            f"'{self.discipline_type}', "
            f"#{self.application_context}, "
            f"'{self.discipline}');\n"
        )

class Product(StepEntity):

    def __init__(self, id_string, name, description, contexts):
        super().__init__("PRODUCT")
        self.id_string = id_string
        self.name = name
        self.description = description
        self.contexts = contexts

    def get_step_string(self):
        contexts = ""

        for i, x in enumerate(self.contexts):
            if i > 0:
                contexts += ", "

            contexts += f"#{x}"

        return (
            f"#{self.id} = PRODUCT("
            f"'{self.id_string}', "
            f"'{self.name}', "
            f"'{self.description}', "
            f"({contexts}));\n"
        )

class ProductDefinitionFormation(StepEntity):

    def __init__(self, id_string, description, product):
        super().__init__("PRODUCT_DEFINITION_FORMATION")
        self.id_string = id_string
        self.description = description
        self.product = product

    def get_step_string(self):
        return (
            f"#{self.id} = PRODUCT_DEFINITION_FORMATION("
            f"'{self.id_string}', "
            f"'{self.description}', "
            f"#{self.product});\n"
        )

class ProductDefinitionContext(StepEntity):

    def __init__(self, name, application_context, life_cycle_stage):
        super().__init__("PRODUCT_DEFINITION_CONTEXT")
        self.name = name
        self.application_context = application_context
        self.life_cycle_stage = life_cycle_stage

    def get_step_string(self):
        return (
            f"#{self.id} = PRODUCT_DEFINITION_CONTEXT("
            f"'{self.name}', "
            f"#{self.application_context}, "
            f"'{self.life_cycle_stage}');\n"
        )

class ProductDefinition(StepEntity):

    def __init__(self, id_string, description, formation, context):
        super().__init__("PRODUCT_DEFINITION")
        self.id_string = id_string
        self.description = description
        self.formation = formation
        self.context = context

    def get_step_string(self):
        return (
            f"#{self.id} = PRODUCT_DEFINITION("
            f"'{self.id_string}', "
            f"'{self.description}', "
            f"#{self.formation}, "
            f"#{self.context});\n"
        )

class ProductDefinitionShape(StepEntity):

    def __init__(self, name, description, definition):
        super().__init__("PRODUCT_DEFINITION_SHAPE")
        self.name = name
        self.description = description
        self.definition = definition

    def get_step_string(self):
        return (
            f"#{self.id} = PRODUCT_DEFINITION_SHAPE("
            f"'{self.name}', "
            f"'{self.description}', "
            f"#{self.definition});\n"
        )

class LengthUnit(StepEntity):

    def __init__(self, prefix="MILLI", unit="METRE"):
        super().__init__("LENGTH_UNIT")
        self.prefix = prefix
        self.unit = unit

    def get_step_string(self):
        return (
            f"#{self.id} = (LENGTH_UNIT() "
            f"NAMED_UNIT(*) "
            f"SI_UNIT(.{self.prefix}.,.{self.unit}.));\n"
        )

class PlaneAngleUnit(StepEntity):

    def __init__(self):
        super().__init__("PLANE_ANGLE_UNIT")

    def get_step_string(self):
        return (
            f"#{self.id} = (NAMED_UNIT(*) "
            f"PLANE_ANGLE_UNIT() "
            f"SI_UNIT($,.RADIAN.));\n"
        )

class SolidAngleUnit(StepEntity):

    def __init__(self):
        super().__init__("SOLID_ANGLE_UNIT")

    def get_step_string(self):
        return (
            f"#{self.id} = (NAMED_UNIT(*) "
            f"SI_UNIT($,.STERADIAN.) "
            f"SOLID_ANGLE_UNIT());\n"
        )


class UncertaintyMeasureWithUnit(StepEntity):

    def __init__(self, value, unit, name, description):
        super().__init__("UNCERTAINTY_MEASURE_WITH_UNIT")
        self.value = value
        self.unit = unit
        self.name = name
        self.description = description

    def get_step_string(self):
        return (
            f"#{self.id} = UNCERTAINTY_MEASURE_WITH_UNIT("
            f"LENGTH_MEASURE({self.value}), "
            f"#{self.unit}, "
            f"'{self.name}', "
            f"'{self.description}');\n"
        )

class GeometricRepresentationContext(StepEntity):

    def __init__(self, uncertainty, units):
        super().__init__("GEOMETRIC_REPRESENTATION_CONTEXT")
        self.uncertainty = uncertainty
        self.units = units

    def get_step_string(self):
        units = ""

        for i, x in enumerate(self.units):
            if i > 0:
                units += ", "

            units += f"#{x}"

        return (
            f"#{self.id} = "
            f"(GEOMETRIC_REPRESENTATION_CONTEXT(3) "
            f"GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{self.uncertainty})) "
            f"GLOBAL_UNIT_ASSIGNED_CONTEXT(({units})) "
            f"REPRESENTATION_CONTEXT('','3D'));\n"
        )

class AdvancedBrepShapeRepresentation(StepEntity):

    def __init__(self, name, items, context):
        super().__init__("ADVANCED_BREP_SHAPE_REPRESENTATION")
        self.name = name
        self.items = items
        self.context = context

    def get_step_string(self):
        items = ""

        for i, x in enumerate(self.items):
            if i > 0:
                items += ", "

            items += f"#{x}"

        return (
            f"#{self.id} = ADVANCED_BREP_SHAPE_REPRESENTATION("
            f"'{self.name}', "
            f"({items}), "
            f"#{self.context});\n"
        )

class ShapeDefinitionRepresentation(StepEntity):

    def __init__(self, definition, representation):
        super().__init__("SHAPE_DEFINITION_REPRESENTATION")
        self.definition = definition
        self.representation = representation

    def get_step_string(self):
        return (
            f"#{self.id} = SHAPE_DEFINITION_REPRESENTATION("
            f"#{self.definition}, "
            f"#{self.representation});\n"
        )