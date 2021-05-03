# def brute_force(G, c, k, d_nodes, d_edges):
#     start_node = 0
#     end_node = G.number_of_nodes() - 1
#     node_bool = False
#     edge_bool = False
#     greatest_path = -float("inf")
#     greatest_nodes = []
#     greatest_edges = []
    
#     if k == 0 and c == 0:
#         return nx.dijkstra_path_length(G, start_node, end_node), d_nodes, d_edges
    
#     for node in list(G.nodes):
#         if c == 0:
#             break
#         if node == start_node or end_node:
#             continue
#         g_copy = G.copy()
#         g_copy.remove_node(node)
#         if nx.is_connected(g_copy):
#             node_bool = True
#             node_copy = d_nodes.copy()
#             node_copy.append(node)
#             best_path, best_nodes, best_edges = brute_force(g_copy, c - 1, k, node_copy, d_edges.copy())
#             if best_path > greatest_path:
#                 print(best_path)
#                 greatest_path = best_path
#                 greatest_nodes = best_nodes
#                 greatest_edges = best_edges

#     for edge in list(G.edges):
#         if k == 0:
#             break
#         weight_rm = G.edges[edge[0], edge[1]]["weight"]
#         G.remove_edge(edge[0], edge[1])
#         if nx.is_connected(G):
#             edge_bool = True
#             edge_copy = d_edges.copy()
#             edge_copy.append(edge)
#             best_path, best_nodes, best_edges = brute_force(G, c, k - 1, d_nodes.copy(), edge_copy)
#             if best_path > greatest_path:
#                 print(best_path)
#                 greatest_path = best_path
#                 greatest_nodes = best_nodes
#                 greatest_edges = best_edges
#         G.add_edge(edge[0], edge[1], weight = weight_rm)

#     if not node_bool and not edge_bool:
#         return nx.dijkstra_path_length(G, start_node, end_node), d_nodes, d_edges
#     else:
#         return greatest_path, greatest_nodes, greatest_edges

# print(brute_force(read_input_file("input/hw12.in"), 1, 15, [], []))