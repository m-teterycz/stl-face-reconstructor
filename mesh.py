class Mesh:
    def __init__(self, triangles):
        self.triangles = triangles
        self.faces = []
    
    def find_neighbours(self):
        for i in range(len(self.triangles)):
            for j in range(i + 1, len(self.triangles)):
                if self.check_connected(self.triangles[i], self.triangles[j]):
                    self.triangles[i].neighbours.append(self.triangles[j])
                    self.triangles[j].neighbours.append(self.triangles[i])

            
    def check_connected(self, triangle1, triangle2):
        connected_vertices = 0
        for vertex in triangle1.vertices:
            for j in range(3):
                if vertex == triangle2.vertices[j]:
                    connected_vertices += 1
        if connected_vertices == 2:
            return True
        return False

    def find_all_planar_regions(self):
        visited = []
        regions = []

        for triangle in self.triangles:
            if triangle not in visited:
                region = self.dfs(triangle)
                regions.append(region)
                visited.extend(region)

        return regions
    
    def dfs(self, triangle):
        normal = triangle.normal
        visited = []
        planarfaces = []
        stack = [triangle]

        while len(stack) != 0:
            current = stack.pop()

            if current in visited:
                continue

            visited.append(current)
            planarfaces.append(current)

            for neighbour in current.neighbours:
                if neighbour not in visited and neighbour.normal == normal:
                    stack.append(neighbour)

        return planarfaces