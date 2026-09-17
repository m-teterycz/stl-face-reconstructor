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
            super().__init__("Line")
            self.coordinates = coords
            self.direction = direction
    
    def get_step_string(self):
        return f"#{self.id} = Line('', {self.coordinates}, {self.direction});\n"