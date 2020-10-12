import numpy as np
import datetime
import random
from tqdm import tqdm


# generate new gen
def create_gen(population_size):
    gen = ""
    for i in range(population_size):
        temp = str(random.randint(0, 1))
        gen += temp
    return gen


# calculate fitness of gen
def calculate_fitness(offstring, option):
    fitness = 0
    if option == "onemax":
        fitness = np.sum(offstring)
    else:
        group = []
        for i in range(0, int(len(offstring)), 5):
            group.append(offstring[i: i+5])

    return fitness


# create population
def create_population(target, max_population, population_size):
    populasi = np.random.randint(0, 2, size=(max_population, population_size))
    return populasi


# selection process
def selection(populasi):
    pop = dict(populasi)
    parent = {}
    for i in range(2):
        gen = max(pop, key=pop.get)
        genfitness = pop[gen]
        parent[gen] = genfitness
        if i == 0:
            del pop[gen]
    return parent


# crossover
def crossover(populasi, option):
    np.random.shuffle(populasi)
    clone = []
    if option == "1X":
        for i in range(0, len(populasi), 2):
            swap_point = np.random.randint(0, len(populasi[0]))
            print("swap point" + str(swap_point))
            clone.append(np.concatenate([populasi[i][:swap_point], populasi[i + 1][swap_point:]]))
            clone.append(np.concatenate([populasi[i + 1][:swap_point], populasi[i][swap_point:]]))
    else:
        for i in range(0, len(populasi), 2):
            clone.append(populasi[i])
            clone.append(populasi[i+1])
            for j in range(0, len(populasi[i])):
                rand = random.random()
                if rand >= 0.5:
                    clone[i][j], clone[i+1][j] = populasi[i+1][j], populasi[i][j]
    return clone


# tourament selection
def tourament_selection(populasi, offstrings):
    concat = np.concatenate([populasi, offstrings])
    random.shuffle(concat)
    for i in range(0, len(concat), 4):


# create new population with new best gen
def regeneration(mutant, populasi):
    for i in range(len(mutant)):
        bad_gen = min(populasi, key=populasi.get)
        del populasi[bad_gen]
    populasi.update(mutant)
    return populasi


# get best gen in a population
def bestgen(parent):
    gen = max(parent, key=parent.get)
    return gen


# get best fitness in a population
def bestfitness(parent):
    fitness = parent[max(parent, key=parent.get)]
    return fitness


# display function
def display(parent):
    timeDiff = datetime.datetime.now() - startTime
    print('{}\t{}%\t{}'.format(bestgen(parent), round(bestfitness(parent), 2), timeDiff))


# main program
target = ''.rjust(40, '1')

max_population = 2

print('Target Word :', target)
print('Max Population :', max_population)

population_size = 6
startTime = datetime.datetime.now()
print('----------------------------------------------')
print('{}\t\t\t\t\t{}\t{}'.format('The Best', 'Fitness', 'Time'))
print('-------------------------------------------------------------------')
populasi = create_population(target, int(max_population), population_size)
offstrings = crossover(populasi, "1X")
tourament_selection(populasi, offstrings)
parent = selection(populasi)
display(parent)
success = False

