import random
from math import sqrt
import numpy as np

from .candidate import Candidate
from .selection import RankingSelection, Tournament, TopSelection
from .crossover import *
from .settings import BLOCK_NUMBER, DIGIT_NUMBER, POPULATION_SIZE, ELITE_NUMBER, MUTATION_RATE, CROSSOVER_RATE

class Population:
    """ A set of candidate solutions to the Sudoku puzzle. These candidates are also known as
    the chromosomes in the population. """
    def __init__(self):
        self.candidates = []
        self.population_size = POPULATION_SIZE
        self.elitism = ELITE_NUMBER
        self.mutation_rate = MUTATION_RATE
        self.crossover_rate = CROSSOVER_RATE
        self.select_method = TopSelection()
        self.crossover_method = HalfCrossover()
    
    def generate_initial_candidates(self, number, given, tracker):
        """
        Generates an initial population of size "number".

        Parameters:
            - number (int): Number of candidates to generate
            - given (array): The given chromosome of the Sudoku problem
            - tracker (array): Helper array to help evaluate candidates' fitness
        """

        self.candidates = []
        for _ in range(number):
            candidate = Candidate()
            # For each sub grid of candidate
            for i in range(DIGIT_NUMBER):
                # Generate a list of possible value to fill in
                shuffled_sub_grid = list(range(1, DIGIT_NUMBER + 1))

                # Remove all the given values in this sub grid of the given chromosome from possible values list
                for j in range(DIGIT_NUMBER):
                    if given[i][j] != 0:
                        candidate.gene[i][j] = given[i][j]

                        shuffled_sub_grid.remove(given[i][j])

                # Shuffle the list so that possible values can be filled in randomly
                random.shuffle(shuffled_sub_grid)
                for j in range(DIGIT_NUMBER):
                    # Fill possible value to unknown cell in the sub grid
                    if given[i][j] == 0:
                        candidate.gene[i][j] = shuffled_sub_grid.pop()

            self.candidates.append(candidate)
        
        # Evaluate fitness for the population
        self.evaluate(tracker)

    def local_search(self, coef, given, tracker):
        new_population = []
        for candidate in self.candidates:
            new_population.extend(candidate.local_search(coef, given))
        
        list(map(lambda x: x.update_fitness(tracker), new_population))
        
        new_population.sort(key = lambda x: -x.fitness)
        top_num = 10
        top_fit = new_population[:top_num]
        new_population = new_population[top_num:]
        # random.shuffle(new_population)
        self.candidates = top_fit + random.choices(new_population, k=self.population_size - top_num)
    
    def sort(self):
        """ Sort the population based on fitness. """
        self.candidates.sort(key = lambda x: -x.fitness)
    
    def evaluate(self, tracker):
        """ Evaluate fitness of every candidate/chromosome in the population. """
        list(map(lambda x: x.update_fitness(tracker), self.candidates))
        self.sort()

    def next_gen(self, given, tracker):
        """ 
        Find the next generation of the population".

        Parameters:
            - given (array): The given chromosome of the Sudoku problem, helps in mutation process of candidates
            - tracker (array): Helper array to help evaluate candidates' fitness
        """
        elites = []
        num_elite = self.elitism

        # Extract top candidate from population. These elite candidates will 
        # go to the next generation without any change
        for i in range(num_elite):
            elite = Candidate()
            elite.gene = np.copy(self.candidates[i].gene)
            elites.append(elite)

        select_candidates = self.select_method.select_candidates(self.candidates, self.population_size - num_elite)

        new_population = []
        for _ in range(0, self.population_size - num_elite, 2):
            # Select 2 parents
            parents = [select_candidates.pop(), select_candidates.pop()]
            # parents = self.select_method.select_candidates(self.candidates, 2)

            # Crossover them to generate new child for next generation with a crossover rate
            child1, child2 = self.crossover_method.crossover(parents[0], parents[1], self.crossover_rate)

            # Add child to the next genration population
            new_population.append(child1)
            new_population.append(child2)
        
        self.candidates = new_population
        # Mutate candidates in the next generation with a mutation rate
        list(map(lambda x: x.mutate(self.mutation_rate, given), self.candidates))
        self.candidates.extend(elites)

        # Evaluate fitness for the next generation
        self.evaluate(tracker)