import numpy as np
import datetime
import random
from tqdm import tqdm

# calculate fitness of gen
def calculate_fitness(offstring, option):
    fitness = 0
    if option == "onemax":
        fitness = np.sum(offstring)
    else:
        group = []
        sum = 0
        for i in range(0, int(len(offstring))):
            if (i + 1) % 5 != 0 and i > 0:
                sum += offstring[i]
            else:
                group.append(sum)
                sum = 0
        for i in range(0, 5):
            if group[i] == 5:
                group[i] = 5
            else:
                group[i] = 4 - group[i]
        for i in range(0, 5):
            fitness += group[i]
    return fitness


# create population
def create_population(target, max_population, population_size):
    populasi = np.random.randint(0, 2, size=(max_population, population_size))
    return populasi


# crossover
def crossover(populasi, option):
    np.random.shuffle(populasi)
    clone = []
    if option == "1X":
        for i in range(0, len(populasi), 2):
            swap_point = np.random.randint(0, len(populasi[0]))
            clone.append(np.concatenate([populasi[i][:swap_point], populasi[i + 1][swap_point:]]))
            clone.append(np.concatenate([populasi[i + 1][:swap_point], populasi[i][swap_point:]]))
    else:
        for i in range(0, len(populasi), 2):
            clone.append(populasi[i])
            clone.append(populasi[i + 1])
            for j in range(0, len(populasi[i])):
                rand = random.random()
                if rand >= 0.5:
                    clone[i][j], clone[i + 1][j] = populasi[i + 1][j], populasi[i][j]
    return clone


# tourament selection
def tourament_selection(populasi, offstrings, option):
    concat = np.concatenate([populasi, offstrings])
    random.shuffle(concat)
    new_gen = []
    for i in range(0, len(concat), 4):
        print(i)
        offstring1 = calculate_fitness(concat[i], option)
        offstring2 = calculate_fitness(concat[i + 1], option)
        offstring3 = calculate_fitness(concat[i + 2], option)
        offstring4 = calculate_fitness(concat[i + 3], option)
        best_offstring = max(offstring1, offstring2, offstring3, offstring4)
        if best_offstring == offstring1:
            new_gen.append(concat[i])
        elif best_offstring == offstring2:
            new_gen.append(concat[i + 1])
        elif best_offstring == offstring3:
            new_gen.append(concat[i + 2])
        else:
            new_gen.append(concat[i + 3])
    return new_gen

def check_converged(populasi):



# main program
target = ''.rjust(40, '1') # 1111...1111
max_population = 4
population_size = 6
success = False
populasi = create_population(target, max_population, population_size)
while not success:
    if check_converged(populasi):
        success = True
    offstrings = crossover(populasi, "1X")
    new_gen1 = tourament_selection(populasi, offstrings, "onemax")
    new_gen2 = tourament_selection(populasi, offstrings, "onemax")
    populasi = np.concatenate([new_gen1, new_gen2])

