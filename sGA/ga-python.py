import numpy as np
import random
from tqdm import tqdm

population_size = 10
number_of_chromosome = 4
target = [1] * population_size
max_chromosome = 8192
randomSeed = 18520573
best_option = 0

crossover_type = "1X"
fitness_func = "onemax"


# calculate fitness of gen
def calculate_fitness(offspring, option):
    fitness = 0
    if option == "onemax":
        fitness = np.sum(offspring)
    else:
        group = []
        sum = 0
        for i in range(0, int(len(offspring))):  # if len(offspring) == 30 then number of element in each group are 6
            if (i + 1) % (len(offspring) / 5) != 0 and i > 0:
                sum += offspring[i]
            else:
                group.append(sum + offspring[i])
                sum = 0
        for i in range(0, int(len(offspring) / 5)):
            if group[i] < len(offspring) / 5:
                group[i] = len(offspring) / 5 - 1 - group[i]

        for i in range(0, int(len(offspring) / 5)):
            fitness += group[i]
    return fitness


# create population
def create_population(chromosome_size, population):
    populasi = np.random.randint(0, 2, size=(chromosome_size, population))
    return populasi


# crossover
def crossover(populasi, option):
    tmp_pop = populasi.copy()
    np.random.shuffle(tmp_pop)
    clone = []
    if option == "1X":
        for i in range(0, len(tmp_pop), 2):
            swap_point = np.random.randint(0, len(tmp_pop[0]))
            clone.append(np.concatenate([tmp_pop[i][:swap_point], tmp_pop[i + 1][swap_point:]]))
            clone.append(np.concatenate([tmp_pop[i + 1][:swap_point], tmp_pop[i][swap_point:]]))
    else:
        for i in range(0, len(tmp_pop), 2):
            clone.append(tmp_pop[i])
            clone.append(tmp_pop[i + 1])
            for j in range(0, len(tmp_pop[i])):
                rand = random.random()
                if rand >= 0.5:
                    clone[i][j], clone[i + 1][j] = tmp_pop[i + 1][j], tmp_pop[i][j]
    return clone


def Popop(population, offspring):
    return np.concatenate([population, offspring])


# tourament selection
def tournament_selection(populasi, offsprings, option):
    tmp_pop = populasi.copy()
    np.random.shuffle(tmp_pop)
    # tmp_pop = np.concatenate([populasi, offsprings])
    # random.shuffle(tmp_pop)
    new_gen = []
    for i in range(0, len(tmp_pop), 4):
        offspring1 = calculate_fitness(tmp_pop[i], option)
        offspring2 = calculate_fitness(tmp_pop[i + 1], option)
        offspring3 = calculate_fitness(tmp_pop[i + 2], option)
        offspring4 = calculate_fitness(tmp_pop[i + 3], option)
        best_offspring = max(offspring1, offspring2, offspring3, offspring4)
        if best_offspring == offspring1:
            new_gen.append(tmp_pop[i])
        elif best_offspring == offspring2:
            new_gen.append(tmp_pop[i + 1])
        elif best_offspring == offspring3:
            new_gen.append(tmp_pop[i + 2])
        else:
            new_gen.append(tmp_pop[i + 3])
    return new_gen


def check_converged(populasi):
    if np.all(populasi == populasi[0]):
        return True
    else:
        return False


def is_success(populasi, target_string):
    if np.all(populasi == target_string):
        return True
    else:
        return False


def run(chromosome_size, population, type_of_crossover, type_of_fitness):
    populasi = create_population(chromosome_size, population)  # create population
    while True:
        if check_converged(populasi):
            break
        offsprings = crossover(populasi, type_of_crossover)  # 2 types of crossover: UX and 1X
        popop = Popop(populasi, offsprings)
        # print(offsprings)
        # print("-----")
        new_gen1 = tournament_selection(popop, offsprings, type_of_fitness)
        # print(offsprings)
        # print("-------")
        new_gen2 = tournament_selection(popop, offsprings, type_of_fitness)
        populasi = np.concatenate([new_gen1, new_gen2])
        global number_of_calling_fitness
        number_of_calling_fitness = number_of_calling_fitness + number_of_chromosome * 8
    return populasi


if __name__ == "__main__":
    for bisection in range(0, 100, 10):
        print('{}-th bisection'.format(int(bisection / 10) + 1))
        global number_of_calling_fitness
        number_of_calling_fitness = 0
        randomSeed += bisection

        # STAGE 1
        N_upper = 0
        exceed = False
        while True:
            pass_all_seed = True
            for seed in range(randomSeed + 0, randomSeed + 10):
                np.random.seed(seed)
                result = run(number_of_chromosome, population_size, crossover_type, fitness_func)
                if not is_success(result, target):
                    pass_all_seed = False
                    break

            if pass_all_seed:
                print(number_of_chromosome)
                print(number_of_calling_fitness)
                N_upper = number_of_chromosome

                break
            number_of_chromosome = number_of_chromosome * 2
            if number_of_chromosome > max_chromosome:
                print("ERROR: CROSS THE LIMIT OF NUMBER OF MAXIMUM CHROMOSOME")
                exceed = True
                break

    # STAGE 2
    if exceed:
        continue
    else:
        N_lower = N_upper / 2
        while (N_upper - N_lower) / N_upper > 0.1:
            N = int((N_upper + N_lower) / 2)
            past_all_test = True
            for i in range(group + 0, group + 10):
                np.random.seed(i)
                result = Run(N_upper, l, tour_size, type_func, type_cross, k)
                if not is_Success(result):
                    past_all_test = False
                    break

            if past_all_test == True:
                N_upper = N
            else:
                N_lower = N
            if N_upper - N_lower <= 2:
                break