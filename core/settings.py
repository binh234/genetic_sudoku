from tkinter.constants import DISABLED
from numpy import sqrt

""" Genetic Algorithm Settings """
BLOCK_NUMBER = 3  # Number of digits on 1 row per box.
DIGIT_NUMBER = 9  # Number of digits (Standard Sudoku is 9).
POPULATION_SIZE = 1000  # Number of candidates (i.e. population size).
ELITE_NUMBER = 0  # Number of elites (Elites will alive after generation).
MAX_GENERATION = 2000  # Number of generations.
MUTATION_RATE = 0.8
CROSSOVER_RATE = 1
MAX_STALE_COUNT = 30
GOAL = 162

""" UI Setting """
BOARD_SIZE = 600
DIGIT_SIZE = 36
DIGIT_SPACE = int((BOARD_SIZE/DIGIT_NUMBER)/2)
TEXT_SIZE = 18
FONT_FAMILY = "*"
NORMAL_DIGIT_COLOR = "blue"
GIVEN_DIGIT_COLOR = "black"
DUPLICATE_DIGIT_BG = "tomato"
DUPLICATE_DIGIT_GIVEN_BG = "orange"
SOLUTION_DIGIT_BG = "spring green"
SOLUTION_DIGIT_GIVEN_BG = "green yellow"
TRANSPARENT_DIGIT_BG = ""

# UI Option
class RenderOption:
    NORMAL = 0
    FOUNDED = 1
    NOT_FOUND = 2
    ONLY_TEXT = 3
class OpenButtonOption:
    OPEN = 0
    CLOSE = 1
    NORMAL = 2
    DISABLED = 3
class WriteButtonOption:
    WRITE = 0
    SAVE = 1
    NORMAL = 2
    DISABLED = 3
class ClearButtonOption:
    NORMAL = 0
    DISABLED = 1
class SolveButtonOption:
    SOLVE = 0
    CANCEL = 1
    READY = 2
    NORMAL = 3
    DISABLED = 4