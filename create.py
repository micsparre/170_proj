import networkx as nx 
import random as rand
import parse


def newGraph(size, path):
    G = nx.Graph()
    for i in range(size):
        G.add_node(i)

    for j in range(size):
        for k in range(j + 1, size):
            G.add_edge(j, k, weight = round(rand.uniform(0.001, 99.999), 3))

    # print(G)
    parse.write_input_file(G, path)

newGraph(100, '/Users/michaelsparre/desktop/cs170/project-sp21-skeleton/input/100.in')

