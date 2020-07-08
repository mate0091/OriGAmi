import numpy as np


class Graph:
    def __init__(self, vertices, file):
        self.edges = [[0 for i in range(vertices)] for j in range(vertices)]
        self.vertex_cnt = vertices

        self.read_tree(file)

    def read_tree(self, file):
        with open(file) as f:
            for line in f:
                pair = line.split(' ')
                try:
                    self.edges[int(pair[0])][int(pair[1])] = int(pair[2])
                    self.edges[int(pair[1])][int(pair[0])] = int(pair[2])
                except ValueError:
                    print("File error")
        self.edges = np.array(self.edges, dtype=np.int16)

    def get_edge_length(self, u, v):
        return self.edges[u][v]

    def leaf_vertices(self):
        leaves = []
        for i, j in enumerate(self.edges):
            temp = np.array(j, dtype=np.int16)
            if np.count_nonzero(temp) == 1:
                leaves.append(i)

        return leaves

    def bfs(self, start):
        q = [start]
        visited = set()
        prev = [-1 for i in range(self.vertex_cnt)]

        while q:
            current = q.pop(0)
            if current not in visited:
                visited.add(current)

                adj_list = self.adj(current)

                for i in adj_list:
                    if i not in visited:
                        prev[i] = current

                q.extend(adj_list)

        return prev

    def dist(self, v, u):
        bfs_list = self.bfs(v)
        dist = 0

        current_vertex = u
        prev_vertex = bfs_list[u]

        while current_vertex != -1:
            dist += self.edges[prev_vertex][current_vertex]
            #step up one time
            current_vertex = prev_vertex
            prev_vertex = bfs_list[prev_vertex]

        return dist

    def candidate_axial_creases(self):
        axial_list = []

        vertex_list = self.leaf_vertices()

        for i in vertex_list:
            #investigate each pair

            for j in vertex_list:
                if i < j:
                    axial_list.append((i, j, self.dist(i, j)))

        return axial_list

    def adj(self, vertex):
        adj_list = []
        for i, j in enumerate(self.edges[vertex]):
            if j != 0:
                adj_list.append(i)

        return adj_list

    def get_path(self, u, v):
        bfs_list = self.bfs(u)
        current_vertex = v
        prev_vertex = bfs_list[v]
        path = []

        while current_vertex != u:
            path.append(current_vertex)
            current_vertex = prev_vertex
            prev_vertex = bfs_list[prev_vertex]

        path.append(u)

        return path

    def leaf_paths(self):
        paths = []

        leaves = self.leaf_vertices()

        for i in leaves:
            for j in leaves:
                if i < j:
                    paths.append(self.get_path(i, j))

        return paths

    def __repr__(self):
        return self.edges.__repr__()


class Point:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def __repr__(self):
        string = "{}: {}, {}"
        return string.format(self.index, self.x, self.y)
