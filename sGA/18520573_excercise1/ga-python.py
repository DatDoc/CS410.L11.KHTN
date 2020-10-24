import numpy as np
import argparse


# calculate fitness of gen
def calculate_fitness(offspring, option):
    fitness = 0
    if option == "onemax":
        fitness = np.sum(offspring)
    elif option == "trap":
        if len(offspring) % 5 != 0:
            print("ERROR: CHROMOSOME SIZE IS NOT DIVISIBLE BY 5")
        else:
            sum_of_each_group = 0
            for i in range(0, int(len(offspring))):
                # if len(offspring) == 30 then there are 6 groups
                if (i + 1) % 5 != 0:
                    sum_of_each_group += offspring[i]
                else:
                    sum_of_each_group += offspring[i]
                    if sum_of_each_group == 5:
                        fitness += sum_of_each_group
                    else:
                        fitness += 5 - sum_of_each_group - 1
                    sum_of_each_group = 0  # then set the sum to 0 continue the operation
    return fitness


# create population
def create_population(population_len, chromosome_len):
    population = np.random.randint(2, size=(population_len, chromosome_len))
    return population


# crossover
def crossover(population, option):
    tmp_pop = population.copy()
    np.random.shuffle(tmp_pop)
    clone = []
    if option == "1X":
        for pos in range(0, len(tmp_pop), 2):
            swap_pos = np.random.randint(0, len(tmp_pop[0]))
            clone.append(np.concatenate([tmp_pop[pos][:swap_pos], tmp_pop[pos + 1][swap_pos:]]))
            clone.append(np.concatenate([tmp_pop[pos + 1][:swap_pos], tmp_pop[pos][swap_pos:]]))
    elif option == "UX":
        for i in range(0, len(tmp_pop), 2):
            clone.append(tmp_pop[i])
            clone.append(tmp_pop[i + 1])
            for j in range(0, len(tmp_pop[i])):
                rand = np.random.rand()
                if rand >= 0.5:
                    clone[i][j], clone[i + 1][j] = tmp_pop[i + 1][j], tmp_pop[i][j]
    return clone


def Popop(population, babies):
    return np.concatenate([population, babies])


# tournament selection
def tournament_selection(population, option):
    tmp_pop = population.copy()
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


def check_converged(population):  # check whether the population converged to the same string
    if np.all(population == population[0]):
        return True
    else:
        return False


def is_success(population, target_string):  # check whether the whole population is converged to 1
    if np.all(population == target_string):
        return True
    else:
        return False


def run(population_len, chromosome_len, type_of_crossover, type_of_fitness):
    population = create_population(population_len, chromosome_len)  # create population
    while True:
        if check_converged(population):
            break
        offsprings = crossover(population, type_of_crossover)  # 2 types of crossover: UX and 1X
        popop = Popop(population, offsprings)
        new_gen = np.concatenate([tournament_selection(popop, type_of_fitness),
                                  tournament_selection(popop, type_of_fitness)])
        population = new_gen
        global number_of_calling_fitness
        # number_of_calling_fitness : number of time calling fitness function
        number_of_calling_fitness = number_of_calling_fitness + population_size * 4
    return population


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-chromosome_size", "--number of chromosome", required=True, type=int, help="number of chromosome")
    ap.add_argument("-fitness_type", "--fitness type", required=True, help="Type of fitness function")
    ap.add_argument("-crossover_type", "--crossover type", required=True, help="Type of crossover")
    ap.add_argument("-path", "--save path", required=True, help="Save result to path")
    args = vars(ap.parse_args())
    chromosome_size = args["number of chromosome"]
    fitness_type = args["fitness type"]
    crossover_type = args["crossover type"]
    path = args["save path"]
    f = open(path, 'a')
    f.write('\n- chromosome_size = {}, fitness function: {}, crossover: {}\n'.format(chromosome_size, fitness_type,
                                                                                     crossover_type))
    max_population = 8192
    randomSeed = 18520573
    #  chromosome_size: number of gene
    #  population_size: number of chromosome
    #  max_population: maximum number of a population
    #  randomSeed: generate different population each loop
    target = [1] * chromosome_size  # define the target to be an array full of 1
    MRPSs = []
    number_of_evaluation = []
    for bisection in range(0, 100, 10):  # each bisection run 10 randomSeed
        print('{}-th bisection'.format(int(bisection / 10) + 1))
        f.write("\t{}-th bisection\n".format(int(bisection / 10) + 1))
        number_of_calling_fitness = 0
        randomSeed += bisection
        population_size = 4

        # STAGE 1: find upper bound
        N_upper = 0
        exceed = False
        failures = 0
        while True:
            pass_all_seed = True
            for seed in range(randomSeed + 0, randomSeed + 10):
                np.random.seed(seed)
                result = run(population_size, chromosome_size, crossover_type, fitness_type)
                if not is_success(result, target):
                    pass_all_seed = False
                    break

            if pass_all_seed:
                print(population_size)
                print(number_of_calling_fitness)
                N_upper = population_size
                f.write("\t\t\tN_upper after stage 1: {}\n".format(N_upper))
                break
            population_size = population_size * 2
            if population_size > max_population:
                print("ERROR: CROSS THE LIMIT OF NUMBER OF MAXIMUM POPULATION")
                f.write("\t\t\tN_upper exceed 8192\n")
                exceed = True
                failures += 1
                break

        # STAGE 2: find MRPS
        if exceed:
            continue
        else:
            N_lower = N_upper / 2
            while (N_upper - N_lower) / N_upper > 0.1:
                N = int((N_upper + N_lower) / 2)
                pass_all_seed = True
                for i in range(randomSeed + 0, randomSeed + 10):
                    np.random.seed(i)
                    result = run(N, chromosome_size, crossover_type, fitness_type)
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

