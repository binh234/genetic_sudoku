import random
from math import sqrt
import numpy as np

from .mutation import *
from .fitness import *
from .settings import DIGIT_NUMBER, BLOCK_NUMBER

class Candidate:
    def __init__(self):
        self.gene = np.zeros((DIGIT_NUMBER, DIGIT_NUMBER), dtype=int)
        self.fitness = 0
        self.fitness_matrix = np.zeros((2, BLOCK_NUMBER), dtype=int)
        self.fitness_method = PerfectFitness()
        self.mutate_method = SwapMutation()
        self.local_search_method = SwapMutation()

    def update_fitness(self, tracker):
        """
        Calculates the fitness value for a candidate.
        """
        self.fitness = self.fitness_method.cal_fitness(self, tracker)

    def mutate(self, mutation_rate, given):
        """
        Mutates a candidate with a mutation_rate.
        """
        r = random.random()
    
        if r < mutation_rate:  # Mutate.
            return self.mutate_method.mutate(self, given)
    
        return False

    def local_search(self, coef, given):
        candidate_list = []
        for _ in range(coef):
            candidate = Candidate()
            candidate.gene = np.copy(self.gene)
            candidate.local_search_method.mutate(self, given)
            candidate_list.append(candidate)
        
        return candidate_list
