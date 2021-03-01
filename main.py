from area_generation import generate, show_map, get_distance_matrix
import random
import numpy as np

quantity = int(input('Input quantity of points: '))
max_length = int(input('Input max length between points: '))
iterations = int(input('Input number of iterations: '))

class Map:
    '''
    initialize our optimization system. Ant count is set to points' quantity by default,
    evaporation rate means how fast pheromones evaporate 0<x<1. Less means faster.
    Alpha and beta are coefficients that can change the weights of two key factors:
    alpha is responsible for pheromone, beta is responsible for distance.
    Starting pheromones and pheromones_per_run are pretty straightforward.
    Different problems will require different values for these keys.
    '''
    def __init__(self, ant_count=quantity, evap_rate=0.6, starting_pheromone=0.5, alpha=1, beta=4, pheromones_per_run=100):
        self.nodes = generate(quantity,max_length,max_length)
        self.distances = get_distance_matrix(self.nodes)
        self.pheromones = np.ones((quantity, quantity))*starting_pheromone
        self.evaporation_rate = evap_rate
        self.ant_count = ant_count
        self.alpha = alpha
        self.beta = beta
        self.best_length = 0
        self.phero_per_run = pheromones_per_run

    '''
    After every run-through pheromones evaporate, then most popular edges receive an additional batch of phero
    '''
    def evaporation(self):
        self.pheromones*=self.evaporation_rate
        self.pheromones+=self.pheromones_batch

    '''
    First we initialize phero batch matrix with zeros. Then we unleash ants. After every single ant we're adding
    pheromones they secrete to the batch. When all ants within iteration done running, we start
    the evaportation process.
    '''
    def iteration(self):
        self.pheromones_batch = np.zeros((quantity,quantity))
        for ant in range(self.ant_count):
            self.get_ant_starting_pos()
            self.choose_path()
            pheromones_to_add = self.phero_per_run/self.path_length
            for edge in self.path:
                self.pheromones_batch[edge[0]][edge[1]]+=pheromones_to_add
        self.evaporation()

    '''
    Simple func that gets new position for every ant. Because when all ants start from the same
    position they may not find some good shortcuts even after many iterations.
    '''
    def get_ant_starting_pos(self):
        self.position = random.randint(0, quantity - 1)


    '''
    At the start we initialize movement and path lists. Former will take indexes of points that ant run through,
    latter will take tuples of indexes for paths, this helps us understand where to put pheromones.
    Path_length will calculate overall length for the record.
    We make list of indexes of available nodes and then immediately remove our starting point from it.
    '''
    def choose_path(self):
        self.movement, self.path = [], []
        self.path_length = 0
        available_nodes = list(range(quantity))
        available_nodes.remove(self.position)
        self.movement.append(self.position)
        '''
        While there're still nodes in our list we will calculate probabilities of choosing any available path
        (minus the nodes ant has already visited). It uses standard ant optimization formula that calculates
        probability via pheromones on edges and distance between points.
        Than ant chooses a path using random choice with weights. We update all linked variables.
        '''
        while available_nodes:
            probabilities = []
            denominator = sum((self.pheromones[self.position][i]**self.alpha)*((100/self.distances[self.position][i])**self.beta) for i in available_nodes)
            for node in available_nodes:
                numerator = (self.pheromones[self.position][node]**self.alpha)*((100/self.distances[self.position][node])**self.beta)
                probabilities.append(numerator/denominator)
            choice = random.choices(population=available_nodes, weights=probabilities)[0]
            self.path_length+=self.distances[self.position][choice]
            self.movement.append(choice)
            self.path.append((self.position,choice))
            self.position = choice
            available_nodes.remove(choice)
        '''
        If that's our first run-through or a run became more optimized, we rewrite our data for the record.
        '''
        if not self.best_length or self.path_length<self.best_length:
            self.best_length = self.path_length
            self.best_path = self.movement

x = Map()
for i in range(iterations):
    x.iteration()
print(f'Best path: {x.best_path}')
print(f'Best length: {x.best_length}')
show_map(x.nodes, x.best_path)