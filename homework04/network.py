from api import get_friends
import time
import igraph
from igraph import Graph

def get_network(users_ids, as_edgelist=True):

    friends = get_friends(users_ids)
    edges = []
    matrix = [[0] * len(friends)] * len(friends)

    for user1 in range(len(friends)):
        fr = get_friends(friends[user1]['id'])
        for user2 in range(user1+1, len(friends)):
            if friends[user2] in fr:
                matrix[user2][user1] = 1
                matrix[user1][user2] = 1
                if as_edgelist:
                    edges.append((user1, user2))

        time.sleep(0.34)

    if as_edgelist:
        return edges
    return matrix


def plot_graph(user_id):

    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames]
    edges = get_network(user_id, True)

    g = Graph(vertex_attrs={'shape': 'circle', 'label': vertices, 'size': 10}, edges=edges, directed=False)

    N = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }

    g.simplify(multiple=True, loops=True)

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(g, **visual_style)


if __name__ == '__main__':
    plot_graph(99183468)
