import pycosat
from copy import copy, deepcopy
import time
import os

m = 11
n = 9
A = []
C = []
rules = []

#Rotation and Reflection

def identical(A, B):
    #checking whether A and B are identical matrices
    row_A = len(A)
    col_A = len(A[0])
    row_B = len(B)
    col_B = len(B[0])
    if((row_A != row_B) or (col_A != col_B)): return False
    else:
        for i in range(row_A):
            for j in range(col_A):
                if(A[i][j] != B[i][j]): return False
    return True
    
def transpose(A):
    #transposing a matrix A, i.e., Atrans[i][j] = A[j][i]
    row_A = len(A)
    col_A = len(A[0])
    row_A_trans = col_A
    col_A_trans = row_A
    A_trans = [[0]*col_A_trans for i in range(row_A_trans)]
    for i in range(row_A_trans):
        for j in range(col_A_trans):
            A_trans[i][j] = A[j][i]
    return deepcopy(A_trans)
    
def reverse_row(A):
    #reversing every row of A
	#Arevrow[i][j] = A[i][n-1-j], where n is the number of column of A
    row_A = len(A)
    col_A = len(A[0])
    A_rev_row = deepcopy(A)
    for i in range(row_A):
        A_rev_row[i].reverse()
    return deepcopy(A_rev_row)

def reverse_col(A):
    #reversing every column A
	#Arevcol[i][j] = A[m-1-i][j], where m is the number of row of A
    row_A = len(A)
    col_A = len(A[0])
    A_rev_col = [[0]*col_A for i in range(row_A)]
    for i in range(row_A):
        for j in range(col_A):
            A_rev_col[i][j] = A[row_A-1-i][j]
    return deepcopy(A_rev_col)
    
def CW_rotate(A):
    #rotating a matrix A 90 degree in clockwise direction
	#transpose the matrix and reverse each row
    A_CW = reverse_row(transpose(A))
    return deepcopy(A_CW)
    
def CCW_rotate(A):
    #rotating a matrix A 90 degree in counter-clockwise direction
	#reverse each row and transpose the matrix
    A_CCW = transpose(reverse_row(A))
    return deepcopy(A_CCW)
    
def one_eighty(A):
    #rotating a matrix A 180 degree in clockwise (or counter-clockwise) direction
	#we can compose CWrotate or CCWrotate twice
    A_one_eighty = CW_rotate(CW_rotate(A))
    return deepcopy(A_one_eighty)
    
def CW_rotate_horizontal_ref(A):
    #rotating a matrix A 90 degree in clockwise direction and reflecting the result horizontally
    A_CW = CW_rotate(A)
    A_CW_hor = reverse_col(A_CW)
    return deepcopy(A_CW_hor)
    
def horizontal_ref_CW_rotate(A):
    #reflecting a matrix A horizontally and then rotating the result 90 degree in clockwise direction
    A_hor = reverse_col(A)
    A_hor_CW = CW_rotate(A_hor)
    return deepcopy(A_hor_CW)

#CNF

def mapping(r, c):
    return n * (r - 1) + c;
    
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

def translate_to_clause(A):
    clause = []
    for r in range(m):
        for c in range(n):
            clause.append(mapping(r+1,c+1) * ((A[r][c] * 2) - 1))
    return clause
    
def negate_clause(clause):
    return [-x for x in clause]

#Verifier

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

#SAT Solver

def check_duplicate_clause(neg_clauses,clause):
    for x in neg_clauses:
        if (x == clause): return neg_clauses
    neg_clauses.append(clause)
    return neg_clauses

def find_solution(cnf):
    total_iter = 0
    while True:
        solution = pycosat.solve(cnf)
        total_iter += 1
        if isinstance(solution, list):
            A = translate_to_array(solution)
            check = verify(A)
            if (check):
                print(total_iter)
                return A
            neg_sol = generate_negations(A, solution)
            cnf.extend(neg_sol) #Negate Solution
        else:
            return []

def generate_negations(A, solution):
    neg_clauses = []
    neg_clauses.append(negate_clause(solution))
    
    #Reflection only + 180 Rotate
    neg_clauses = check_duplicate_clause(neg_clauses,negate_clause(translate_to_clause(reverse_row(A))))
    neg_clauses = check_duplicate_clause(neg_clauses,negate_clause(translate_to_clause(reverse_col(A))))
    neg_clauses = check_duplicate_clause(neg_clauses,negate_clause(translate_to_clause(one_eighty(A))))
    
    if (m == n): 
        #Rotation and both
        neg_clauses = check_duplicate_clause(neg_clauses,negate_clause(translate_to_clause(CW_rotate(A))))
        neg_clauses = check_duplicate_clause(neg_clauses,negate_clause(translate_to_clause(CCW_rotate(A))))
        neg_clauses = check_duplicate_clause(neg_clauses,negate_clause(translate_to_clause(CW_rotate_horizontal_ref(A))))
        neg_clauses = check_duplicate_clause(neg_clauses,negate_clause(translate_to_clause(horizontal_ref_CW_rotate(A))))
    
    return neg_clauses

#File Manipulations

def read_file(path):
    with open(path, "r") as in_file:
        A = [line.split() for line in in_file]
    in_file.close()
    for i in range(m):
        for j in range(n):
            if A[i][j] != "*":
                A[i][j] = int(A[i][j])
    return A
    
def clear_time(path):
    if os.path.exists(path):
        f = open(path, "w")
    else:
        f = open(path, "x")
    f.close()

def write_time(path, duration):
    output_time = open(path, "a")
    output_time.write(str(duration))
    output_time.write(",")
    output_time.close()

def write_next_line(path):
    output_time = open(path, "a")
    output_time.write(" \n")
    output_time.close()


alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

print("e = ",end=' ')
e = input()

time_path = "SAT-ExecTime"+e+".csv"
clear_time(time_path)

rules.extend(rule_2by2())
rules.extend(rule_alternating())

for i in range(26):
    if (alphabet[i] != " "):
        path = alphabet[i]+"/Yin-Yang-"+alphabet[i]+"-"+e+".in"
        print(path)
        
        pbTemp = read_file(path)
        
        for i in range(3):
            playboard = deepcopy(pbTemp)
            cnf = deepcopy(rules)
            board = add_hints(playboard)
            cnf.extend(board)
            start = time.perf_counter()
            sol = find_solution(cnf)
            if sol:
                print("Solution found")
            else:
                print("Puzzle has no solution")
            end = time.perf_counter()
            duration = end - start
            print("duration = ",duration)
            write_time(time_path,duration)
    write_next_line(time_path)