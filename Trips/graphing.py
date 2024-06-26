import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt


def stage_one(pois, display=True):
    # Create minimum spanning tree
    G = nx.Graph()
    for poi in pois:
        G.add_node(poi["name"], pos=(poi["point"]["lat"], poi["point"]["lon"]))
    for i in range(len(pois)):
        for j in range(i + 1, len(pois)):
            G.add_edge(
                pois[i]["name"],
                pois[j]["name"],
                weight=ox.distance.great_circle_vec(
                    pois[i]["point"]["lat"],
                    pois[i]["point"]["lon"],
                    pois[j]["point"]["lat"],
                    pois[j]["point"]["lon"],
                ),
            )
    T = nx.minimum_spanning_tree(G)
    pos = nx.get_node_attributes(T, "pos")
    if display:
        nx.draw(T, pos, with_labels=True)
        plt.show()
    return T, pos


def stage_two(T, pos, display=True):
    G = nx.complete_graph(T.nodes)
    for u, v in G.edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        G[u][v]["length"] = ox.distance.great_circle_vec(y1, x1, y2, x2)
    if display:
        nx.draw(G, with_labels=True, font_weight="bold")
        plt.show()
    return G, nx.eulerian_circuit(G)


def stage_three(G, pos):
    tour = list(G.nodes)
    n = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):

                # two current edges from tour
                cur1 = (tour[i], tour[i + 1])
                cur2 = (tour[j], tour[(j + 1) % n])
                cur_length = G.edges[cur1]["length"] + G.edges[cur2]["length"]

                # two 'new' edges for the tour
                new1 = (tour[i], tour[j])
                new2 = (tour[i + 1], tour[(j + 1) % n])
                new_length = G.edges[new1]["length"] + G.edges[new2]["length"]

                # update the tour, if improved
                if new_length < cur_length:
                    # print("swapping edges", cur1, cur2, "with", new1, new2)
                    tour[i + 1 : j + 1] = tour[i + 1 : j + 1][::-1]
                    improved = True

                    # draw the new tour
                    tour_edges = [(tour[i - 1], tour[i]) for i in range(n)]
                    # plt.figure()  # call this to create a new figure, instead of drawing over the previous one(s)
                    # nx.draw(
                    #     G.edge_subgraph(tour_edges),
                    #     pos=pos,
                    #     with_labels=True,
                    #     font_weight="bold",
                    # )
                    # plt.show()
    return tour


def stage_four(G, pos, tour):
    tour_edges = [(tour[i], tour[i+1]) for i in range(len(tour)-1)]
    plt.figure() 
    nx.draw(
        G.edge_subgraph(tour_edges), pos=pos, with_labels=True, font_weight="bold"
    )
    plt.show()


def concat_graph_routes(routes):
    route = list()
    for r in routes:
        route = route[:-1] + r
    return route


def create_and_plot_routes(tour, pos, OX_Graph, distance):
    nodes = []
    for t in tour:
        nodes.append(ox.distance.nearest_nodes(OX_Graph, pos[t][1], pos[t][0]))
    routes = []
    for i in range(len(nodes) - 1):
        route = nx.shortest_path(OX_Graph, nodes[i], nodes[i + 1], weight="length")
        routes.append(route)
    
    base_colors = ["r", "g", "b", "y", "m", "c", "k"]

    colors = [base_colors[i % len(base_colors)] for i in range(len(routes))]
    bbox = ox.utils_geo.bbox_from_point((pos[tour[0]][0], pos[tour[0]][1]), dist=distance)
    fig, ax = ox.plot_graph_routes(
        OX_Graph, routes, route_colors=colors, route_linewidth=6, bbox=bbox, node_size=0
    )


    # route = concat_graph_routes(routes)
    #
    # fig2, ax2 = ox.plot_graph_route(
    #     OX_Graph, route, route_linewidth=6, node_size=0, bbox=bbox
    # )
    #

    return nodes, routes, fig, ax, None, None


def one_big_route_from_routes(routes, OX_Graph):
    route = concat_graph_routes(routes)

    fig, ax = ox.plot_graph_route(
        OX_Graph, route, route_linewidth=6, node_size=0
    )
    plt.show()
    return route

