import random

class RankingSelection:
    def select_candidates(self, candidates, number):
        """ Select a number of candidates from given candidates list.
        Fitness level is used to associate a probability of selection with each candidate.
        
        Parameters:
            - candidates (list): given candidates list to select
            - number (int): number of candidates to select
        """
        fitness_weight = [c.fitness for c in candidates]
        selected_candidates = random.choices(candidates, weights=fitness_weight, k=number)

        return selected_candidates

class Tournament:
    def __init__(self, size=2, selection_rate=0.8):
        self.size = size
        self.selection_rate = selection_rate

    def select_candidates(self, candidates, number):
        """ Select a number of candidates from given candidates list.
        Involves running several "tournaments" among a few individuals (or chromosomes) chosen at random from the population.
        
        Parameters:
            - candidates (list): given candidates list to select
            - number (int): number of candidates to select
        """
        selected_candidates = []
        for _ in range(0, number):
            competitors = random.choices(candidates, k=self.size)
            selected_candidates.append(self.compete(competitors))

        return selected_candidates

    def compete(self, competitors):
        competitors.sort(key=lambda x: -x.fitness)
        q = 1 - self.selection_rate
        cum_rate = q

        r = random.random()
        for i in range(0, len(competitors) - 1):
            if r < 1 - cum_rate:
                return competitors[i]
            else:
                cum_rate = cum_rate * q
        return competitors[-1]

class TopSelection:
    def __init__(self, selection_rate=0.2):
        self.selection_rate = selection_rate

    def select_candidates(self, candidates, number):
        """ Randomly select a number of candidates from top portion of given candidates list.
        
        Parameters:
            - candidates (list): given candidates list to select
            - number (int): number of candidates to select
        """
        top_index = int(self.selection_rate * len(candidates))

        return random.choices(candidates[:top_index], k=number)