import numpy as np
from math import sqrt
from .settings import BLOCK_NUMBER, DIGIT_NUMBER

def same_column_indexes(i, j, itself=True):
    """
    A generator function that yields indexes of the elements that are in the same column as the input indexes.

    Parameters:
        - i (int): Sub-grid's index.
        - j (int): Sub-grid's element index.
        - itself (bool) (optional=True): Indicates whether to yield the input indexes or not.
    """

    DIGIT_NUMBER = BLOCK_NUMBER * BLOCK_NUMBER
    sub_grid_column = i % BLOCK_NUMBER
    cell_column = j % BLOCK_NUMBER

    for a in range(sub_grid_column, DIGIT_NUMBER, BLOCK_NUMBER):
        for b in range(cell_column, DIGIT_NUMBER, BLOCK_NUMBER):
            if (a, b) == (i, j) and not itself:
                continue

            yield (a, b)


def same_row_indexes(i, j, itself=True):
    """
    A generator function that yields indexes of the elements that are in the same row as the input indexes.

    Parameters:
        - i (int): Sub-grid's index.
        - j (int): Sub-grid's element index.
        - itself (bool) (optional=True): Indicates whether to yield the input indexes or not.
    """

    sub_grid_row = int(i / BLOCK_NUMBER)
    cell_row = int(j / BLOCK_NUMBER)

    for a in range(sub_grid_row * BLOCK_NUMBER, sub_grid_row * BLOCK_NUMBER + BLOCK_NUMBER):
        for b in range(cell_row * BLOCK_NUMBER, cell_row * BLOCK_NUMBER + BLOCK_NUMBER):
            if (a, b) == (i, j) and not itself:
                continue

            yield (a, b)


def same_sub_grid_indexes(i, j, itself=True):
    """
    A generator function that yields indexes of the elements that are in the same sub-grid as the input indexes.

    Parameters:
        - i (int): Sub-grid's index.
        - j (int): Sub-grid's element index.
        - itself (bool) (optional=True): Indicates whether to yield the input indexes or not.
    """

    for k in range(BLOCK_NUMBER * BLOCK_NUMBER):
        if k == j and not itself:
            continue

        yield (i, k)


def get_cells_from_indexes(grid, indexes):
    """
    A generator function that yields the values of a list of grid indexes.

    Parameters:
        - grid (list)
        - indexes (list) : e.g. [[1, 2], [3, 10]]
    """

    for a, b in indexes:
        yield grid[a][b]

def copy_grid(grid, elem_generator=None):
    """
    Returns an empty Sudoku grid.

    Parameters:
        - elem_generator (function) (optional=None): Is is used to generate initial values of the grid's elements.
            If it's not given, all grid's elements will be "None".
    """

    return np.array([
        [
            (0 if elem_generator is None else elem_generator(i, j))
            for j in range(len(grid))
        ] for i in range(len(grid))
    ])

def get_chromosome(grid):
    """
    Returns chromosome of Sudoku puzzle. The chromosome of a puzzle is 
    defined as an array of 81 numbers that is divided into nine sub block.

    Parameters:
        - grid: Sudoku puzzle
    """
    chromosome = [[] for i in range(DIGIT_NUMBER)]
    for j in range(DIGIT_NUMBER):
        for i in range(DIGIT_NUMBER):
            chromosome[
                int(i / BLOCK_NUMBER) +
                int(j / BLOCK_NUMBER) * BLOCK_NUMBER
                ].append(grid[j][i])

    return np.array(chromosome)

def parse_chromosome(chromosome):
    """
    Returns Sudoku puzzle of chromosome.

    Parameters:
        - chromosome: Chromosome.
    """
    grid = np.zeros_like(chromosome)

    i = 0
    for a, b in same_column_indexes(0, 0, BLOCK_NUMBER):
        row = list(get_cells_from_indexes(chromosome, same_row_indexes(a, b, BLOCK_NUMBER)))
        grid[i] = np.array(row)
        i +=1

    return grid