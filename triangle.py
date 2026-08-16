import math

class Triangle:
    def __init__(self, vertices):
        self.normal = None
        self.vertices = vertices
        self.neighbours = []
        self.edges = []

        temp_vert = []
            
        for vertex in self.vertices:
            temp_vert.append([float(vertex[0]), float(vertex[1]), float(vertex[2])])

        self.vertices = temp_vert

        self.edge1 = self.vector(self.vertices[0], self.vertices[1])
        self.edge2 = self.vector(self.vertices[0], self.vertices[2])
        self.normal = self.normalize(self.cross_product(self.edge1, self.edge2))

        self.get_edges()

    def vector(self, v1, v2):
        return [
            v2[0] - v1[0],
            v2[1] - v1[1],
            v2[2] - v1[2]
        ]

    def cross_product(self, a, b):
        return [
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]
        ]

    def normalize(self, vector):
        x = vector[0]
        y = vector[1]
        z = vector[2]

        length = math.sqrt(x*x + y*y + z*z)

        if length == 0:
            return [0, 0, 0]

        x = x / length
        y = y / length
        z = z / length

        return [x, y, z]


    def get_edges(self):
        for i in range(3):
            for j in range(i + 1, 3):
                if self.vertices[i] < self.vertices[j]:
                    self.edges.append([self.vertices[i],self.vertices[j]])
                else:
                    self.edges.append([self.vertices[j],self.vertices[i]])

def create_triangles(data):
    triangles = []
    
    for i in range(0, len(data), 3):
        triangle = Triangle(data[i:i + 3])
        triangles.append(triangle)

    return triangles
