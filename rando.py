import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import random
import numpy

import multiprocessing as mp

def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities (nodes) to remove
        k: list of edges to remove
    """
    path_score = nx.dijkstra_path_length(G, 0, G.number_of_nodes() - 1)

    best_cost_1 = -float('inf')
    best_nodes_1 = []
    best_edges_1 = []
    best_cost_2 = -float('inf')
    best_nodes_2 = []
    best_edges_2 = []
    best_cost_3 = -float('inf')
    best_nodes_3 = []
    best_edges_3 = []
    best_cost_4 = -float('inf')
    best_nodes_4 = []
    best_edges_4 = []

    for i in range(2):
        if G.number_of_nodes() <= 30:
            q = mp.Queue()
            p1 = mp.Process(target=solver1, args=(G.copy(), 1, 15, q, ))
            p2 = mp.Process(target=solver1, args=(G.copy(), 1, 15, q, ))
            p3 = mp.Process(target=solver1, args=(G.copy(), 1, 15, q, ))
            p4 = mp.Process(target=solver1, args=(G.copy(), 1, 15, q, ))
            p1.start()
            p2.start()
            p3.start()
            p4.start() 

            p1.join()
            p2.join()
            p3.join()
            p4.join()

            path_cost_1, nodes_deleted_1, edges_deleted_1 = q.get()
            path_cost_2, nodes_deleted_2, edges_deleted_2 = q.get()
            path_cost_3, nodes_deleted_3, edges_deleted_3 = q.get()
            path_cost_4, nodes_deleted_4, edges_deleted_4 = q.get()
        elif G.number_of_nodes() <= 50:

            q = mp.Queue()
            p1 = mp.Process(target=solver1, args=(G.copy(), 3, 50, q, ))
            p2 = mp.Process(target=solver1, args=(G.copy(), 3, 50, q, ))
            p3 = mp.Process(target=solver1, args=(G.copy(), 3, 50, q, ))
            p4 = mp.Process(target=solver1, args=(G.copy(), 3, 50, q, ))
            p1.start()
            p2.start()
            p3.start()
            p4.start() 

            p1.join()
            p2.join()
            p3.join()
            p4.join()

            path_cost_1, nodes_deleted_1, edges_deleted_1 = q.get()
            path_cost_2, nodes_deleted_2, edges_deleted_2 = q.get()
            path_cost_3, nodes_deleted_3, edges_deleted_3 = q.get()
            path_cost_4, nodes_deleted_4, edges_deleted_4 = q.get()
        else:

            q = mp.Queue()
            p1 = mp.Process(target=solver1, args=(G.copy(), 5, 100, q, ))
            p2 = mp.Process(target=solver1, args=(G.copy(), 5, 100, q, ))
            p3 = mp.Process(target=solver1, args=(G.copy(), 5, 100, q, ))
            p4 = mp.Process(target=solver1, args=(G.copy(), 5, 100, q, ))
            p1.start()
            p2.start()
            p3.start()
            p4.start() 

            p1.join()
            p2.join()
            p3.join()
            p4.join()

            path_cost_1, nodes_deleted_1, edges_deleted_1 = q.get()
            path_cost_2, nodes_deleted_2, edges_deleted_2 = q.get()
            path_cost_3, nodes_deleted_3, edges_deleted_3 = q.get()
            path_cost_4, nodes_deleted_4, edges_deleted_4 = q.get()

        if path_cost_1 > best_cost_1:
            best_cost_1 = path_cost_1
            best_edges_1 = edges_deleted_1
            best_nodes_1 = nodes_deleted_1

        if path_cost_2 > best_cost_2:
            best_cost_2 = path_cost_2
            best_edges_2 = edges_deleted_2
            best_nodes_2 = nodes_deleted_2

        if path_cost_3 > best_cost_3:
            best_cost_3 = path_cost_3
            best_edges_3 = edges_deleted_3
            best_nodes_3 = nodes_deleted_3

        if path_cost_4 > best_cost_4:
            best_cost_4 = path_cost_4
            best_edges_4 = edges_deleted_4
            best_nodes_4 = nodes_deleted_4
    
        print(1 + 4*i, ": ", path_cost_1 - path_score)
        print(2 + 4*i, ": ", path_cost_2 - path_score)
        print(3 + 4*i, ": ", path_cost_3 - path_score)
        print(4 + 4*i, ": ", path_cost_4 - path_score)

    if (best_cost_1 >= best_cost_2 and best_cost_1 >= best_cost_3 and best_cost_1 >= best_cost_4):
        return best_nodes_1, best_edges_1
    elif (best_cost_2 >= best_cost_3 and best_cost_2 >= best_cost_4):
        return best_nodes_2, best_edges_2
    elif (best_cost_3 >= best_cost_4):
        return best_nodes_3, best_edges_3
    else:
        return best_nodes_4, best_edges_4


# random
def solver1(G, c, k, q):
    """
    Args:
        G: networkx.Graph
        c: budget for cities/nodes you can remove
        k: budget for paths/edges you can remove
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    start_node = 0
    end_node = G.number_of_nodes() - 1
    nodes_deleted = [] # list of nodes deleted
    edges_deleted = [] # list of tuples of edges deleted
    timeout = 0
    cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")

    c_plus_k = c + k
    while (c != 0 or k != 0) and timeout < 10000:
        cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")
        flip = random.random()
        if flip < c_plus_k and len(path) > 2 and c > 0:
            node_to_delete = None
            greatest_cost = cost
            num_can_be_deleted = 0
            for i in range(1, len(path) - 1):
                copy_graph = G.copy()
                rm_node = path[i]
                copy_graph.remove_node(rm_node)
                if nx.is_connected(copy_graph):
                    rm_cost = nx.shortest_path_length(copy_graph, source = start_node, target = end_node, weight = "weight")
                    if rm_cost >= greatest_cost:
                        greatest_cost = rm_cost
                        node_to_delete = rm_node
                else:
                    num_can_be_deleted += 1

            if num_can_be_deleted == len(path) - 2:
                c = 0  # change back if future edge deleted ?
            # removes node if improved cost
            if node_to_delete and greatest_cost >= cost:
                G.remove_node(node_to_delete)
                nodes_deleted.append(node_to_delete)
                c -= 1
        elif len(path) == 2 and k == 0:  # s->t is shortest path (so no node deletion)
            break
        elif flip == 1 and k > 0:
            #delete an edge
            max_cost = cost
            edge_to_delete = None
            for j in range(len(path) - 1):
                weight_rm = G.edges[path[j], path[j + 1]]["weight"]
                G.remove_edge(path[j], path[j + 1])
                if nx.is_connected(G):
                    rm_cost = nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight")
                    if rm_cost >= max_cost:
                        max_cost = rm_cost
                        edge_to_delete = (path[j], path[j + 1])
                G.add_edge(path[j], path[j + 1], weight = weight_rm)
            if edge_to_delete and max_cost >= cost:
                G.remove_edge(edge_to_delete[0], edge_to_delete[1])
                edges_deleted.append(edge_to_delete)
                k -= 1
        timeout += 1
    path_cost = nx.dijkstra_path_length(G, start_node, end_node)
    q.put((path_cost, nodes_deleted, edges_deleted))










# if __name__ == "__main__":
#     G = read_input_file("inputs/large/large-138.in")
#     c, k = solve(G)
#     print(is_valid_solution(G, c, k))
#     print(calculate_score(G, c, k))
# solve(read_input_file("input/hw12.in"))

# NetworkX useful functions:
    # nx.average_shortest_path_length(G, weight=None, method=None) -> Returns the average shortest path length.
    # nx.is_connected(G) -> Returns true if the graph is connected.
    # Graph.remove_edge(u, v)



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/large/*')
    num = 0
    for input_path in inputs:
        output_path = 'outputs/large/' + basename(normpath(input_path))[:-3] + '.out'
        print("input path:", input_path, "num:", num)
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
        num += 1
        

    inputs = glob.glob('inputs/medium/*')
    num = 0
    for input_path in inputs:
        output_path = 'outputs/medium/' + basename(normpath(input_path))[:-3] + '.out'
        print("input path:", input_path, "num:", num)
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
        num += 1

    inputs = glob.glob('inputs/small/*')
    num = 0
    for input_path in inputs:
        output_path = 'outputs/small/' + basename(normpath(input_path))[:-3] + '.out'
        print("input path:", input_path, "num:", num)
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
        num += 1

