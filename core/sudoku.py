import random
from math import sqrt
import numpy as np

from .helper import *
from .candidate import Candidate
from .population import Population
from .settings import BLOCK_NUMBER, DIGIT_NUMBER, GOAL, POPULATION_SIZE, MAX_GENERATION, MAX_STALE_COUNT, RenderOption
from .given import given

class Sudoku:
    def __init__(self, render):
        self.render = render
        self.reseed_count = 0
        self.exit_flag = False
        self.given = get_chromosome(given.values)
        self.track_grid = None
        self.population = Population()
    
    def fill_predetermined(self):
        """
        Fills some predetermined cells of the Sudoku grid using a pencil marking method.
        """
        self.track_grid = copy_grid(self.given, lambda i, j: set(range(1, DIGIT_NUMBER + 1)))

        def pencil_mark(i, j):
            """
            Marks the value of grid[i][j] element in it's row, column and sub-grid.

            Parameters:
                - i (int): Sub-grid's index.
                - j (int): Sub-grid's element index.

            Returns: The more completed version of the grid.
            """

            # remove from same sub-grid cells
            for a, b in same_sub_grid_indexes(i, j, itself=False):
                self.track_grid[a][b].discard(self.given[i][j])

            # remove from same row cells
            for a, b in same_row_indexes(i, j, itself=False):
                self.track_grid[a][b].discard(self.given[i][j])

            # remove from same column cells
            for a, b in same_column_indexes(i, j, itself=False):
                self.track_grid[a][b].discard(self.given[i][j])

        for i in range(DIGIT_NUMBER):
            for j in range(DIGIT_NUMBER):
                if self.given[i][j] != 0:
                    pencil_mark(i, j)

        while True:
            anything_changed = False

            for i in range(DIGIT_NUMBER):
                for j in range(DIGIT_NUMBER):
                    if self.given[i][j] != 0:
                        continue

                    elif len(self.track_grid[i][j]) == 0:
                        renderTxt = 'The puzzle is unsolvable'
                        self.render(renderTxt, RenderOption.NOT_FOUND)
                    elif len(self.track_grid[i][j]) == 1:
                        self.given[i][j] = list(self.track_grid[i][j])[0]
                        pencil_mark(i, j)

                        # track_grid[i][j] = None
                        anything_changed = True

            if not anything_changed:
                break

    def solve(self):
        """
        Solves the Sudoku puzzle using genetic algorithm.
        """

        # Fill all predetermined value for the puzzle
        self.fill_predetermined()
        print(*self.given, sep="\n")

        # Generate initial candidates
        self.population.generate_initial_candidates(POPULATION_SIZE, self.given, self.track_grid)
        prev_best_fitness = 0
        stale = 0
        cum_elites = []
        self.reseed_count = 0

        # For up to 2000 generations...
        for i in range(MAX_GENERATION):
            if self.exit_flag:
                return

            # Update the best candidate for each generation
            given.bestCandidate = self.population.candidates[0]
            given.bestCandidate.gene = parse_chromosome(self.population.candidates[0].gene)
            prev_best_fitness = self.population.candidates[0].fitness

            if i % 1 == 0:
                print("Generation %d" % i)
                print("Best score: %d" % prev_best_fitness)
                print("Worst score: %d" % self.population.candidates[-1].fitness)

            renderTxt = "Generation %d\n" % i
            renderTxt += "Best fitness: %d\n" % prev_best_fitness
            renderTxt += "Worst fitness: %d\n" % self.population.candidates[-1].fitness
            renderTxt += "Reseed count: %d\n" % self.reseed_count
            self.render(renderTxt)

            # Check for a solution
            if prev_best_fitness == GOAL:
                return

            # Go to next generation if the current population doesn't have solution
            self.population.next_gen(self.given, self.track_grid)

            # Check for stale population
            if self.population.candidates[0].fitness != prev_best_fitness:
                stale = 0
            else:
                stale += 1

            # Re-seed the population if 30 generations have passed with the fittest value not improving.
            if stale > MAX_STALE_COUNT:
                # print("The population has gone stale. Searching in local space...")
                # self.population.local_search(3, self.given, self.track_grid)
                self.reseed_count += 1
                renderTxt = "The population has gone stale. Restarting..."
                self.render(renderTxt, RenderOption.ONLY_TEXT)
                
                # Store the top few solutions (candiddates) from each stale population
                # When enough top solutions accumulate, a new population is created from these best solutions
                # and used as an initial population when the GA is restarted.
                if len(cum_elites) < POPULATION_SIZE:
                    num_elite = int(POPULATION_SIZE * 0.1)
                    cum_elites.extend(self.population.candidates[:num_elite])
                    self.population.generate_initial_candidates(POPULATION_SIZE, self.given, self.track_grid)
                else:
                    print("Activate cumulative method")
                    self.population.candidates = cum_elites
                    cum_elites = []
                stale = 0

        renderTxt = "No solution found."
        self.render(renderTxt, RenderOption.NOT_FOUND)
        return None