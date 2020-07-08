import Graph
import eval
import random as rand
from deap import tools
from deap import base
from deap import creator
import sys

if __name__ == '__main__':
    input_file = str(sys.argv[1])
    p1_index = int(sys.argv[2])
    p2_index = int(sys.argv[3])

    SIZE = int(sys.argv[4])
    GEN_CNT = int(sys.argv[5])

    g = Graph.Graph(SIZE, input_file)
    p1 = Graph.Point(p1_index, rand.random(), rand.random())
    p2 = Graph.Point(p2_index, rand.random(), rand.random())

    active_path = g.get_path(p1.index, p2.index)
    LEAF_SIZE = len(g.leaf_paths())

    creator.create("FitnessMin", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("rand_coord", rand.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.rand_coord, n=LEAF_SIZE * 2)
    toolbox.register("evaluate", eval.evaluate, graph=g)
    toolbox.decorate("evaluate", tools.DeltaPenality(eval.constrain_space, 0))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", eval.mutate, sigma=1, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=50)


    pop = toolbox.population(n=1000)
    crossover_prob = 0.3
    mut_prob = 0.7

    print("Start of evolution")

    fitnesses = list(map(toolbox.evaluate, pop))

    gen = 0

    while gen < GEN_CNT:
        gen = gen + 1

        print("Generation %i:" % gen)

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        #apply crossover and mutation
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if rand.random() < crossover_prob:
                toolbox.mate(child1, child2)

                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            if rand.random() < mut_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        #reevaluate invalid indexes
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("Evaluated %i individuals" % len(invalid_ind))

        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("Min: %s" % min(fits))
        print("Max: %s" % max(fits))
        print("Avg: %s" % mean)
        print("Standard deviation: %s" % std)

    print("END OF EVOLUTION")

    best = tools.selBest(pop, 1)[0]

    print("Best individual is %s %s" % (best, best.fitness.values))
