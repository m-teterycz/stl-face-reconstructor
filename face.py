class Face:
    def __init__(self, triangles):
        self.triangles = triangles
        self.vertices = []
        self.get_edges()
        self.order_edges()
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


    
    def order_edges(self): # WIP Needed so that in the STEP writer a closed loop can be created
        self.original_length = len(self.edges)
        self.current_edge = self.edges[0]
        self.ordered_edges = [self.edges[0]]
        self.used_edges = [self.current_edge]

        while len(self.ordered_edges) != self.original_length:
            for edge in self.edges:
                if self.current_edge[1] == edge[0] and (edge not in self.used_edges and edge[::-1] not in self.used_edges): # points match so they must form a loop when joined
                    self.ordered_edges.append(edge)
                    self.current_edge = edge
                    self.used_edges.append(self.current_edge)
                    break
                elif self.current_edge[1] == edge[1] and (edge not in self.used_edges and edge[::-1] not in self.used_edges):
                    self.ordered_edges.append(edge[::-1])
                    self.current_edge = edge[::-1]
                    self.used_edges.append(self.current_edge)
                    break

        self.edges = self.ordered_edges        
    