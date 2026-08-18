class StepWriter: # WIP
    def __init__(self, mesh):
        self.name = "YourName"
        self.application_name = "AppName"
        self.application = "YourApplication"
        self.file_name = "FileName"
        self.file_desc = "Description"
        self.faces = mesh.faces
        self.triangles = mesh.triangles

        self.entity_number_mapper()

        with open("OUTPUT.step", "w") as f:
            self.write_header(f)
        

    def write_header(self, f):
        f.write('ISO-10303-21;\nHEADER;\n\n')
        f.write(f"FILE_DESCRIPTION(('{self.file_desc}'),'2;1');\nFILE_NAME('{self.file_name}','2026-08-16T09:00:00',('{self.name}'),('{self.application}'),'','','');\nFILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));\n\n")
        f.write("ENDSEC;\n\n")
        f.write("DATA;\n\n")
        self.write_cart_points(f)
        """
        Writes basic structure of step file

        HEADER;
        FILE_DESCRIPTION(...);
        FILE_NAME(...);
        FILE_SCHEMA(...);
        ENDSEC;
        """

    def write_cart_points(self, f):
        for point in self.cart_points:
            f.write(f"#{point[0]} = CARTESIAN_POINT('', ({point[1][0]}, {point[1][1]}, {point[1][2]}));\n")
            pass

    def entity_number_mapper(self): # WIP
        self.cart_points = []
        unique_vertices = []
        i = 1
        
        for triangle in self.triangles:
            for edge in triangle.edges:
                for vertex in edge:
                    if vertex not in unique_vertices:
                        unique_vertices.append(vertex)

        for vertex in unique_vertices:
            self.cart_points.append([i, vertex])
            i += 1