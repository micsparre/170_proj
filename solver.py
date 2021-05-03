import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import random
import numpy

def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities (nodes) to remove
        k: list of edges to remove
    """
    path_score = nx.dijkstra_path_length(G, 0, G.number_of_nodes() - 1)
    if G.number_of_nodes() <= 30:
        path_cost_1, nodes_deleted_1, edges_deleted_1 = solver1(G.copy(), 1, 15)
        path_cost_2, nodes_deleted_2, edges_deleted_2 = solver2(G.copy(), 1, 15)
        path_cost_3, nodes_deleted_3, edges_deleted_3 = solver3(G.copy(), 1, 15)
        path_cost_4, nodes_deleted_4, edges_deleted_4 = solver4(G.copy(), 1, 15)
        # path_cost_5, nodes_deleted_5, edges_deleted_5 = brute_force(G.copy(), 1, 15)
        # distance_1 = calculate_score(G, c, k)
        # distance_2 = calculate_score(G, c, k)
    elif G.number_of_nodes() <= 50:
        path_cost_1, nodes_deleted_1, edges_deleted_1 = solver1(G.copy(), 3, 50)
        path_cost_2, nodes_deleted_2, edges_deleted_2 = solver2(G.copy(), 3, 50)
        path_cost_3, nodes_deleted_3, edges_deleted_3 = solver3(G.copy(), 3, 50)
        path_cost_4, nodes_deleted_4, edges_deleted_4 = solver4(G.copy(), 3, 50)
        # path_cost_5, nodes_deleted_5, edges_deleted_5 = brute_force(G.copy(), 3, 50)
    else:
        path_cost_1, nodes_deleted_1, edges_deleted_1 = solver1(G.copy(), 5, 100)
        path_cost_2, nodes_deleted_2, edges_deleted_2 = solver2(G.copy(), 5, 100)
        path_cost_3, nodes_deleted_3, edges_deleted_3 = solver3(G.copy(), 5, 100)
        path_cost_4, nodes_deleted_4, edges_deleted_4 = solver4(G.copy(), 5, 100)
        # path_cost_5, nodes_deleted_5, edges_deleted_5 = brute_force(G.copy(), 5, 100)
    
    # print("1: ", path_cost_1 - path_score, nodes_deleted_1, edges_deleted_1)
    # print("2: ", path_cost_2 - path_score, nodes_deleted_2, edges_deleted_2)
    # print("3: ", path_cost_3 - path_score, nodes_deleted_3, edges_deleted_3)
    # print("4: ", path_cost_4 - path_score, nodes_deleted_4, edges_deleted_4)

    if (path_cost_1 >= path_cost_2 and path_cost_1 >= path_cost_3 and path_cost_1 >= path_cost_4):
        return nodes_deleted_1, edges_deleted_1
    elif (path_cost_2 >= path_cost_3 and path_cost_2 >= path_cost_4):
        return nodes_deleted_2, edges_deleted_2
    elif (path_cost_3 >= path_cost_4):
        return nodes_deleted_3, edges_deleted_3
    else:
        return nodes_deleted_4, edges_deleted_4


# random
def solver1(G, c, k):
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
    while (c != 0 or k != 0) and timeout < 10000:
        cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")
        flip = random.randint(0, 1)
        if flip == 0 and len(path) > 2 and c > 0:
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

        # print("time: ", timeout)
    # print("nodes to delete: ", nodes_deleted)
    # print("edges to delete: ", edges_deleted)
    # print("new shortest cost: ", nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight"))
    # print("new shortest path: ", nx.dijkstra_path(G, start_node, end_node))
    # print("num nodes deleted: ", len(nodes_deleted))
    # print("num edges deleted: ", len(edges_deleted))
    path_cost = nx.dijkstra_path_length(G, start_node, end_node)
    return path_cost, nodes_deleted, edges_deleted


# delete edges, then nodes
def solver2(G, c, k):
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
    while (c != 0 or k != 0) and timeout < 10000:
        cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")
        if k > 0:
            # delete an edge
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
        elif len(path) == 2 and k == 0:  # s->t is shortest path (so no node deletion)
            break
        if len(path) > 2 and c > 0:
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
        timeout += 1

        # print("time: ", timeout)
    # print("nodes to delete: ", nodes_deleted)
    # print("edges to delete: ", edges_deleted)
    # print("new shortest cost: ", nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight"))
    # print("new shortest path: ", nx.dijkstra_path(G, start_node, end_node))
    # print("num nodes deleted: ", len(nodes_deleted))
    # print("num edges deleted: ", len(edges_deleted))
    path_cost = nx.dijkstra_path_length(G, start_node, end_node)
    return path_cost, nodes_deleted, edges_deleted

# delete nodes then edges
def solver3(G, c, k):
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
    while (c != 0 or k != 0) and timeout < 10000:
        cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")
        if len(path) > 2 and c > 0:
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
        elif k > 0:
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

        # print("time: ", timeout)
    # print("nodes to delete: ", nodes_deleted)
    # print("edges to delete: ", edges_deleted)
    # print("new shortest cost: ", nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight"))
    # print("new shortest path: ", nx.dijkstra_path(G, start_node, end_node))
    # print("num nodes deleted: ", len(nodes_deleted))
    # print("num edges deleted: ", len(edges_deleted))
    path_cost = nx.dijkstra_path_length(G, start_node, end_node)
    return path_cost, nodes_deleted, edges_deleted

# delete everything...
def solver4(G, c, k):
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
    while (c != 0 or k != 0) and timeout < 10000:
        cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")
        # node removal
        node_to_delete = None 
        greatest_cost = cost
        ran_nodes = False
        # edge removal
        edge_to_delete = None
        max_cost = cost
        ran_edges = False        
        if len(path) > 2 and c > 0:
            ran_nodes = True
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
            
        elif len(path) == 2 and k == 0:  # s->t is shortest path (so no node deletion)
            break
        if k > 0:
            #delete an edge
            ran_edges = True
            for j in range(len(path) - 1):
                weight_rm = G.edges[path[j], path[j + 1]]["weight"]
                G.remove_edge(path[j], path[j + 1])
                if nx.is_connected(G):
                    rm_cost = nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight")
                    if rm_cost >= max_cost:
                        max_cost = rm_cost
                        edge_to_delete = (path[j], path[j + 1])
                G.add_edge(path[j], path[j + 1], weight = weight_rm)
            
        if ran_nodes and ran_edges:
            if node_to_delete and edge_to_delete and greatest_cost >= cost and max_cost >= cost:
                if greatest_cost >= max_cost:                
                    G.remove_node(node_to_delete)
                    nodes_deleted.append(node_to_delete)
                    c -= 1
                else:
                    G.remove_edge(edge_to_delete[0], edge_to_delete[1])
                    edges_deleted.append(edge_to_delete)
                    k -= 1
        elif ran_nodes:
            if node_to_delete and greatest_cost >= cost:
                G.remove_node(node_to_delete)
                nodes_deleted.append(node_to_delete)
                c -= 1
        elif ran_edges:
            if edge_to_delete and max_cost >= cost:
                G.remove_edge(edge_to_delete[0], edge_to_delete[1])
                edges_deleted.append(edge_to_delete)
                k -= 1
        timeout += 1

        # print("time: ", timeout)
    # print("nodes to delete: ", nodes_deleted)
    # print("edges to delete: ", edges_deleted)
    # print("new shortest cost: ", nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight"))
    # print("new shortest path: ", nx.dijkstra_path(G, start_node, end_node))
    # print("num nodes deleted: ", len(nodes_deleted))
    # print("num edges deleted: ", len(edges_deleted))
    path_cost = nx.dijkstra_path_length(G, start_node, end_node)
    return path_cost, nodes_deleted, edges_deleted











# solve(read_input_file("inputs/small/small-67.in"))
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
    print(inputs[57:])

    # num = 0
    # for input_path in inputs:
    #     output_path = 'outputs/large/' + basename(normpath(input_path))[:-3] + '.out'
    #     G = read_input_file(input_path)
    #     c, k = solve(G)
    #     assert is_valid_solution(G, c, k)
    #     distance = calculate_score(G, c, k)
    #     write_output_file(G, c, k, output_path)
    #     num += 1
    #     print(num)

    # inputs = glob.glob('inputs/medium/*')
    # num = 0
    # for input_path in inputs:
    #     output_path = 'outputs/medium/' + basename(normpath(input_path))[:-3] + '.out'
    #     G = read_input_file(input_path)
    #     c, k = solve(G)
    #     assert is_valid_solution(G, c, k)
    #     distance = calculate_score(G, c, k)
    #     write_output_file(G, c, k, output_path)
    #     num += 1
    #     print(num)

    # inputs = glob.glob('inputs/small/*')
    # num = 0
    # for input_path in inputs:
    #     output_path = 'outputs/small/' + basename(normpath(input_path))[:-3] + '.out'
    #     G = read_input_file(input_path)
    #     c, k = solve(G)
    #     assert is_valid_solution(G, c, k)
    #     distance = calculate_score(G, c, k)
    #     write_output_file(G, c, k, output_path)
    #     num += 1
    #     print(num)

