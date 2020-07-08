import math
from Graph import *
import random


def calc_scale(graph, path, u, v):
    distance = graph.dist(path[0], path[-1])
    point_dist = math.sqrt(((u.x - v.x) * (u.x - v.x)) + ((u.y - v.y) * (u.y - v.y)))

    return point_dist / distance


def constrain_space(individual):
    for p in individual:
        if p < 0 or p > 1:
            return False

    return True


def mutate(individual, sigma, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = random.gauss(individual[i], sigma * individual[i])

    return individual,


def evaluate(individual, graph):
    scale = 999

    #calculate scale of all leaf paths in the graph and select minimum

    leaf_vertexes = graph.leaf_vertices()

    points = list(zip(individual[::2], individual[1:][::2]))

    for i in range(len(leaf_vertexes)):
        #1 2 -> u v
        #path accepts indexes

        u = Point(leaf_vertexes[i], points[i][0], points[i][1])

        for j in range(i + 1, len(leaf_vertexes)):

            v = Point(leaf_vertexes[j], points[j][0], points[j][1])

            path = graph.get_path(u.index, v.index)
            temp_scale = calc_scale(graph, path, u, v)

            if temp_scale < scale:
                scale = temp_scale

    return scale,
