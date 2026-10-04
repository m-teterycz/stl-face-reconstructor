import geometry_math

class Face:
    def __init__(self, triangles):
        self.triangles = triangles
        self.normal = triangles[0].normal
        self.vertices = []
        self.get_edges()
        self.order_edges()
        self.get_vertices()

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

        self.edges = tuple(self.edges)

    def get_vertices(self): # Get unique vertices from edges and store them in self.vertices
        for edge in self.edges:
            if edge[0] not in self.vertices:
                self.vertices.append(edge[0])
            if edge[1] not in self.vertices:
                self.vertices.append(edge[1])


    
    def order_edges(self):
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


        v1 = geometry_math.vector(self.ordered_edges[0][0], self.ordered_edges[0][1])
        v2 = geometry_math.vector(self.ordered_edges[1][0], self.ordered_edges[1][1])
        normal = tuple(geometry_math.normalize(geometry_math.cross_product(v1, v2)))
        dot = geometry_math.dot(normal, self.normal)

        if dot < 0:
            self.ordered_edges.reverse()
            for i,edge in enumerate(self.ordered_edges):
                self.ordered_edges[i] = edge[::-1]
                
        self.edges = self.ordered_edges
        
    