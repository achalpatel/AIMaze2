# --------------------------------------------------------------------------------
# Assignment 2
# Name - Achal Patel | Student Id - 026598245
# Name - Kabir Majmudar | Student Id - 025792284
# 
# --------------------------------------------------------------------------------

import numpy as np
import sys
import math
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
        self.readFile()
        self.createNumberedMatrix()
        self.getStartPos()
        self.getEndPos()
        
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

    # Initializes the Final matrix with zeros 
    def createFinalMat(self):
        self.final_matrix=np.zeros((self.col_size*self.row_size, self.col_size*self.row_size))
        self.addValues()

    # Adds the values in the Final matrix based on the relationship with the adjacent matrix cells
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

    # Creates edges for the graph based on the adjacent cells
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
        
        self.countHeuristicStart()
    
    # Counts the heuristic values of each Vertices in a graph 
    def countHeuristicStart(self):
        visit_set = set()
        queue = []
        goal_vert = self.myGraph.vertex[self.end_pos]
        goal_vert.heuristic = 0
        queue.append(goal_vert)
        visit_set.add(goal_vert.get_id())        
        while queue:
            popped_v = queue.pop(0)            
            for neigh_data in popped_v.get_connections():
                if(neigh_data not in visit_set):
                    neigh_v = self.myGraph.vertex[neigh_data]
                    neigh_v.heuristic = popped_v.heuristic + self.EDGE_WEIGHT
                    queue.append(neigh_v)
                    visit_set.add(neigh_data)



    # BFS search traversal
    def bfsSearch(self):
        visited_dict={}
        queue = []
        queue.append(self.start_pos)
        visited_dict[self.start_pos]=None
        found = False
        max_fringe = -math.inf
        expand_count = 0
        while queue and not found:
            # print("queueu : ",queue)
            pop_value = queue.pop(0)
            if(pop_value == self.end_pos):
                found=True
                break
            expand_count+=1
            for i in range(0, self.final_matrix[pop_value].shape[0]):
                if(self.final_matrix[pop_value][i] == 1 and (i not in visited_dict)):                    
                    queue.append(i)                    
                    visited_dict[i]=pop_value                    
                    # print("i:",i, "dict : ",visited_dict, "que: ",queue)
                    # if(i==self.end_pos):
                    #     found = True
                    #     break
            count_fringe = len(queue)    
            if(count_fringe>=max_fringe):
                max_fringe=count_fringe
        if(not found):
            print("No solution from BFS")
            return None
        path = self.traverseBFS(visited_dict)
        self.bfsFringeSize = max_fringe
        self.bfsExpandCount = expand_count
        return path


    def traverseBFS(self, visited_dict):
        path=[]
        complete=False
        value = visited_dict[self.end_pos]
        path.append(self.end_pos)
        path.append(value)
        while not complete:
            parent = visited_dict[value]
            path.append(parent)
            value=parent
            if(parent == None):
                complete=True
                path.pop()
        return path


    # DFS search traversal
    def searchDFS(self):        
        path=[]        
        visited=set()
        visited.add(self.start_pos)
        for i in range(0, self.final_matrix[self.start_pos].shape[0]):
            if(self.final_matrix[self.start_pos][i] == 1 and i not in visited):               
                visited.add(i)            
                if(self.search_rec(i, visited, path)):
                    path.append(i)
                    path.append(self.start_pos)
                    return path
                    
        return np.array(path)
        
    def search_rec(self, number, visited, path):
        if(number==self.end_pos):
            return True        
        for i in range(0, self.final_matrix[number].shape[0]):
            if(self.final_matrix[number][i] == 1 and (i not in visited)):
                # visited.append(i)                
                visited.add(i)            
                if(self.search_rec(i, visited, path)):
                    path.append(i)                    
                    return True
        return False

    # Dfs search traversal maintaining the fringe 
    def searchDFSusingStack(self):
        path = []
        stack = []
        visited_dict={}    
        stack.append(self.start_pos)
        visited_dict[self.start_pos] = None
        found = False
        expand_count=0
        max_fringe = -math.inf        
        while stack and not found:
            # print("stack :",stack)
            pop_value = stack.pop()            
            if(pop_value == self.end_pos):
                found=True
                break
            expand_count+=1            
            for i in range(0, self.final_matrix[pop_value].shape[0]):
                if(self.final_matrix[pop_value][i] == 1 and (i not in visited_dict)):                    
                    stack.append(i)                    
                    visited_dict[i]=pop_value                    
                    # print("i:",i, "dict : ",visited_dict, "que: ",stack)
            count_fringe = len(stack)    
            if(count_fringe>=max_fringe):
                max_fringe=count_fringe
        if(not found):
            print("No solution from DFS")
            return None
        path = self.traverseBFS(visited_dict)
        self.dfsFringe = max_fringe
        self.dfsExpandCount = expand_count
        return path


    # AStar search
    def astarSearch(self):
        self.createEdges()
        path =[]
        visited_set = set()
        visited_set.add(self.start_pos)
        path.append(self.start_pos)        
        min_value = math.inf
        min_v = None
        current_v=self.myGraph.vertex[self.start_pos]
        max_fringe = 1
        expand_count = 0
        while min_value>=0:        
            expand_count+=1
            fringe_count = len(current_v.get_connections())
            for ver in current_v.get_connections():   
                if(ver in visited_set):
                    continue
                visited_set.add(ver)                           
                v = self.myGraph.vertex[ver]
                if v.heuristic <= min_value:
                    min_v = v
                    min_value = v.heuristic
            # if(fringe_count>=max_fringe):
            #     max_fringe = fringe_count
            path.append(min_v.get_id())
            if(min_value==0):
                break     
            if min_v == current_v:
                print("No solution from ASTAR")
                return None      
            current_v = min_v
        self.astarFringeSize = max_fringe
        self.astarExpandCount = expand_count
        return path

    # This method takes index(i, j) and returns the element at that position from the matrix
    def getElementFromMatrix(self, m, n):
        try:
            return self.matrix[m][n]    
        except IndexError:
            return None

    # Returns the index of the number represented in the numbered matrix
    def getIndexofNumber(self, number):
        try:
            index_i = number//self.col_size
            index_j = number%self.col_size
            return (index_i, index_j)
        except IndexError:
            return None
            
    # Returns the starting position of the maze
    def getStartPos(self):
        for i in range(0,self.row_size):
            for j in range(0, self.col_size):
                if(self.matrix[i][j]==self.char_start):
                    self.start_pos = self.number_matrix[i][j]
                    return self.start_pos

    # Returns the ending position of the maze
    def getEndPos(self):
        for i in range(0,self.row_size):
            for j in range(0, self.col_size):
                if(self.matrix[i][j]==self.char_end):
                    self.end_pos = self.number_matrix[i][j]
                    return self.end_pos    

    # Taking a path list and creating a output array for including a dot representation of the answer
    def printDots(self, path):
        if(path==None):
            return None
        local_output = self.matrix.copy()        
        for values in path:            
            local_i, local_j = self.getIndexofNumber(values)
            local_output[local_i][local_j] = "."
        return np.array(local_output)
    
    # Prints the final matrix
    def printFinalMatrix(self):
        for i in range(0, self.final_matrix.shape[0]):
            print("index = ",i, self.final_matrix[i])
    
    # Displays the graph summary
    def displayGraphSummary(self):
        self.myGraph.graph_summary()    

    # Testing purpose
    # def getOnesPos(self):
    #     l=[]
    #     for i in range(0, self.final_matrix.shape[0]):
    #         for j in range(0, self.final_matrix.shape[1]):
    #             if(self.final_matrix[i][j]==1):
    #                 l.append((i,j))
    #     return np.array(l)
    
    # Testing purpose
    # def readAnswerMatrix(self, file):
    #     f = open(file, 'r')
    #     arr=[]
    #     for line in f:
    #         temp=[]
    #         for i in line:
    #             if(i!="\n" and i!="\t"):
    #                 temp.append(i)
    #             td=list(temp)
    #         arr.append(td)
    #     ans_arr=np.array(arr)
    #     ones_list=[]
    #     for i in range(0,ans_arr.shape[0]):
    #         for j in range(0, ans_arr.shape[1]):
    #             if(ans_arr[i][j]=='1'):
    #                 ones_list.append((i,j))
        
    #     return np.array(ones_list)

    # Calls an Astar search
    def createASTAR(self):
        ASTARpath = self.astarSearch()
        if ASTARpath != None:
            ASTARprinted_out = self.printDots(ASTARpath)
            print(" ASTAR Path : ",ASTARpath)
            print("ASTAR cost : ",len(ASTARpath))
            print("ASTAR Fringe Size",self.astarFringeSize)
            print("ASTAR expand count : ", self.astarExpandCount)
            for line in ASTARprinted_out:
                print(' '.join(map(str, line)))

    # Calls a BFS search
    def createBFS(self):
        self.createFinalMat()
        BFSpath = self.bfsSearch()
        if BFSpath != None:
            BFSprinted_out = self.printDots(BFSpath)
            print("BFSpath :",BFSpath)
            print("BFS cost : ",len(BFSpath))
            print("BFS Fringe size: ",self.bfsFringeSize)
            print("BFS expand count : ",self.bfsExpandCount)
            print("BFS OUTPUT-----------------------------------")
            for line in BFSprinted_out:
                print(' '.join(map(str, line)))
    
    # Calls a DFS search
    def createDFS(self):
        self.createFinalMat()
        DFSpath = self.searchDFSusingStack()
        if DFSpath != None:
            DFSprinted_out = self.printDots(DFSpath)            
            print(" DFS path : ", DFSpath)
            print(" DFS cost : ", len(DFSpath))
            print("DFS Fringe size: ",self.dfsFringe)
            print("DFS expand count : ",self.dfsExpandCount)
            for line in DFSprinted_out:
                print(' '.join(map(str, line)))

    
board = Board("mediumMaze.lay","%"," ", "P", ".")
board.createASTAR()
print("---------------------------------------------")
board.createBFS()
print("---------------------------------------------")
board.createDFS()
print("---------------------------------------------")

