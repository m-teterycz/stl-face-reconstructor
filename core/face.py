from core import geometry_math

class Face:
    def __init__(self, triangles):
        self.triangles = triangles
        self.normal = triangles[0].normal
        self.vertices = []
        self.loops = []
        self.get_edges()
        self.get_vertices()
        self.order_edges()
        self.plane_mapping()
        self.outer_loop = self.get_outer_loop()

    def get_edges(self): # Get outer edges from triangles and store them in self.edges
        self.edges = set()

        for triangle in self.triangles:
            for edge in triangle.edges:
                if frozenset(edge) not in self.edges:
                    self.edges.add(edge)
                    
        seen = set()
        inner_edges = []
        for triangle in self.triangles:
            for i in range(3):
                if frozenset(triangle.edges[i]) in seen:
                    inner_edges.append(triangle.edges[i])
                seen.add(frozenset(triangle.edges[i]))


        for inner_edge in inner_edges:
            self.edges.remove(inner_edge)

        self.edges = tuple(self.edges)

    def get_vertices(self): # Get unique vertices from edges and store them in self.vertices
        for edge in self.edges:
            if edge[0] not in self.vertices:
                self.vertices.append(edge[0])
            if edge[1] not in self.vertices:
                self.vertices.append(edge[1])

    def get_unused_edges(self, seen):
        unused = []
        for edge in self.edges:
            if edge in seen or edge[::-1] in seen:
                pass
            else:
                unused.append(edge)

        return unused

    def order_edges(self): # Seperates different co-planar groups into outer and inner loops
        self.original_length = len(self.edges)
        self.used_edges = []
        while self.get_unused_edges(self.used_edges):
            edge = self.get_unused_edges(self.used_edges)[0]
            self.current_edge = edge
            self.used_edges.append(edge)
            self.ordered_edges = [self.current_edge]
            start = edge
            while start[0] != self.current_edge[1]:
                found = False
                for edge in self.edges:
                    if self.current_edge[1] == edge[0] and (edge not in self.used_edges and edge[::-1] not in self.used_edges): # points match so they must form a loop when joined
                        self.ordered_edges.append(edge)
                        self.current_edge = edge
                        self.used_edges.append(self.current_edge)
                        found = True
                        break
                    elif self.current_edge[1] == edge[1] and (edge not in self.used_edges and edge[::-1] not in self.used_edges):
                        self.ordered_edges.append(edge[::-1])
                        self.current_edge = edge[::-1]
                        self.used_edges.append(self.current_edge)
                        found = True
                        break

                if not found:
                    raise ValueError(f"Could not find next edge after {self.current_edge}")

            self.loops.append(self.ordered_edges)


        v1 = geometry_math.vector(self.ordered_edges[0][0], self.ordered_edges[0][1])
        v2 = geometry_math.vector(self.ordered_edges[1][0], self.ordered_edges[1][1])
        normal = tuple(geometry_math.normalize(geometry_math.cross_product(v1, v2)))
        dot = geometry_math.dot(normal, self.normal)

        if dot < 0: # Check ordering later determines .T. or .F. in STEP file.
            self.ordered_edges.reverse()
            for i,edge in enumerate(self.ordered_edges):
                self.ordered_edges[i] = edge[::-1]
                
        self.edges = self.ordered_edges
        
    def plane_mapping(self):
        self.loops_2d = []
        if len(self.loops) == 1:
            return None
        
        origin = self.vertices[0]
        i = 2

        while True:
            u = geometry_math.normalize(geometry_math.vector(origin, self.vertices[1]))
            v = geometry_math.vector(origin, self.vertices[i])
            v = geometry_math.vector_subtraction(v, geometry_math.vector_scalar(u, geometry_math.dot(u,v))) # make it perpendicular to u
            v = geometry_math.normalize(v)

            if geometry_math.dot(v, v) > 0:
                break
            i += 1

        for loop in self.loops:
            edges = [] 

            for edge in loop:
                vertex_pair = []
                for vertex in edge:
                    r = geometry_math.vector_subtraction(vertex, origin)
                    new_x = geometry_math.dot(r, u)
                    new_y = geometry_math.dot(r, v)
                    vertex_pair.append([new_x, new_y])
                edges.append(vertex_pair)
            self.loops_2d.append(edges)


    def point_in_loop(self, point, loop):
        crossings = 0
        for i in range(len(loop)): # Iterate through all the edges of the other loop
            p1, p2 = loop[i]
            if (p1[1] <= point[1] and  p2[1] > point[1]) or (p2[1] <= point[1] and  p1[1] > point[1]):
                x_intersection = p1[0] + (point[1] - p1[1])*((p2[0] - p1[0])/(p2[1] - p1[1]))
                if x_intersection > point[0]:
                    crossings += 1

        return crossings % 2 == 1 # Returns True if when point is inside of the loop

    def get_outer_loop(self): # Currently assumes that there is only one outer boundary assuming there are no disconnected boundaries.
        if len(self.loops) == 1:
            return 0
        loop_classes = set()
        for i in range(len(self.loops_2d)):
            for j in range(i + 1, len(self.loops_2d)):
                i_inside_j = self.point_in_loop(self.loops_2d[i][0][0], self.loops_2d[j])
                j_inside_i = self.point_in_loop(self.loops_2d[j][0][0], self.loops_2d[i])

                if i_inside_j and not j_inside_i:
                    loop_classes.add(i)
                elif j_inside_i and not i_inside_j:
                    loop_classes.add(j)

        return set(range(0,len(self.loops_2d))).difference(loop_classes).pop() # Currently assumes there is only one outer loop. Returns index