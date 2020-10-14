import numpy as np
import random
import argparse
from tqdm import tqdm

number_of_chromosome = 4
max_chromosome = 8192
randomSeed = 18520573


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
    # print(tmp_pop)
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
                rand = np.random.rand()
                # print(j, " ", rand)
                if rand >= 0.5:
                    clone[i][j], clone[i + 1][j] = tmp_pop[i + 1][j], tmp_pop[i][j]
    return clone


def Popop(population, offsprings):
    return np.concatenate([population, offsprings])


# tourament selection
def tournament_selection(populasi, option):
    tmp_pop = populasi.copy()
    np.random.shuffle(tmp_pop)
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
        new_gen1 = tournament_selection(popop, type_of_fitness)
        new_gen2 = tournament_selection(popop, type_of_fitness)
        populasi = np.concatenate([new_gen1, new_gen2])
        global number_of_calling_fitness
        number_of_calling_fitness = number_of_calling_fitness + number_of_chromosome * 8
    return populasi


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-population_size", "--number of parameters", required=True, type=int, help="number of parameters")
    ap.add_argument("-function_type", "--function type", required=True, help="Type of function")
    ap.add_argument("-crossover_type", "--crossover type", required=True, help="Type of crossover")
    args = vars(ap.parse_args())
    population_size = args["number of parameters"]
    fitness_func = args["function type"]
    crossover_type = args["crossover type"]
    f = open('result.txt', 'a')
    f.write('\n- population_size = {}, fitness function: {}, crossover: {}\n'.format(population_size, fitness_func,
                                                                                     crossover_type))
    target = [1] * population_size
    MRPSs = []
    number_of_evaluation = []
    for bisection in range(0, 100, 10):
        print('{}-th bisection'.format(int(bisection / 10) + 1))
        f.write("\t{}-th bisection\n".format(int(bisection / 10) + 1))
        global number_of_calling_fitness
        number_of_calling_fitness = 0
        randomSeed += bisection

        # STAGE 1
        N_upper = 0
        exceed = False
        failures = 0
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
                f.write("\t\t\tN_upper after stage 1: {}\n".format(N_upper))
                break
            number_of_chromosome = number_of_chromosome * 2
            if number_of_chromosome > max_chromosome:
                print("ERROR: CROSS THE LIMIT OF NUMBER OF MAXIMUM CHROMOSOME")
                f.write("\t\t\tN_upper exceed 8192\n")
                exceed = True
                failures += 1
                break

        # STAGE 2
        if exceed:
            continue
        else:
            N_lower = N_upper / 2
            while (N_upper - N_lower) / N_upper > 0.1:
                N = int((N_upper + N_lower) / 2)
                pass_all_seed = True
                for i in range(randomSeed + 0, randomSeed + 10):
                    np.random.seed(i)
                    result = run(N, population_size, crossover_type, fitness_func)
                    if not is_success(result, target):
                        pass_all_seed = False
                        break

                if pass_all_seed:
                    N_upper = N
                else:
                    N_lower = N
                if N_upper - N_lower <= 2:
                    break
        MRPSs.append(N_upper)
        avg_failures = number_of_calling_fitness / (10 - failures)
        number_of_evaluation.append(avg_failures)
        print('MRPS: {}'.format(N_upper))
        f.write("\t\t\tMRPS: {}\n".format(N_upper))
        print('Average number of evaluations: {}'.format(avg_failures))
        f.write("\t\t\tAverage number of evaluations: {}\n".format(avg_failures))

    if len(MRPSs) != 0:
        mean_MRPS = np.mean(MRPSs).round(2)
        print('Mean MRPS: {}'.format(mean_MRPS))
        f.write('\tMean MRPS: {}\n'.format(mean_MRPS))

        std_MRPS = np.std(MRPSs).round(2)
        print('std MRPS: {}'.format(std_MRPS))
        f.write('\tstd MRPS: {}\n'.format(std_MRPS))

        mean_eval = np.mean(number_of_evaluation).round(2)
        print('Mean number of evalution: {}'.format(mean_eval))
        f.write('\tMean number of evalution: {}\n'.format(mean_eval))

        std_eval = np.std(number_of_evaluation).round(2)
        print('std number of evaluations: {}'.format(std_eval))
        f.write('\tstd number of evaluations: {}\n'.format(std_eval))

