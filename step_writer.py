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

        self.cartesian_registry = {}  # Use these to map a feature e.g coord into its id. 
        self.vertex_registry = {}     
        self.edge_registry = {}
        self.direction_registry = {}
        self.line_registry = {}
        self.vector_registry = {}      
        self.edgecurve_registry = {}
        self.orientededge_registry = {}
        self.edgeloop_registry = {}    

        

    def write_data(self, f):
        f.write('ISO-10303-21;\nHEADER;\n\n')
        f.write(f"FILE_DESCRIPTION(('{self.file_desc}'),'2;1');\nFILE_NAME('{self.file_name}','2026-08-16T09:00:00',('{self.name}'),('{self.application}'),'','','');\nFILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));\n\n")
        f.write("ENDSEC;\n\n")
        f.write("DATA;\n\n")

        for entity in self.registry:
            f.write(entity.get_step_string())
        """
        Writes basic structure of step file

        HEADER;
        FILE_DESCRIPTION(...);
        FILE_NAME(...);
        FILE_SCHEMA(...);
        ENDSEC;
        """

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
        super().__init__("Direction")
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
    def __init__(self, curve):
            super().__init__("ORIENTED_EDGE")
            self.curve = curve
    
    def get_step_string(self):
        return f"#{self.id} = ORIENTED_EDGE('', *, *, #{self.curve}, .T.);\n"

class EdgeLoop(StepEntity):
    def __init__(self, loop):
            super().__init__("EDGE_LOOP")
            self.loop = loop
            for i in range(len(self.loop)):
                 text = f"#{self.loop[i]}"
                 self.loop[i] = text
            self.loop = ", ".join(self.loop)

    def get_step_string(self):
        print(self.loop)
        return f"#{self.id} = EDGE_LOOP('', ({self.loop}));\n"