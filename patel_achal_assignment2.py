# Assignment 1
# Name - Achal Patel
# Student Id - 026598245

import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from Vertex import Vertex
from Graph import Graph

class Board:
    # Constructor initialized with the input file, Obstacle character, 
    # free space character, Begin position character and the End position
    # character
    EDGE_WEIGHT=1
    def __init__(self, file, char_obs, char_free, char_start, char_end):
        super().__init__()
        self.file=file
        self.char_obstacle=char_obs
        self.char_free=char_free
        self.char_start=char_start
        self.char_end=char_end
        self.myGraph = Graph()
        

    # Reads the input file and creates a matrix of characters named as matrix .
    def readFile(self):
        temp_arr=[]
        f = open(self.file, "r")
        for line in f:
            temp = []
            for i in line:
                if(i!="\n"):
                    temp.append(i)    
            temp_arr.append(temp)

        self.matrix = np.array(temp_arr)
        
    

    # This method creates the numbered represantation of the character matrix named as number_matrix
    # Numbers start from 0
    def createNumberedMatrix(self):
        self.row_size=self.matrix.shape[0]
        self.col_size=self.matrix.shape[1]
        low_x=0
        t=[]
        for i in range(0, self.row_size):
            high_x=low_x+self.col_size
            temp=list(range(low_x,high_x))
            t.append(temp)
            low_x=high_x

        self.number_matrix=np.array(t)

    def createEdges(self):
        for i in range(0, self.row_size):
            for j in range(0, self.col_size):
                num = self.number_matrix[i][j]
                char = self.matrix[i][j]
                if(char!=self.char_obstacle):
                    if(i-1>=0 and self.matrix[i-1][j]!=self.char_obstacle):
                        self.myGraph.add_edge(num, self.number_matrix[i-1][j], self.EDGE_WEIGHT)
                    if(i+1<=self.row_size-1 and self.matrix[i+1][j]!=self.char_obstacle):                                              
                       self.myGraph.add_edge(num, self.number_matrix[i+1][j], self.EDGE_WEIGHT)
                    if(j-1>=0 and self.matrix[i][j-1]!=self.char_obstacle):                                              
                       self.myGraph.add_edge(num, self.number_matrix[i][j-1], self.EDGE_WEIGHT)
                    if(j+1<=self.col_size-1 and self.matrix[i][j+1]!=self.char_obstacle):                                              
                       self.myGraph.add_edge(num, self.number_matrix[i][j+1], self.EDGE_WEIGHT)
        
    def displayGraphSummary(self):
        self.myGraph.graph_summary()
    
    # This method takes index(i, j) and returns the element at that position from the matrix
    def getElementFromMatrix(self, m, n):
        try:
            return self.matrix[m][n]    
        except IndexError:
            return None

    def getIndexofNumber(self, number):
        try:
            index_i = number//self.col_size
            index_j = number%self.col_size
            return (index_i, index_j)
        except IndexError:
            return None
        
    
    def initFinalMat(self):
        self.final_matrix=np.zeros((self.col_size*self.row_size, self.col_size*self.row_size))

    def addValues(self):
        for i in range(0, self.row_size):
            for j in range(0, self.col_size):
                num = self.number_matrix[i][j]
                char = self.matrix[i][j]
                if(char!=self.char_obstacle):
                    if(i-1>=0 and self.matrix[i-1][j]!=self.char_obstacle):                       
                       self.final_matrix[num][self.number_matrix[i-1][j]] = 1
                    if(i+1<=self.row_size-1 and self.matrix[i+1][j]!=self.char_obstacle):                       
                       self.final_matrix[num][self.number_matrix[i+1][j]] = 1
                    if(j-1>=0 and self.matrix[i][j-1]!=self.char_obstacle):                       
                       self.final_matrix[num][self.number_matrix[i][j-1]] = 1
                    if(j+1<=self.col_size-1 and self.matrix[i][j+1]!=self.char_obstacle):                       
                       self.final_matrix[num][self.number_matrix[i][j+1]] = 1

    def printFinalMatrix(self):
        for i in range(0, self.final_matrix.shape[0]):
            print("index = ",i, self.final_matrix[i])
    

    def getStartPos(self):
        for i in range(0,self.row_size):
            for j in range(0, self.col_size):
                if(self.matrix[i][j]==self.char_start):
                    return self.number_matrix[i][j]

    def getEndPos(self):
        for i in range(0,self.row_size):
            for j in range(0, self.col_size):
                if(self.matrix[i][j]==self.char_end):
                    return self.number_matrix[i][j]

    def searchDFS(self, startPos, endPos):        
        path=[]
        # visited.append(startPos)
        visited=set()
        visited.add(startPos)
        for i in range(0, self.final_matrix[startPos].shape[0]):
            if(self.final_matrix[startPos][i] == 1 and i not in visited):
                # visited.append(i)                            
                visited.add(i)            
                if(self.search_rec(i, visited, path, endPos)):
                    path.append(i)
                    path.append(startPos)
                    return path
                    
        return np.array(path)
        

    def search_rec(self, number, visited, path, endPos):
        if(number==endPos):
            return True        
        for i in range(0, self.final_matrix[number].shape[0]):
            if(self.final_matrix[number][i] == 1 and (i not in visited)):
                # visited.append(i)                
                visited.add(i)            
                if(self.search_rec(i, visited, path, endPos)):
                    path.append(i)                    
                    return True
        return False

    
    # BFS search traversal
    def bfsSearch(self, startPos, endPos):
        # visited dictionary storing value of Parent
        visited_dict={}
        queue = []
        queue.append(startPos)
        visited_dict[startPos]=None
        found = False
        while queue and not found:
            pop_value = queue.pop()
            # print("queueu : ",queue)
            for i in range(0, self.final_matrix[pop_value].shape[0]):
                if(self.final_matrix[pop_value][i] == 1 and (i not in visited_dict)):                    
                    queue.append(i)
                    visited_dict[i]=pop_value                    
                    # print("i:",i, "dict : ",visited_dict, queue)
                    if(i==endPos):
                        found = True
                        break
        if(not found):
            print("No solution")
            return None
        return visited_dict

    def traverseBFS(self, visited_dict, endPos):
        path=[]
        complete=False
        value = visited_dict[endPos]
        path.append(endPos)
        path.append(value)
        while not complete:
            parent = visited_dict[value]
            path.append(parent)
            value=parent
            if(parent == None):
                complete=True
                path.pop()
        return path


    def printDots(self, path):
        local_output = self.matrix
        for values in path:            
            local_i, local_j = self.getIndexofNumber(values)
            local_output[local_i][local_j] = "."
        return np.array(local_output)

    # Testing purpose
    def getOnesPos(self):
        l=[]
        for i in range(0, self.final_matrix.shape[0]):
            for j in range(0, self.final_matrix.shape[1]):
                if(self.final_matrix[i][j]==1):
                    l.append((i,j))
        return np.array(l)
    
    # Testing purpose
    def readAnswerMatrix(self, file):
        f = open(file, 'r')
        arr=[]
        for line in f:
            temp=[]
            for i in line:
                if(i!="\n" and i!="\t"):
                    temp.append(i)
                td=list(temp)
            arr.append(td)
        ans_arr=np.array(arr)
        ones_list=[]
        for i in range(0,ans_arr.shape[0]):
            for j in range(0, ans_arr.shape[1]):
                if(ans_arr[i][j]=='1'):
                    ones_list.append((i,j))
        
        return np.array(ones_list)


b = Board("custom.lay","%"," ", "P", ".")
b.readFile()
b.createNumberedMatrix()
start_ind = b.getStartPos()
end_ind = b.getEndPos()
print(start_ind, end_ind)
b.createEdges()
b.displayGraphSummary()


