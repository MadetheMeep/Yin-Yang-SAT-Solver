from copy import copy, deepcopy
import time
import os

m = 11
n = 9
playboard = []
count = 0

def compare_2by2(s):
    return ((s == '0000') or (s == '1111') or (s == '0110') or (s == '1001'))

#Input Checking
def check_2by2(playboard):
    for i in range(m-1):
        for j in range(n-1):
            #if all cells in the 2x2 box are all the same (all 0 or all 1) the sum will be 0 or 4, plus if it creates alternating pattern (total 2 and (cell i j and i+1 j+1 are the same value))
            s = str(playboard[i][j]) + str(playboard[i+1][j]) + str(playboard[i][j+1]) + str(playboard[i+1][j+1])
            if (compare_2by2(s)): return False
    return True
    
def valid_cell(r,c):
    return ((r >= 0) and (r < m) and (c >=0) and (c < n))
    
def check_connectivity(A, r, c, color):
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
    
def find_first(pb, type): #Finds the first cell containing type, if none found it returns empty array
    for i in range(m):
        for j in range(n):
            if(pb[i][j]==type):
                return [i, j]
    return []
    
def verify(pb):
    # if (m > 1) and (n > 1): #checks if the grid length or height are bigger than 1
        # box_valid = check_2by2(pb, m, n)
    # else:
        # box_valid = True
    # if (box_valid):
    b_count = sum(row.count(0) for row in pb) #count black (0)
    w_count = sum(row.count(1) for row in pb) #count white (1)
    b_start = find_first(pb, 0)
    w_start = find_first(pb, 1)
    if b_start: #checks if b_start is an empty list or not
        b_valid = check_connectivity(pb, b_start[0], b_start[1], 0)
    else:
        b_valid = 0
    if w_start: #checks if w_start is an empty list or not
        w_valid = check_connectivity(pb, w_start[0], w_start[1], 1)
    else:
        w_valid = 0
    if (b_valid == b_count) and (w_valid == w_count):
        return True
    else:
        return False
    # else:
        # return False

def check_surround_2_by_2(playboard, r, c):
    dr = [1,-1,1,-1]
    dc = [1,1,-1,-1]
    
    for i in range(4):
        adj_r = r + dr[i]
        adj_c = c + dc[i]
        if(valid_cell(adj_r,adj_c)):
            s = str(playboard[r][c]) + str(playboard[adj_r][c]) + str(playboard[r][adj_c]) + str(playboard[adj_r][adj_c])
            if(compare_2by2(s)): return False
    return True
    
#Exhaustive
def get_config(playboard):
    configs = []
    config = deepcopy(playboard)
    configs.append(config)
    for i in range(m):
        for j in range(n):
            if (playboard[i][j] == "*"):
                new_list = []
                while configs:
                    new_config = configs.pop(0)
                    new_config[i][j] = 0
                    if (check_surround_2_by_2(new_config, i, j)): new_list.append(deepcopy(new_config))
                    new_config[i][j] = 1
                    if (check_surround_2_by_2(new_config, i, j)): new_list.append(deepcopy(new_config))
                configs = new_list
    return configs
    
def show_config(pb):
    print("")
    for x in pb:
        print(*x, sep=" ")
        
def show_config_array(pb):
    print("")
    for i in range(m):
        for j in range(n):
            print(pb.pop(0), end=" ")
        print("")
        
def convert_array(pb):
    new_pb = []
    for x in pb:
        new_pb.extend(x)
    return new_pb
    
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

time_path = "ExecTime"+e+".csv"
clear_time(time_path)

for i in range(26):
    if (alphabet[i] != " "):
        path = alphabet[i]+"/Yin-Yang-"+alphabet[i]+"-"+e+".in"
        print(path)
        
        pbTemp = read_file(path)
        
        for i in range(3):
            count = 0
            playboard = deepcopy(pbTemp)
            start = time.perf_counter()
            if check_2by2(playboard):
                configs = get_config(playboard)
                solutions = []
                for config in configs:
                    valid = verify(config)
                    if valid:
                        count += 1
                if count == 0:
                    print("no solution")
                else:
                    print(count)
            else:
                print("no solution")
            end = time.perf_counter()
            duration = end - start
            print("duration = ",duration)
            write_time(time_path,duration)
    write_next_line(time_path)
