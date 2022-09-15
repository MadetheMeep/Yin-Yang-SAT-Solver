import pycosat
from copy import copy, deepcopy
import time

m = 0
n = 0
A = []
C = []
cnf_temp = []


def mapping(r, c):
    return n * (r - 1) + c;

def get_1_solution():
    cnf = []
    clause = []
    if (m == 1):
        for c in range(1,n+1):
            clause.append(-mapping(m,c))
    elif (n == 1):
        for r in range(1,m+1):
            clause.append(-mapping(r,n))
    cnf.append(clause)
    return cnf
   
def rule_2by2():
    cnf = []
    for r in range(1, m):
        for c in range(1, n):
            clause = []
            clause.append(-mapping(r,c))
            clause.append(-mapping(r+1,c))
            clause.append(-mapping(r,c+1))
            clause.append(-mapping(r+1,c+1))
            cnf.append(clause)
            clause = []
            clause.append(mapping(r,c))
            clause.append(mapping(r+1,c))
            clause.append(mapping(r,c+1))
            clause.append(mapping(r+1,c+1))
            cnf.append(clause)
    return cnf

def rule_alternating():
    cnf = []
    for r in range(1, m):
        for c in range(1, n):
            clause = []
            clause.append(-mapping(r,c))
            clause.append(mapping(r+1,c))
            clause.append(mapping(r,c+1))
            clause.append(-mapping(r+1,c+1))
            cnf.append(clause)
            clause = []
            clause.append(mapping(r,c))
            clause.append(-mapping(r+1,c))
            clause.append(-mapping(r,c+1))
            clause.append(mapping(r+1,c+1))
            cnf.append(clause)
    return cnf

def add_hints(A): 
    cnf = []
    for r in range(m):
        for c in range(n):
            if(A[r][c] != '*'):
                cnf.append([mapping(r+1,c+1) * ((A[r][c] * 2) - 1)]) #Map Positive for 1, Map Negative for 0
    return cnf
    
def translate_to_array(cnf):
    config = deepcopy(cnf)
    A = []
    for r in range(m):
        row_list = []
        for c in range(n):
            if (config.pop(0) > 0): #Positive Value
                row_list.append(1)
            else:                   #Negative Value
                row_list.append(0)
        A.append(row_list)
    return A

def valid_cell(r,c):
    return ((r >= 0) and (r < m) and (c >=0) and (c < n))
 
def check_connectivity_BFS(A, r, c, color):
    #Initialize 2 dimentional array of 0 for checklist
    checklist = [[0]*n for _ in range(m)]
    checklist[r][c] = 1
    #Initialize queue for breath first search
    queue = []
    queue.append([r,c])
    #Initialize Direction
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]
    #initialize count
    count = 1
    #run until the stack is empty
    while queue:
        #pop queue
        row, col = queue.pop(0)
        for i in range(4):
            adj_row = row + dr[i]
            adj_col = col + dc[i]
            if (valid_cell(adj_row, adj_col)) and (checklist[adj_row][adj_col] == 0):
                checklist[adj_row][adj_col] = 1
                if (A[adj_row][adj_col] == color):
                    queue.append([adj_row,adj_col])
                    count += 1
    #return count of all connected cells from the starting cell
    return count
    
def check_connectivity_DFS(A, r, c, color):
    #Initialize 2 dimentional array of 0 for checklist
    checklist = [[0]*n for _ in range(m)]
    checklist[r][c] = 1
    #Initialize queue for breath first search
    stack = []
    stack.append([r,c])
    #Initialize Direction
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]
    #initialize count
    count = 1
    #run until the stack is empty
    while stack:
        #pop stack
        row, col = stack.pop()
        for i in range(4):
            adj_row = row + dr[i]
            adj_col = col + dc[i]
            if (valid_cell(adj_row, adj_col)) and (checklist[adj_row][adj_col] == 0):
                checklist[adj_row][adj_col] = 1
                if (A[adj_row][adj_col] == color):
                    stack.append([adj_row,adj_col])
                    count += 1
    #return count of all connected cells from the starting cell
    return count
    
def show_config(A):
    print("")
    for x in A:
        print(*x, sep=" ")
        
def find_first(A, color): #Finds the first cell containing color, if none found it returns empty array
    for i in range(m):
        for j in range(n):
            if(A[i][j]==color):
                return [i, j]
    return []
    
def verify(A):
    b_count = sum(row.count(0) for row in A) #count black (0)
    w_count = sum(row.count(1) for row in A) #count white (1)
    b_start = find_first(A, 0)
    w_start = find_first(A, 1)
    if b_start: #checks if b_start is an empty array or not
        b_valid = check_connectivity_DFS(A, b_start[0], b_start[1], 0)
    else:
        b_valid = 0
    if w_start: #checks if w_start is an empty array or not
        w_valid = check_connectivity_DFS(A, w_start[0], w_start[1], 1)
    else:
        w_valid = 0
    if (b_valid == b_count) and (w_valid == w_count):
        return True
    else:
        return False

def find_solution(cnf):
    total_iter = 0
    while True:
        solution = pycosat.solve(cnf)
        total_iter += 1
        if isinstance(solution, list):
            arr = translate_to_array(solution)
            check = verify(arr)
            print(check)
            if (check):
                print(total_iter)
                return arr
            else:
                neg_sol = [-x for x in solution]
                cnf.extend([neg_sol]) #Negate Solution
        else:
            return []
            
def find_total(cnf,default_count):
    count = default_count
    while True:
        solution = pycosat.solve(cnf)
        if isinstance(solution, list):
            arr = translate_to_array(solution)
            check = verify(arr)
            if (check):
                count += 1
            neg_sol = [-x for x in solution]
            cnf.extend([neg_sol]) #Negate Solution
        else:
            return count
    

m, n = map(int,input().split())
if ((m == 1) or (n == 1)):
    cnf_temp.extend(get_1_solution())
    default_count = 1
else:
    cnf_temp.extend(rule_2by2()) #adding 2by2 rule to CNF
    cnf_temp.extend(rule_alternating()) #adding 2by2 alternating rule to CNF
    default_count = 0

for i in range(3):
    cnf = deepcopy(cnf_temp)
    start = time.perf_counter()
    count = find_total(cnf,default_count)
    end = time.perf_counter()
    duration = end - start
    print("result = ",count,", duration = ",duration)