
import sys
from io import StringIO
import pycosat


"""
The implementation of this Sudoku solver is based on the paper:

    "A SAT-based Sudoku solver" by Tjark Weber

    https://www.lri.fr/~conchon/mpri/weber.pdf

If you want to understand the code below, in particular the function valid(),
which calculates the 324 clauses corresponding to 9 cells, you are strongly
encouraged to read the paper first.  The paper is very short, but contains
all necessary information.
"""
import pycosat


def v(i, j, d):
    """
    Return the number of the variable of cell i, j and digit d,
    which is an integer in the range of 1 to 729 (including).
    """
    return 81 * (i - 1) + 9 * (j - 1) + d


def sudoku_clauses():
    """
    Create the (11745) Sudoku clauses, and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    def valid(cells):
        # Append 324 clauses, corresponding to 9 cells, to the result.
        # The 9 cells are represented by a list tuples.  The new clauses
        # ensure that the cells contain distinct values.
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)])
        valid([(j, i) for j in range(1, 10)])
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)])

    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res


import subprocess
def solve(grid):
    """
    solve a Sudoku grid inplace
    """
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal).
            # Note:
            #     We could also remove all variables for the known cells
            #     altogether (which would be more efficient).  However, for
            #     the sake of simplicity, we decided not to do that.
            if d:
                clauses.append([v(i, j, d)])

    # solve the SAT problem
    # verbose = 1 --> see statistics (@ terminal, TBD: get statistics in python)
    sol = set(pycosat.solve(clauses, verbose = 1, vars=729))

    def read_cell(i, j):
        # return the digit of cell i, j according to the solution
        for d in range(1, 10):
            if v(i, j, d) in sol:
                return d

    for i in range(1, 10):
        for j in range(1, 10):
            grid[i - 1][j - 1] = read_cell(i, j)

    return sol


###############################################################################
###############################################################################
###############################################################################
import numpy as np
from pprint import pprint

def sudoku_to_array(sudoku):
    row = []
    rows = []
    j = 0
    for i,char in enumerate(sudoku):
        if char == ".":
            row.append(0)
        else:
            row.append(int(char))
        if ((i+1)%9 == 0):
            rows.append(row)
            j += 1
            row = []
    return rows

def load_data():
    difficulties = ["_simple", "_easy", "_intermediate", "expert",""]
    data = []
    for difficulty in difficulties:
        processed_lines = []
        try:
            with open('data/sudokus_10000{}.csv'.format(difficulty), "r") as csv:
                for text_line in csv:
                    line = text_line.rstrip().split(',')
                    if len(line) > 11:
                        line = line[:-1]
                        line[0] = np.array(sudoku_to_array(line[0]))

                    # Transform string  difficulty into integer levels
                    if line[-1] == "Simple":
                        line[-1] = 0
                    elif line[-1] == "Easy":
                        line[-1] = 1
                    elif line[-1] == "Intermediate":
                        line[-1] = 2
                    elif line[-1] == "Expert":
                        line[-1] = 3

                    processed_lines.append(line)
                # print('sudokus_{}.csv processed!'.format(difficulty))
                data.append(processed_lines)
        except FileNotFoundError:
            # print("sudokus_{}.csv not found!".format(difficulty))
            continue
    try:
        data[0][0]
    except IndexError:
        print("No sudokus file could be found!")
        raise IndexError("No sudokus file could be found!")
    data = data[0]
    return data[0], data[1:] #column names, data

# Main
import sys
column_names, data = load_data()
for i, sudoku_and_features in enumerate(data):
    sys.stdout.flush()
    sudoku = sudoku_and_features[0].tolist()
    # print("Unsolved sudoku")
    # pprint(sudoku)
    solve(sudoku)
    # print("Solved sudoku")
    # pprint(sudoku)
    print("*"*80)
    # print()
