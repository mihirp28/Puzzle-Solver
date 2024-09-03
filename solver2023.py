#!/usr/local/bin/python3
# solver2023.py : 2023 Sliding tile puzzle solver
#
# Code by: snemanoh-mjp5-npoojary
#
# Based on skeleton code by B551 Staff, Fall 2023
#

import sys
import heapq
import copy
import numpy as np

ROWS = 5
COLS = 5

def move_left(sts, r_m):
    # Moving the given r_m to left one position
    brd = copy.deepcopy(sts)
    brd[r_m] = brd[r_m][1:] + brd[r_m][:1]

    return brd

def move_right(sts, r_m):
    # Moving the given r_m to right one position
    brd = copy.deepcopy(sts)
    brd[r_m] = brd[r_m][-1:] + brd[r_m][:-1]

    return brd

def rotate_left(brd, r_m, rsdl):
    # Rotating matrix to left
    brd[r_m] = brd[r_m][:-1] + [rsdl] + [brd[r_m][-1]]
    rsdl = brd[r_m].pop(0)
    
    return rsdl

def rotate_right(brd, r_m, rsdl):
    # Rotating matrix to right
    brd[r_m] = [brd[r_m][0]] + [rsdl] + brd[r_m][1:]
    rsdl = brd[r_m].pop()

    return rsdl

def move_inner_ring_clockwise(brd):
    # Moving clockwise inner ring 
    sts = np.array(brd)

    inner_brd = sts[1:-1, 1:-1].tolist()
    inner_brd = move_clockwise(inner_brd)

    sts[1:-1, 1:-1] = np.array(inner_brd)

    return sts.tolist()

def move_inner_ring_cc_clockwise(brd):
    # Moving counter-clockwise inner ring 
    sts = np.array(brd)

    inner_brd = sts[1:-1, 1:-1].tolist()
    inner_brd = move_cclockwise(inner_brd)

    sts[1:-1, 1:-1] = np.array(inner_brd)

    return sts.tolist()

def move_clockwise(sts):
    # Moving clockwise outer ring 
    brd = copy.deepcopy(sts)
    brd[0] = [brd[1][0]] + brd[0]
    rsdl = brd[0].pop()

    brd = transpose_board(brd)
    rsdl = rotate_right(brd, -1, rsdl)

    brd = transpose_board(brd)
    rsdl = rotate_left(brd, -1, rsdl)

    brd = transpose_board(brd)
    rsdl = rotate_left(brd, 0, rsdl)

    brd = transpose_board(brd)

    return brd

def move_cclockwise(sts):
    # Moving counter-clockwise outer ring 
    brd = copy.deepcopy(sts)
    brd[0] = brd[0] + [brd[1][-1]]
    rsdl = brd[0].pop(0)

    brd = transpose_board(brd)
    rsdl = rotate_right(brd, 0, rsdl)

    brd = transpose_board(brd)
    rsdl = rotate_right(brd, -1, rsdl)

    brd = transpose_board(brd)
    rsdl = rotate_left(brd, -1, rsdl)

    brd = transpose_board(brd)

    return brd

def transpose_board(brd):
    # Transpose the brd i.e. changing r_m to column
    return [list(col) for col in zip(*brd)]

def printable_board(brd):
    # Printing the brd
    return [("%3d ") * COLS % brd[j : (j + COLS)] for j in range(0, ROWS * COLS, COLS)]    

# Returning possible successor states list
def successors(sts):
    # Successor states list
    sts_successors_list = []

    # Ten Successors with rows horizontally shifted 
    for row in range(ROWS):
        # Shifting right one cell
        child_sts = move_right(sts, row)
        sts_successors_list.append([child_sts, "R" + str(row + 1)])

        # Shifting left one cell
        child_sts = move_left(sts, row)
        sts_successors_list.append([child_sts, "L" + str(row + 1)])

    # Ten Successors with rows vertically shifted 
    for col in range(COLS):
        # Shifting up one cell
        child_sts = transpose_board(move_left(transpose_board(sts), col))
        sts_successors_list.append([child_sts, "U" + str(col + 1)])

        # Shifting down one cell
        child_sts = transpose_board(move_right(transpose_board(sts), col))
        sts_successors_list.append([child_sts, "D" + str(col + 1)])

    # Rotating clockwise Outer ring
    child_sts = move_clockwise(sts)
    sts_successors_list.append([child_sts, "Oc"])

    # Rotating counter-clockwise Outer ring
    child_sts = move_cclockwise(sts)
    sts_successors_list.append([child_sts, "Occ"])

    # Rotating clockwise Inner ring
    child_sts = move_inner_ring_clockwise(sts)
    sts_successors_list.append([child_sts, "Ic"])

    # Rotating counter-clockwise Inner ring
    child_sts = move_inner_ring_cc_clockwise(sts)
    sts_successors_list.append([child_sts, "Icc"])

    return sts_successors_list

# Checking if we have reached the goal state
def is_goal(sts):
    goal_sts = [ [1, 2, 3, 4, 5],
                   [6, 7, 8, 9, 10],
                   [11, 12, 13, 14, 15],
                   [16, 17, 18, 19, 20],
                   [21, 22, 23, 24, 25],]

    for i in range(5):
        for j in range(5):
            if goal_sts[i][j] != sts[i][j]:
                return False
            
    return True

# Using Manhattan distance as a heusristic function
def heuristics_calculation(sts):
    heur = 0
    for i in range(len(sts)):
        for j in range(len(sts[0])):
            goal_i = (sts[i][j] - 1) // 5
            goal_j = (sts[i][j] - 1) % 5
            heur = heur + abs(i - goal_i) + abs(j - goal_j)

    return heur

def eval_func(sts, cost):
    # Using daptive cost in the path finding algorithms
    return heuristics_calculation(sts) + pow(cost, 2) * 0.2

def solve(init_brd):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(init_brd) and it should return
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    init_brd = np.array(init_brd).reshape(ROWS, COLS).tolist()

    prior_que = []
    evaluation_func = eval_func(init_brd, 0)
    vis_sts = set()

    combined_elm = [evaluation_func, init_brd, [], 0]
    heapq.heappush(prior_que, combined_elm)

    while prior_que:
        (evaluation_func, sts, ttl_route, cost) = heapq.heappop(prior_que)

        if is_goal(sts):
            return ttl_route

        sts_successors_list = successors(sts)
        list_sts = tuple(tuple(r_m) for r_m in sts)

        if list_sts not in vis_sts:
            for elm in sts_successors_list:
                elm_route = copy.deepcopy(ttl_route)
                successor_sts = elm[0]
                extended_route = elm[1]
                elm_route.append(extended_route)

                combined_elm = [ eval_func(successor_sts, cost + 1),
                                     successor_sts,
                                     elm_route,
                                     cost + 1,]
                
                heapq.heappush(prior_que, combined_elm)

            vis_sts.add(list_sts)

    return ttl_route

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise (Exception("Error: expected a brd filename"))

    start_state = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != ROWS * COLS:
        raise (Exception("Error: couldn't parse start sts file"))

    print("Start sts: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
