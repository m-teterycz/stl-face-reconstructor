class Mesh:
    def __init__(self, triangles):
        self.triangles = triangles
        self.faces = []
        self.vertices = self.get_vertices()

    def find_neighbours(self):
        vertex_to_triangles = {}
        for triangle in self.triangles:
            for edge in triangle.edges:
                vertex_to_triangles.setdefault(frozenset(edge), []).append(triangle) # frozen set used so that (a,b) == (b,a) is true

        for value in vertex_to_triangles.values():
            if len(value) == 2:
                for i in range(0,2):
                    for j in range(i + 1,2):
                        value[i].neighbours.append(value[j])
                        value[j].neighbours.append(value[i])
            else:
                raise Exception("Non-manifold edge detected / STL input is invalid. ")


    def find_all_planar_regions(self):
        visited = set()
        regions = []

        for triangle in self.triangles:
            if triangle not in visited:
                region = self.dfs(triangle)
                regions.append(region)
                for triangle1 in region:
                    visited.add(triangle1)

        return regions
    
    def dfs(self, triangle):
        normal = triangle.normal
        visited = set()
        planarfaces = []
        stack = [triangle]

        while len(stack) != 0:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)
            planarfaces.append(current)

            for neighbour in current.neighbours:
                if neighbour not in visited and neighbour.normal == normal:
                    stack.append(neighbour)

        return planarfaces

    def get_vertices(self):
        vertices = []
        seen = set()
        for triangle in self.triangles:
            for vertex in triangle.vertices:
                if vertex not in seen:
                    vertices.append(vertex)
                    seen.add(vertex)
        return tuple(vertices)