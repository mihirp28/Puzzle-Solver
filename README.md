# Puzzle-Solver
## Problem
Consider the 2023 puzzle, which is a lot like the 8-puzzle we talked about in class, but: (1) it is 5 x 5 with 25 tiles, so there are no empty spots on the board; (2) instead of moving a single tile into an open space, a move in this puzzle consists of either (a) sliding an entire row of tiles left or right one space, with the left- or right-most tile ‘wrapping around’ to the other side of the board, (b) sliding an entire column of tiles up or down one space, with the top- or bottom-most tile ‘wrapping around’ to the other side of the board, (c) rotating the outer ‘ring’ of tiles either clockwise
or counterclockwise, or (d) rotating the inner ring either clockwise or counterclockwise.

For example, here is a sequence of three moves on such a puzzle:
![image](https://github.com/user-attachments/assets/4a505211-c261-445e-8783-9a9629b501db)
The goal of the puzzle is to find a short sequence of moves that restores the canonical configuration (on the left above) given an initial board configuration. We’ve provided skeleton code to get you started. You can run the skeleton code on the command line:
  python3 solver2023.py [input-board-filename]
where input-board-filename is a text file containing a board configuration (we have provided an example). You’ll need to complete the function called solve(), which should return a list of valid moves. The moves should be encoded as strings in the following way:
• For sliding rows, R (right) or L (left), followed by the row number indicating the row to move left or right. The row numbers range from 1-5.
• For sliding columns, U (up) or D (down), followed by the column number indicating the column to move up or down. The column numbers range from 1-5.
• For rotations, I (inner) or O (outer), followed by whether the rotation is clockwise (c) or counterclockwise (cc). For example, the above diagram performs the moves L3 (slide row 3 left), D3 (slide column 3 down), Occ (outer counterclockwise), and Ic (inner clockwise).

Implement a fast version, using A* search with a suitable heuristic function that guarantees finding a solution in as few moves as possible. For example, board1.txt can be solved in 11 moves. Try to make your code as fast as possible even for difficult boards, although it is not necessarily possible to quickly solve all puzzles. You will need to be creative with your heuristic function in order to find this solution in less than 15 minutes

1. In this problem, what is the branching factor of the search tree?
2. If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? A rough answer is fine

## Solution
move_left(sts, r_m): It moves given row (r_m) in board to left by one position, effectively rotating it.

move_right(sts, r_m): It moves a given row (r_m) in board to right by one position, effectively rotating it in opposite direction of move_left.

rotate_left(brd, r_m, rsdl): It rotates elements in specific row (r_m) of board to left, returning rotated element that "falls off" row.

rotate_right(brd, r_m, rsdl): It rotates elements in specific row (r_m) of board to right, returning rotated element that "falls off" row.

move_inner_ring_clockwise(brd): This function moves inner ring of elements in board in clockwise direction, effectively shifting elements within inner ring.

move_inner_ring_cc_clockwise(brd): It moves inner ring of elements in board in counterclockwise direction, effectively shifting elements within inner ring.

move_clockwise(sts): It moves outer ring of elements in board in clockwise direction, effectively shifting the elements within the outer ring.

move_cclockwise(sts): This function moves the outer ring of elements board in counterclockwise direction, effectively shifting the elements within the outer ring.

transpose_board(brd): It transposes board, exchanging rows for columns and columns for rows.

printable_board(brd): It generates a printable representation of the board for display.

successors(sts): It figures out all the different ways the puzzle can change from the current state sts. It explores ten possibilities for each row and column. For example, it looks at what happens if you move a row or column to the left or right, or if you shift it up or down. Additionally, it checks how the rings of the puzzle rotate clockwise or counterclockwise. For each of these actions, it creates a new puzzle state and notes down what action was taken. It returns a list of these possible next puzzle states along with the actions that were done to get there.

is_goal(sts): The is_goal(sts) function checks if the given puzzle state sts is the final goal state where all the puzzle pieces are in their correct positions, forming a solved puzzle. It compares each puzzle piece's current position with its intended position in the solved state. If all pieces are in their correct spots, it returns True, indicating that the puzzle is solved. Otherwise, it returns False, indicating that the puzzle is not yet solved and needs further moves to reach the goal state.

heuristics_calculation(sts): It measures how far puzzle state sts is from being solved. It does by looking at each number's position and comparing it to where it should be in solved puzzle. For every number, it calculates vertical and horizontal distance it is from its correct position and adds these distances together. This total distance is used as a measure of how close or far the puzzle is from being solved. In simple terms it helps estimate how many steps or moves are likely needed to complete the puzzle based on how far each piece is from where it should be.

eval_func(sts, cost): It calculates how good puzzle state sts is as a potential solution. It combines two factors: Heuristic Value: It measures how close puzzle state is to goal state by calculating Manhattan distance for each puzzle piece to its correct position and adding them up. Path Cost: It considers cost of path taken to reach this puzzle state, where cost represents number of moves made so far.

solve(init_brd): It finds solution to sliding puzzle starting from an initial board configuration init_brd. It uses search algorithm to explore possible moves until it reaches goal state. During search it keeps track of board's configuration actions taken to reach each state, and cost associated with each move. It prioritizes moves based on an evaluation function that combines estimated distance from goal and a dynamic cost factor. Once goal state is reached, function returns a list of actions that represent sequence of moves needed to solve puzzle.

In this problem, what is the branching factor of the search tree?
In this problem, the branching factor of search tree can be calculated by examining the successors function. There are 2 choices for rotating the outer ring There are 2 choices for rotating the inner ring There are 10 possible horizontal row slides There are 10 possible vertical column slides Therefore, the total branching factor of the search tree is 2 (for outer ring rotation) + 2 (for inner ring rotation) + 10 (for horizontal row slides) + 10 (for vertical column slides), which equals 24.

If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search?
If you aim to solve the puzzle in 7 moves using Breadth-First Search (BFS) rather than A* search, you'll likely need to explore a much larger number of states. (i.e) 1+24+24^2+24^3+24^4+24^5+24^6+24^7
