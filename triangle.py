import math, geometry_math

class Triangle:
    def __init__(self, vertices):
        self.normal = None
        self.vertices = vertices
        self.neighbours = []
        self.edges = []

        temp_vert = []
            
        for vertex in self.vertices:
            temp_vert.append([float(vertex[0]), float(vertex[1]), float(vertex[2])])

        self.vertices = tuple(temp_vert)

        self.edge1 = geometry_math.vector(self.vertices[0], self.vertices[1])
        self.edge2 = geometry_math.vector(self.vertices[0], self.vertices[2])
        self.normal = geometry_math.normalize(geometry_math.cross_product(self.edge1, self.edge2))
        self.small_large_vertex()

        self.get_edges()

    def get_edges(self):
        for i in range(3):
            for j in range(i + 1, 3):
                if self.vertices[i] < self.vertices[j]:
                    self.edges.append([self.vertices[i],self.vertices[j]])
                else:
                    self.edges.append([self.vertices[j],self.vertices[i]])

    def small_large_vertex(self): # Orders all vertices to allow for easy duplicate edge detection later in faces.py
            if self.vertices[0] < self.vertices[1]:
                self.edge1 = geometry_math.vector(self.vertices[0], self.vertices[1])
            else:
                self.edge1 = geometry_math.vector(self.vertices[1], self.vertices[0])
            
            if self.vertices[0] < self.vertices[2]:
                self.edge2 = geometry_math.vector(self.vertices[0], self.vertices[2])
            else:
                self.edge2 = geometry_math.vector(self.vertices[2], self.vertices[0])


def create_triangles(data):
    triangles = []
    
    for i in range(0, len(data), 3):
        triangle = Triangle(data[i:i + 3])
        triangles.append(triangle)

    return triangles

    
