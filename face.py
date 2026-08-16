class Face:
    def __init__(self, triangles):
        self.triangles = triangles
        self.vertices = []
        self.edges = []
        self.boundary_edges = []

    def get_edges(self):
        for triangle in self.triangles:
            for edge in triangle.edges:
                self.edges.append(edge)

    def remove_inner_edge(self): # WIP
        pass
