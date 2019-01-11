import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from blossom import *

INF = 10**9


def prima(W):
    n = len(W)
    g = [[] for _ in range(n)]
    used = [False for _ in range(n)]
    min_e = [INF for _ in range(n)]
    pred = [-1 for _ in range(n)]
    min_e[0] = 0
    for _ in range(n):
        v = min((i for i in range(n) if not used[i]), key=lambda i: min_e[i])
        used[v] = True
        if pred[v] != -1:
            g[v].append(pred[v])
            g[pred[v]].append(v)
        for to in range(n):
            if (W[v][to] < min_e[to]):
                min_e[to] = W[v][to]
                pred[to] = v
    return g


def find_euler(g):
    n = len(g)
    g = [[int(bool(x)) for x in row] for row in g]
    deg = [sum(row) for row in g]
    first = 0
    while not deg[first]:
        first += 1
    st = [first]
    res = []
    while st:
        v = st[-1]
        try:
            i = g[v].index(1)
            g[v][i] -= 1
            g[i][v] -= 1
            st.append(i)
        except ValueError:
            res.append(v)
            st.pop()

    return res

def kristofedes(a):
    n = len(a)
    g = prima(a)
    odd_vertices = [i for i in range(n) if len(g[i]) % 2]
    p = blossom(odd_vertices, a)
    new_g = [[0] * n for i in range(n)]
    for i, j in p:
        new_g[i][j] = new_g[j][i] = a[i][j]
    for i in range(n):
        for j in g[i]:
            new_g[i][j] = new_g[j][i] = a[i][j]
    path = find_euler(new_g)
    new_path = []
    path.pop()
    for v in path:
        if v not in new_path:
            new_path.append(v)
        else:
            new_path.remove(v)
    path = new_path
    path.append(path[0])
    edges = [(path[i-1], path[i]) for i in range(len(path))]

    return edges