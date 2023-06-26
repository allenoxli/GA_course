import copy
from math import sqrt, cos, sin, pi
import random
import sys

import numpy as np

class Cell:
    def __init__(self, x, y, fitness=0.0):
        self.x = x
        self.y = y
        self.fitness = fitness

def total_area(r, h):
    # Area function.
    B = base_area(r, h)
    S = surface_area(r, h)
    return B + S

def base_area(r, h):
    return -1 * pi * r**2

def surface_area(r, h):
    s = sqrt(r**2 + h**2)
    return -1* pi * r * s

def volume(r, h):
    return pi * r**2 * h / 3

class ParetoFrontierGA:
    def __init__(
        self,
        population_size: int,
        max_iter: int,
        p_crossover: float,
        p_mutation: float,
        radius: float,
        alpha: float,
        r_bounded,
        h_bounded,
        select_times: int,
        base_area,
        surface_area,
        total_area
    ):
        self.population_size = population_size
        self.max_iter = max_iter
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.radius = radius
        self.alpha = alpha
        self.select_times = select_times

        self.base_area = base_area
        self.surface_area = surface_area
        self.total_area = total_area

        self.r_bounded = r_bounded
        self.h_bounded = h_bounded

        self.population = []
        self.pool = []
        self.best_gene_list = []
        self.best_cell = Cell(0, 0, -sys.maxsize)
        self.prev_cell = Cell(0, 0, -sys.maxsize)
        self.now_cell = Cell(0, 0, -sys.maxsize)

    def check_volume(self, x, y):
        while volume(x, y) <= 200:
            if  self.best_cell.fitness != -sys.maxsize:
                epsilon = 1e-4
                return self.best_cell.x + epsilon, self.best_cell.y + epsilon

            x = random.uniform(*self.r_bounded)
            y = random.uniform(*self.h_bounded)
        return x, y

    def initialize(self):
        for _ in range(self.population_size):
            x = random.uniform(*self.r_bounded)
            y = random.uniform(*self.h_bounded)
            x, y = self.check_volume(x, y)
            fitness = self.total_area(x, y)
            self.population.append(Cell(x, y, fitness))

    def evaluate(self, fitness_func):
        for node in self.population:
            node.fitness  = fitness_func(node.x, node.y)

    def select(self):
        rev_pop = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        sum_fits = sum(node.fitness for node in self.population)
        chosen = []
        for i in range(self.population_size):
            u = random.random() * sum_fits
            sum_ = 0
            for node in rev_pop:
                sum_ += node.fitness
                if sum_ > u:
                    chosen.append(node)
                    break

        self.population.clear()
        self.population = copy.deepcopy(chosen)
        chosen.clear()

    def crossover(self):
        for _ in range(self.population_size):
            if random.uniform(0, 1) > self.p_crossover:
                continue
            idx1 = random.randint(0, len(self.population)-1)
            idx2 = random.randint(0, len(self.population)-1)
            while idx1 == idx2:
                idx2 = random.randint(0, len(self.population)-1)

            self.population[idx1].x = self.population[idx2].x
            self.population[idx2].y = self.population[idx1].y
            
            x1, y1 = self.population[idx1].x, self.population[idx1].y
            x2, y2 = self.population[idx2].x, self.population[idx2].y
            x1, y1 = self.check_volume(x1, y1)
            x2, y2 = self.check_volume(x2, y2)
            self.population[idx1].x, self.population[idx1].y = x1, y1
            self.population[idx2].x, self.population[idx2].y = x2, y2

    def mutation(self):
        for node in self.population:
            if random.uniform(0, 1) < self.p_mutation:
                node.x = random.uniform(*self.r_bounded)
            if random.uniform(0, 1) < self.p_mutation:
                node.y = random.uniform(*self.h_bounded)

            node.x, node.y = self.check_volume(node.x, node.y)

    def run(self):
        state_idx = 0
        wrose_times = 0
        prev_cell = None
        eval_func = [self.total_area, self.base_area, self.surface_area]
        self.initialize()
        for iter in range(self.max_iter):
            self.select()
            self.crossover()
            self.mutation()
            self.evaluate(eval_func[state_idx])
            cur_best_gene = self.find_best()

            # Record the best gene in each iteration.
            self.best_gene_list.append(cur_best_gene)
            if prev_cell == None:
                prev_cell = Cell(cur_best_gene.x, cur_best_gene.y, cur_best_gene.fitness)
            
            if prev_cell.fitness > cur_best_gene.fitness:
                wrose_times += 1
                if  wrose_times > 10:
                    wrose_times = 0
                    state_idx = (state_idx + 1) % 3
                    state_idx = 1 if state_idx == 0 else state_idx 

            prev_cell = Cell(cur_best_gene.x, cur_best_gene.y, cur_best_gene.fitness)


    def find_best(self):
        maximum = -sys.maxsize
        cur_best_iter, cur_best_idx = 0, 0
        for i in range(len(self.population)):
            if self.population[i].fitness >  maximum:
                maximum = self.population[i].fitness
                cur_best_idx = i

        # print(cur_best_idx, maximum, self.population[15].fitness)
        self.now_cell = self.population[cur_best_idx]

        # Update the best cell & best iter.
        if self.best_cell.fitness < maximum:
            self.best_cell = self.population[cur_best_idx]
            self.best_iter = cur_best_iter

        return self.population[cur_best_idx]

    def distance(self, src, tar):
        return sqrt((src.x - tar.x)**2 + (src.y - tar.y)**2)

    def display_info(self, iter_interval: int = 200):
        for iter in range(0, len(self.best_gene_list), iter_interval):
            node = self.best_gene_list[iter]
            print(f'Iteration: {iter}')
            print(f'Best fitness: {-node.fitness:.4f}')
            print(f'Best volume: {volume(node.x, node.y):.4f}')
            print(f'(x, y): ({node.x:.4f}, {node.y:.4f})')
            print('========\n')

        print(f'All best fitness: {-self.best_cell.fitness:.4f}')
        print(f'All best volume: {volume(self.best_cell.x, self.best_cell.y):.4f}')
        print(f'All best (x, y): ({self.best_cell.x:.4f}, {self.best_cell.y:.4f})')
        print(f'All best iter: {self.best_iter}')


if __name__ == '__main__':
    max_iter = 5000
    population_size = 50
    p_mutation, p_crossover = 0.01, 0.25
    select_times = 5

    alpha = 1
    radius = 0.1

    r_bounded, h_bounded = [0, 10], [0, 20]

    exp_num = 100
    total_r, total_h, total_fits, total_vol = [], [], [], []
    for exp in range(exp_num):
        ga = ParetoFrontierGA(
            population_size=population_size,
            max_iter=max_iter,
            p_crossover=p_crossover,
            p_mutation=p_mutation,
            radius=radius,
            alpha=alpha,
            r_bounded=r_bounded,
            h_bounded=h_bounded,
            select_times=select_times,
            base_area=base_area,
            surface_area=surface_area,
            total_area=total_area
        )

        ga.run()
        # self.display_info()


        total_r.append(ga.best_cell.x)
        total_h.append(ga.best_cell.y)
        total_fits.append(ga.best_cell.fitness)
        vol = volume(ga.best_cell.x, ga.best_cell.y)
        total_vol.append(vol)


    fit_mean = sum(total_fits) / len(total_fits)
    r_mean = sum(total_r) / len(total_r)
    h_mean = sum(total_h) / len(total_h)
    vol_mean = sum(total_vol) / len(total_vol)
    print('|name|stats|')
    print('|-|-|')
    print(f'|Total area mean|{fit_mean}|')
    print(f'|Volume mean|{vol_mean}|')
    print(f'|r mean|{r_mean}|')
    print(f'|h|{h_mean}|')