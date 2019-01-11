import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

from kristofedes import *

n = 10
pos = np.random.random((n, 2))
a = [[euclidean(u, v) for v in pos] for u in pos]

edges = kristofedes(a)
G = nx.Graph(edges)
nx.draw(G, pos=pos)
plt.show()