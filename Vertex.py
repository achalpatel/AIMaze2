# Name - Achal Patel
# Student ID - 026598245

class Vertex:
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.neighbor = {}
    
    def get_id(self):
        return self.data

    def get_weight(self,neighbor):
        return self.neighbor[neighbor]

    def get_connections(self):
        return self.neighbor
    
    def add_neighboor(self, neighbor, weight):
        self.neighbor[neighbor.get_id()] = weight
