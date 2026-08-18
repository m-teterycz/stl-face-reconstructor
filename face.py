class Face:
    def __init__(self, triangles):
        self.triangles = triangles
        self.vertices = []
        self.get_edges()
        self.get_vertices()
        self.normal = triangles[0].normal

    def get_edges(self): # Get outer edges from triangles and store them in self.edges
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

    def get_vertices(self): # Get unique vertices from edges and store them in self.vertices
        for edge in self.edges:
            if edge[0] not in self.vertices:
                self.vertices.append(edge[0])
            if edge[1] not in self.vertices:
                self.vertices.append(edge[1])