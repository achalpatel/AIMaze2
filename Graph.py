# Name - Achal Patel
# Student ID - 026598245
from Vertex import Vertex

class Graph():
    def __init__(self):
        super().__init__()
        self.vertex = {}

    def add_vertex(self, vertex):
        self.vertex[vertex] = vertex

    def get_vertex(self, vertex):
        return self.vertex[vertex]

    def get_vertices(self):
        return self.vertex

    def add_edge(self, vertex_from, vertex_to, weight):
        if(self.vertex[vertex_from]==None):
            self.add_vertex(vertex_from)
        if(self.vertex[vertex_to]==None):
            self.add_vertex(vertex_to)
        vertex_from.add_neighboor(vertex_to,weight)

    def graph_summary(self):
        print("Graph Summary :")
        for ver in self.get_vertices():
            print("For vertex ",ver.get_id()," -> ",ver.get_connections())



# A = Vertex('A')
# B = Vertex('B')
# C = Vertex('C')
# D = Vertex('D')
# S = Vertex('S')
# g = Graph()
# g.add_vertex(A)
# g.add_vertex(B)
# g.add_vertex(C)
# g.add_vertex(D)
# g.add_vertex(S)

# g.add_edge(A,B,1)
# g.add_edge(A,C,2)
# g.add_edge(B,D,4)
# g.add_edge(C,A,3)
# g.add_edge(C,B,9)
# g.add_edge(C,D,2)
# g.add_edge(D,B,6)
# g.add_edge(D,S,7)
# g.add_edge(S,C,5)
# g.add_edge(S,A,10)


# print("get_Vertices():")
# for items in g.get_vertices():
#     print(items.get_id(), end=" ")
# print("")
# g.graph_summary()


