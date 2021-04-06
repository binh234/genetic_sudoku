import random
from .settings import DIGIT_NUMBER

class RandomMutation:
    def __init__(self):
        self.method = [SwapMutation(), RandomResetting()]
        self.weight = [0.8, 0.2]

    def mutate(self, candidate, given):
        method = random.choices(self.method, weights=self.weight)[0]
        return method.mutate(candidate, given)

class SwapMutation:
    def mutate(self, candidate, given):
        """  Mutate a candidate gene. Two numerals within a
        sub-block that are not given in the starting point are 
        selected randomly and their positions are swapped.
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        random_sub_grid = random.randint(0, DIGIT_NUMBER - 1)
        possible_swaps = []
        success = False

        # Get all unknown cells index
        for grid_element_index in range(DIGIT_NUMBER):
            if given[random_sub_grid][grid_element_index] == 0:
                possible_swaps.append(grid_element_index)

        # Select two indexes and swap their values
        if len(possible_swaps) > 1:
            success = True
            random.shuffle(possible_swaps)
            first_index, second_index = random.choices(possible_swaps, k=2)
            tmp = candidate.gene[random_sub_grid][first_index]
            candidate.gene[random_sub_grid][first_index] = candidate.gene[random_sub_grid][second_index]
            candidate.gene[random_sub_grid][second_index] = tmp
        
        return success

class MultiSwapMutation:
    def __init__(self):
        self.weights = [0.625, 0.304, 0.066, 0.005, 0.0001]

    def mutate(self, candidate, given):
        """  Mutate a candidate gene. Performs 1 to 5 swap mutations to the candidate gene
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        # Randomly select 1 to 5 swap actions to perform
        num_swap = random.choices(list(range(1, 6)), weights=self.weights, k=1)[0]
        success = False

        for _ in range(num_swap):
            random_sub_grid = random.randint(0, DIGIT_NUMBER - 1)
            possible_swaps = []
            # Get all unknown cells index
            for grid_element_index in range(DIGIT_NUMBER):
                if given[random_sub_grid][grid_element_index] == 0:
                    possible_swaps.append(grid_element_index)

            # Select two indexes and swap their values
            if len(possible_swaps) > 1:
                success = True
                random.shuffle(possible_swaps)
                first_index, second_index = random.choices(possible_swaps, k=2)
                tmp = candidate.gene[random_sub_grid][first_index]
                candidate.gene[random_sub_grid][first_index] = candidate.gene[random_sub_grid][second_index]
                candidate.gene[random_sub_grid][second_index] = tmp
        
        return success

class AllSwapMutation:
    def mutate(self, candidate, given):
        """  Mutate a candidate gene. Performs swap mutations to each sub-block in 
        the gene with a rate of 16%.
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        for sub_grid in range(DIGIT_NUMBER):
            if random.random() < 0.16:
                possible_swaps = []
                for grid_element_index in range(DIGIT_NUMBER):
                    if given[sub_grid][grid_element_index] == 0:
                        possible_swaps.append(grid_element_index)
                if len(possible_swaps) > 1:
                    random.shuffle(possible_swaps)
                    first_index, second_index = random.choices(possible_swaps, k=2)
                    tmp = candidate.gene[sub_grid][first_index]
                    candidate.gene[sub_grid][first_index] = candidate.gene[sub_grid][second_index]
                    candidate.gene[sub_grid][second_index] = tmp
        
        return True

class RandomResetting:
    def mutate(self, candidate, given):
        """  Mutate a candidate gene. Selects a sub-block and sets randomly values to
        all cells contain unknown value in the statring Sudoku puzzle
        
        Parameters:
            - candidate (Candidate): The candidate to mutate
            - given (array): Helper array that determines all fixed values in the statring Sudoku puzzle
        """
        random_sub_grid = random.randint(0, DIGIT_NUMBER - 1)
        possible_values = list(range(1, DIGIT_NUMBER + 1))
        for grid_element_index in range(DIGIT_NUMBER):
            if given[random_sub_grid][grid_element_index] != 0:
                possible_values.remove(given[random_sub_grid][grid_element_index])

        random.shuffle(possible_values)
        for grid_element_index in range(DIGIT_NUMBER):
            if given[random_sub_grid][grid_element_index] == 0:
                candidate.gene[random_sub_grid][grid_element_index] = possible_values.pop()
        
        return True