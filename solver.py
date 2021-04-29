import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities (nodes) to remove
        k: list of edges to remove
    """
    if G.number_of_nodes() <= 30:
        return solver(G, 1, 15)
        # return solver(G, 1, 2)
    elif G.number_of_nodes() <= 50:
        return solver(G, 3, 50)
    else:
        return solver(G, 5, 100)

def solver(G, c, k):
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
    # cost, path = nx.single_source_dijkstra(G, start_node, end_node)
    # print(cost)
    # print(path)
    nodes_deleted = [] # list of nodes deleted
    edges_deleted = [] # list of tuples of edges deleted
    timeout = 0
    cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")
    print("original cost: ", cost)
    print("original path: ", path)
    while (c != 0 or k != 0) and timeout < 100:
        cost, path = nx.single_source_dijkstra(G, start_node, target = end_node, weight = "weight")
        # print(cost, len(path))
        if len(path) > 2 and c > 0:
            # delete a node
            # print("first")
            node_to_delete = None
            greatest_cost = cost
            num_can_be_deleted = 0
            for i in range(1, len(path) - 1):
                copy_graph = G.copy()
                rm_node = path[i]
                copy_graph.remove_node(rm_node)
                if nx.is_connected(copy_graph):
                    # print("connected")
                    rm_cost = nx.shortest_path_length(copy_graph, source = start_node, target = end_node, weight = "weight")
                    # print(rm_cost, greatest_cost)
                    if rm_cost > greatest_cost:
                        # print("c comparison")
                        greatest_cost = rm_cost
                        node_to_delete = rm_node
                else:
                    # print("not connected")
                    num_can_be_deleted += 1

            if num_can_be_deleted == len(path) - 2:
                # print("No nodes can be deleted so c = 0")
                c = 0  # change back if future edge deleted ?
            # removes node if improved cost
            if node_to_delete and greatest_cost > cost:
                # print("c removed")
                G.remove_node(node_to_delete)
                nodes_deleted.append(node_to_delete)
                c -= 1

        elif len(path) == 2 and k == 0:  # s->t is shortest path (so no node deletion)
            # print("second")
            break

        elif k > 0:
            #delete an edge
            # print("third")
            max_cost = cost
            edge_to_delete = None
            for j in range(len(path) - 1):
                weight_rm = G.edges[path[j], path[j + 1]]["weight"]
                G.remove_edge(path[j], path[j + 1])
                if nx.is_connected(G):
                    rm_cost = nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight")
                    if rm_cost > max_cost:
                        # print("k comparison")
                        max_cost = rm_cost
                        edge_to_delete = (path[j], path[j + 1])
                        # print("new cost and edge:", max_cost, edge_to_delete)
                G.add_edge(path[j], path[j + 1], weight = weight_rm)
            # removes edge if improved cost
            if edge_to_delete and max_cost > cost:
                # print("k removed")
                G.remove_edge(edge_to_delete[0], edge_to_delete[1])
                edges_deleted.append(edge_to_delete)
                k -= 1

        timeout += 1
        # print("time: ", timeout)
    print("nodes to delete: ", nodes_deleted)
    print("edges to delete: ", edges_deleted)
    print("new shortest cost: ", nx.shortest_path_length(G, source = start_node, target = end_node, weight = "weight"))
    print("new shortest path: ", nx.dijkstra_path(G, start_node, end_node))
    print("num nodes deleted: ", len(nodes_deleted))
    print("num edges deleted: ", len(edges_deleted))
    return nodes_deleted, edges_deleted

# solve(read_input_file("inputs/medium/medium-200.in"))
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
    inputs = glob.glob('inputs/*')
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)





## HW12 prob 4
    # path = nx.dijkstra_path(G, 0, 6)
    # longest_path = 0
    # edge_deleted = []
    # l_path = []
    # for j in range(len(path) - 1):
    #     weight_rm = G.edges[path[j], path[j + 1]]["weight"]
    #     G.remove_edge(path[j], path[j + 1])
    #     path2 = nx.dijkstra_path(G, 0, 6)
    #     for k in range(len(path2) - 1):
    #         weight_rm2 = G.edges[path2[k], path2[k + 1]]["weight"]
    #         G.remove_edge(path2[k], path2[k + 1])
    #         if nx.is_connected(G):
    #             path3 = nx.dijkstra_path(G, 0, 6)
    #             cost = 0
    #             for i in range(len(path3) - 1):
    #                 cost += G.edges[path3[i], path3[i + 1]]["weight"]
    #                 if cost > longest_path:
    #                     longest_path = cost
    #                     edge_deleted = [path[j], path[j + 1]] + [path2[k], path2[k + 1]]
    #                     l_path = path3
    #         G.add_edge(path2[k], path2[k + 1], weight = weight_rm2)
    #     G.add_edge(path[j], path[j + 1], weight = weight_rm)

    # print(longest_path)
    # print(l_path)
    # print(edge_deleted)
