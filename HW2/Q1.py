import copy
from math import sqrt, cos, sin, pi
import random
import sys

import numpy as np


def fitness_func(x, y):
    return  80 - x**2 - y**2 + 10*cos(2*pi*x) + 10*cos(2*pi*y)

class Cell:
    def __init__(self, x, y, fitness=0.0):
        self.x = x
        self.y = y
        self.fitness = fitness

class NichGA:
    def __init__(
        self,
        population_size: int,
        max_iter: int,
        p_crossover: float,
        p_mutation: float,
        radius: float,
        alpha: float,
        lower: float,
        upper: float,
        select_times: int
    ):
        r"""[GA with Niching sharing method.]

        Args:
            radius (float): [The threshold of dissimilarity (also the
                            distance cutoff or the niche radius]
            alpha (float): [Regulates the shape of the sharing function.]
        """
        self.population_size = population_size
        self.max_iter = max_iter
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.radius = radius
        self.alpha = alpha
        self.select_times = select_times

        self.lower = lower
        self.upper = upper

        self.population = []
        self.pool = []
        self.best_gene_list = []
        self.best_cell = Cell(0, 0, -sys.maxsize)

    def initialize(self):
        for _ in range(self.population_size):
            x = random.uniform(self.lower, self.upper)
            y = random.uniform(self.lower, self.upper)
            # fitness = fitness_func(x, y)
            self.population.append(Cell(x, y, 0))

    def compute_niche_count(self, cur_node):
        niche_count = 0.0
        for node in self.population:
            dis = self.distance(cur_node, node)
            if dis < self.radius:
                niche_count += 1 - (dis / self.radius)**self.alpha
        
        return niche_count if niche_count != 0 else 1.0

    def distance(self, src, tar):
        return sqrt((src.x - tar.x)**2 + (src.y - tar.y)**2)

    def evaluate(self, mode='no'):
        for node in self.population:
            node.fitness  = fitness_func(node.x, node.y)
        if mode == 'init':
            return

        for node in self.population:
            niche_count = self.compute_niche_count(node)
            node.fitness /= niche_count

    def select(self):
        self.pool.clear()
        for node in self.population:
            select_idx = random.randint(0, self.population_size-1)
            for _ in range(self.select_times):
                idx = random.randint(0, self.population_size-1)
                if self.population[select_idx].fitness < self.population[idx].fitness:
                    select_idx = idx

            self.pool.append(self.population[select_idx])

        self.population.clear()
        self.population = copy.deepcopy(self.pool)
    
    def crossover(self):
        for _ in range(self.population_size):
            if random.uniform(0, 1) > self.p_crossover:
                continue
            idx1 = random.randint(0, self.population_size-1)
            idx2 = random.randint(0, self.population_size-1)
            while idx1 == idx2:
                idx2 = random.randint(0, self.population_size-1)

            self.population[idx1].x = self.population[idx2].x
            self.population[idx2].y = self.population[idx1].y

    def mutation(self):
        for node in self.population:
            if random.uniform(0, 1) < self.p_mutation:
                node.x = random.uniform(self.lower, self.upper)
            if random.uniform(0, 1) < self.p_mutation:
                node.y = random.uniform(self.lower, self.upper)

    def run(self):
        self.initialize()
        self.evaluate('init')
        for iter in range(self.max_iter):
            self.select()
            self.crossover()
            self.mutation()
            self.evaluate()

            # Record the best gene in each iteration.
            cur_best_gene = self.find_best()
            self.best_gene_list.append(cur_best_gene)

        self.display_info()

    def find_best(self):
        self.real_eval()
        maximum = -sys.maxsize
        cur_best_iter, cur_best_idx = 0, 0
        for iter, idx in enumerate(range(self.population_size)):
            if self.pool[idx].fitness >  maximum:
                maximum = self.pool[idx].fitness
                cur_best_idx = idx
                cur_best_iter = iter

        # Update the best cell & best iter.
        if self.best_cell.fitness < maximum:
            self.best_cell = self.pool[cur_best_idx]
            self.best_iter = cur_best_iter

        return self.pool[cur_best_idx]


    def display_info(self, iter_interval: int = 100):
        for iter in range(0, len(self.best_gene_list), iter_interval):
            node = self.best_gene_list[iter]
            print(f'Iteration: {iter}')
            print(f'Best fitness: {node.fitness}')
            print(f'(x, y): ({node.x}, {node.y})')
            print('========\n')

        print(f'All best fitness: {self.best_cell.fitness}')
        print(f'All best (x, y): ({self.best_cell.x}, {self.best_cell.y})')
        print(f'All best iter: {self.best_iter}')

    def real_eval(self):
        for node in self.pool:
            node.fitness = fitness_func(node.x, node.y)

    def find_peak(self, k: int = 3):
        top_k = 4
        tmp = []
        print(f'\nFind {k} peaks')
        sorted_genes = sorted(self.best_gene_list, key=lambda x: x.fitness, reverse=True)
        for i, node in enumerate(sorted_genes[:k]):
            # print(f'Peak {i}:')
            # print(f'fitness {node.fitness}:')
            # print(f'(x, y) ({node.x:.4f}, {node.y:.4f}):')
            # print('----')
            # if i < top_k or node.fitness >= 91:
            #     tmp.append(node)
            #     continue

            counter = 0
            for other in tmp:
                if self.distance(other, node) >= 1:
                    print('##')
                    counter += 1

            if counter == len(tmp):
                tmp.append(node)
            
            if len(tmp) == top_k
        for i, node in enumerate(tmp):
            print(f'Peak {i}')
            print(f'fitness = {fitness_func(node.x, node.y)}:')
            print(f'(x, y) = ({node.x:.4f}, {node.y:.4f}):')
            print('----')

        return tmp


if __name__ == '__main__':
    max_iter = 1000
    population_size = 150
    lower, upper = -0.5, 1.500001
    p_mutation, p_crossover = 0.01, 0.25
    select_times = 5

    alpha = 1
    radius = 0.25

    exp_num = 1
    for exp in range(exp_num):
        ga = NichGA(
            population_size=population_size,
            max_iter=max_iter,
            p_crossover=p_crossover,
            p_mutation=p_mutation,
            radius=radius,
            alpha=alpha,
            lower=lower,
            upper=upper,
            select_times=select_times
        )

        ga.run()

        ga.find_peak(k=30)
    