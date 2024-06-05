import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
def two_opt(shortest_path, pos):
    for i in range(len(shortest_path)):
        for j in range(i + 1, len(shortest_path)):
            new_path = shortest_path.copy()
            new_path[i:j] = shortest_path[j - 1:i - 1:-1]
            if path_length(new_path, pos) < path_length(shortest_path, pos):
                shortest_path = new_path
    return shortest_path

def path_length(path, pos):
    length = 0
    for i in range(len(path) - 1):
        length += ox.distance.great_circle_vec(pos[path[i]], pos[path[i + 1]])
    return length


def stage_one(pois):
     # Create minimum spanning tree
        G = nx.Graph()
        for poi in pois:
            G.add_node(poi['name'], pos=(poi['point']['lat'], poi['point']['lon']))
        for i in range(len(pois)):
            for j in range(i + 1, len(pois)):
                G.add_edge(pois[i]['name'], pois[j]['name'], weight=ox.distance.great_circle_vec(pois[i]['point']['lat'], pois[i]['point']['lon'], pois[j]['point']['lat'], pois[j]['point']['lon']))
        T = nx.minimum_spanning_tree(G)
        pos = nx.get_node_attributes(T, 'pos')
        nx.draw(T, pos, with_labels=True)
        plt.show()
        return T, pos

def stage_two(T, pos):
     # Find the Eulerian path
    eulerian_path = nx.eulerize(T)
    print(eulerian_path)
    # Display the Eulerian path
    nx.draw(eulerian_path, pos, with_labels=True)
    plt.show()
    return eulerian_path

def stage_three(eulerian_path, pos):
     # Estimate the shortest path
    eulerian_path = nx.DiGraph(eulerian_path)
    shortest_path = nx.shortest_path(eulerian_path, 'Notre-Dame')
    print(shortest_path)

    # Display the shortest path calculated from the Eulerian path
    nx.draw(shortest_path, pos, with_labels=True)
    plt.show()


def stage_four(shortest_path, pos):
    # Optimize the shortest path
    optimized_path = two_opt(shortest_path, pos)
    print(optimized_path)

    # Display the optimized path
    nx.draw(optimized_path, pos, with_labels=True)
    plt.show()
