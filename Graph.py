# Name - Achal Patel
# Student ID - 026598245
from Vertex import Vertex

class Graph():
    def __init__(self):
        super().__init__()
        self.vertex = {}

    def create_vertex(self, data):
        v = Vertex(data)
        self.add_vertex(v)
        return v

    def add_vertex(self, vertex):
        self.vertex[vertex.get_id()] = vertex

    def get_vertex(self, vertex):
        return self.vertex[vertex]

    def get_vertices(self):
        return self.vertex

    def add_edge(self, data_from, data_to, weight):
        if(data_from not in self.vertex.keys()):
            vertex_from = self.create_vertex(data_from)
        else:
            vertex_from = self.vertex[data_from]
        if(data_to not in self.vertex.keys()):
            vertex_to = self.create_vertex(data_to)
        else:
            vertex_to = self.vertex[data_to]
        # print("--",vertex_from.get_id(), data_to)    
        vertex_from.add_neighboor(vertex_to,weight)
        

    def graph_summary(self):
        print("Graph Summary :")
        
        for ver in self.get_vertices():
            print("For vertex ",ver, "->", self.vertex[ver].get_connections())



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


