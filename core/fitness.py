import numpy as np
from .helper import same_column_indexes, same_row_indexes, get_cells_from_indexes
from .settings import DIGIT_NUMBER, BLOCK_NUMBER, GOAL

class DifferentFitness():
    def cal_fitness(self, candidate, tracker):
        """  The fitness of a candidate solution is determined by
        total sum of number of different numberals in each row and column
        
        Parameters:
            - candidate (Candidate): The candidate to evaluate
            - tracker (array): Helper array that determines all possible values for each cell in the chromosome
        """
        row_fitness = 0
        col_fitness = 0
        candidate.fitness_matrix = np.zeros((2, BLOCK_NUMBER), dtype=int)

        # calculate rows duplicates
        for a, b in same_column_indexes(0, 0):
            row = set()
            for x, y in same_row_indexes(a, b):
                value = candidate.gene[x][y]
                row.add(value)

            row_fitness += len(row)
            candidate.fitness_matrix[0][a // BLOCK_NUMBER] += len(row)
        
        for a, b in same_row_indexes(0, 0):
            col = set()
            for x, y in same_column_indexes(a, b):
                value = candidate.gene[x][y]
                col.add(value)

            col_fitness += len(col)
            candidate.fitness_matrix[1][a] += len(col)

        return row_fitness + col_fitness

class PerfectFitness:
    def cal_fitness(self, candidate, tracker=None):
        """  The fitness of a candidate solution is determined by
        sum of number of different numberals in each row and column
        minus total number of cell that contains invalid value
        
        Parameters:
            - candidate (Candidate): The candidate to evaluate
            - tracker (array): Helper array that determines all possible values for each cell in the chromosome
        """
        row_fitness = 0
        col_fitness = 0
        duplicates_count = 0
        candidate.fitness_matrix = np.zeros((2, BLOCK_NUMBER), dtype=int)

        # calculate rows duplicates
        for a, b in same_column_indexes(0, 0):
            row = set()
            for x, y in same_row_indexes(a, b):
                value = candidate.gene[x][y]
                row.add(value)
                if value not in tracker[x][y]:
                    duplicates_count += 1

            row_fitness += len(row)
            candidate.fitness_matrix[0][a // BLOCK_NUMBER] += len(row)
        
        for a, b in same_row_indexes(0, 0):
            col = set()
            for x, y in same_column_indexes(a, b):
                value = candidate.gene[x][y]
                col.add(value)
                if value not in tracker[x][y]:
                    duplicates_count += 1

            col_fitness += len(col)
            candidate.fitness_matrix[1][a] += len(col)

        return row_fitness + col_fitness - duplicates_count