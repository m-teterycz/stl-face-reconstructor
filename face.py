class Face:
    def __init__(self, triangles):
        self.triangles = triangles
        self.vertices = []
        self.get_edges()

    def get_edges(self):
        self.edges = []

        for triangle in self.triangles:
            for edge in triangle.edges:
                if edge not in self.edges:
                    self.edges.append(edge)
                    
        seen = []
        inner_edges = []
        for triangle in self.triangles:
            for i in range(3):
                if triangle.edges[i] in seen:
                    inner_edges.append(triangle.edges[i])
                seen.append(triangle.edges[i])

        for inner_edge in inner_edges:
            self.edges.remove(inner_edge)
