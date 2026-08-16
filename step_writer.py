class StepWriter: # WIP
    def __init__(self, triangles, co_planar_groups): # change to faces later they have more info
        self.name = "YourName"
        self.application_name = "AppName"
        self.application = "YourApplication"
        self.file_name = "FileName"
        self.file_desc = "Description"

        self.triangles = triangles
        self.co_planar_groups = co_planar_groups

        with open("OUTPUT.step", "w") as f:
            self.write_header(f)
        

    def write_header(self, f):
        f.write('ISO-10303-21;\nHEADER;\n\n')
        f.write(f"FILE_DESCRIPTION(('{self.file_desc}'),'2;1');\nFILE_NAME('{self.file_name}','2026-08-16T09:00:00',('{self.name}'),('{self.application}'),'','','');\nFILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));\n\n")
        f.write("ENDSEC;\n\n")
        f.write("DATA;\n\n")
        """
        Writes basic structure of step file with some empty lines inbetween:

        HEADER;
        FILE_DESCRIPTION(...);
        FILE_NAME(...);
        FILE_SCHEMA(...);
        ENDSEC;
        """

    def entity_number_mapper(self): # WIP
        eNumtoVertex = {}

        for face in self.co_planar_groups:
            for triangle in face:
                pass