from .candidate import Candidate
from .settings import DIGIT_NUMBER
import random
import numpy as np

class RandomCrossover:
    def __init__(self):
        self.method = [Crossover(), RowColCrossover(), UniformCrossover(), TwoPointCrossover()]
        self.weight = [0.3, 0.4, 0.2, 0.1]
    
    def crossover(self, parent1, parent2, crossover_rate):
        method = random.choices(self.method, weights=self.weight, k=1)[0]
        return method.crossover(parent1, parent2, crossover_rate)

class Crossover:
    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes.
        Parent genes are splitted by one point and then concatenate to generate child genes
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossover_rate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = np.copy(parent1.gene)
        grid2 = np.copy(parent2.gene)

        grid_size = len(parent1.gene)

        r = random.random()
        if r < crossover_rate:
            # Get a ranom crossover point to split parent genes
            cross_point = random.randint(1, grid_size - 2)
            child1.gene = np.concatenate((grid1[:cross_point], grid2[cross_point:]), axis=0)
            child2.gene = np.concatenate((grid2[:cross_point], grid1[cross_point:]), axis=0)
        else:
            child1.gene = grid1
            child2.gene = grid2

        return child1, child2

class RowColCrossover:
    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes.
            When two child individuals are generated from two parents, scores are obtained 
            for each of the three rows that constitute the sub-blocks of the parents, 
            and a child inherits the ones with the highest scores. Then the columns are 
            compared in the same way and the other child inherits the ones with the highest scores. 
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossover_rate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = parent1.gene
        grid2 = parent2.gene

        r = random.random()
        if r < crossover_rate:
            row_score1 = parent1.fitness_matrix[0]
            row_score2 = parent2.fitness_matrix[0]

            col_score1 = parent1.fitness_matrix[1]
            col_score2 = parent2.fitness_matrix[1]

            for i in range(3):
                if row_score1[i] > row_score2[i]:
                    child1.gene[3*i:3*(i+1)] = np.copy(grid1[3*i:3*(i+1)])
                else:
                    child1.gene[3*i:3*(i+1)] = np.copy(grid2[3*i:3*(i+1)])
                
                if col_score1[i] > col_score2[i]:
                    for j in range(3):
                        child2.gene[j * 3 + i] = np.copy(grid1[j * 3 + i])
                else:
                    for j in range(3):
                        child2.gene[j * 3 + i] = np.copy(grid2[j * 3 + i])
        else:
            child1.gene = np.copy(grid1)
            child2.gene = np.copy(grid2)

        return child1, child2

class UniformCrossover:
    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes. 
        Parent genes will swap 2 consecutive blocks to generate child genes
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossover_rate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = np.copy(parent1.gene)
        grid2 = np.copy(parent2.gene)

        grid_size = len(parent1.gene)
        r = random.random()
        if r < crossover_rate:
            cross_point = random.randint(0, grid_size - 1)
            tmp = grid1[cross_point]
            grid1[cross_point] = grid2[cross_point]
            grid2[cross_point] = tmp
            child1.gene = grid1
            child2.gene = grid2
        else:
            child1.gene = grid1
            child2.gene = grid2

        return child1, child2

class TwoPointCrossover:
    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes.
        Parent genes are splitted by two point and then concatenate to generate child genes 
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossover_rate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = np.copy(parent1.gene)
        grid2 = np.copy(parent2.gene)

        grid_size = len(parent1.gene)
        r = random.random()
        if r < crossover_rate:
            cross_point1 = random.randint(1, grid_size - 2)
            cross_point2 = random.randint(cross_point1 + 1, grid_size - 1)
            child1.gene = np.concatenate((grid1[:cross_point1], grid2[cross_point1:cross_point2], grid1[cross_point2:]), axis=0)
            child2.gene = np.concatenate((grid2[:cross_point1], grid1[cross_point1:cross_point2], grid2[cross_point2:]), axis=0)
        else:
            child1.gene = grid1
            child2.gene = grid2

        return child1, child2

class ChoiceCrossover:
    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes.
        The child will randomly choose each sub grid from first parent or second parent 
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossover_rate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = parent1.gene
        grid2 = parent2.gene

        grid_size = len(parent1.gene)
        r = random.random()
        if r < crossover_rate:
            for i in range(grid_size):
                blocks = [grid1[i], grid2[i]]
                child1.gene[i] = np.copy(random.choice(blocks))
                child2.gene[i] = np.copy(random.choice(blocks))
        else:
            child1.gene = np.copy(grid1)
            child2.gene = np.copy(grid2)

        return child1, child2

class HalfCrossover:
    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes. 
        The first child will randomly choose each sub grid from first parent or second parent
        and the seond child will get all unchoosen sub grid
        
        Parameters:
            - parent1 (Candidate): First parent to crossover
            - parent2 (Candidate): Second parent to crossover
            - crossover_rate (float): Ratio defines if these parents are crossover or not
        
        Return:
            Tuple of two child generate from the crossover process
        """

        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        grid1 = parent1.gene
        grid2 = parent2.gene

        grid_size = len(parent1.gene)
        r = random.random()
        if r < crossover_rate:
            for i in range(grid_size):
                if random.random() < 0.5:
                    child1.gene[i] = np.copy(grid1[i])
                    child2.gene[i] = np.copy(grid2[i])
                else:
                    child1.gene[i] = np.copy(grid2[i])
                    child2.gene[i] = np.copy(grid1[i])
        else:
            child1.gene = np.copy(grid1)
            child2.gene = np.copy(grid2)

        return child1, child2