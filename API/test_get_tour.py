from get_tour import Node, Supernode, cluster, divide, spanning_tree, get_cycle, condense, get_tour

nodes = list(range(1,13))
sample_edges = [
    {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 5},
    {'id': (2, 3), 'start': 2, 'end': 3, 'weight': 6},
    {'id': (3, 4), 'start': 3, 'end': 4, 'weight': 7},
    {'id': (4, 5), 'start': 4, 'end': 5, 'weight': 8},
    {'id': (5, 6), 'start': 5, 'end': 6, 'weight': 9},
    {'id': (1, 7), 'start': 1, 'end': 7, 'weight': 5},
    {'id': (7, 8), 'start': 7, 'end': 8, 'weight': 6},
    {'id': (8, 9), 'start': 8, 'end': 9, 'weight': 7},
    {'id': (9, 10), 'start': 9, 'end': 10, 'weight': 10},
    {'id': (2, 11), 'start': 2, 'end': 11, 'weight': 9},
    {'id': (11, 12), 'start': 11, 'end': 12, 'weight': 8}
    ]
sample_cycle = [
    {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 5},
    {'id': (2, 3), 'start': 2, 'end': 3, 'weight': 6},
    {'id': (3, 1), 'start': 3, 'end': 1, 'weight': 7},
]
sample_edges_with_cycle = [
    {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 5},
    {'id': (2, 3), 'start': 2, 'end': 3, 'weight': 6},
    {'id': (3, 1), 'start': 3, 'end': 1, 'weight': 7},
    {'id': (3, 4), 'start': 3, 'end': 4, 'weight': 7},
    {'id': (4, 5), 'start': 4, 'end': 5, 'weight': 8},
    {'id': (5, 6), 'start': 5, 'end': 6, 'weight': 9},
    {'id': (1, 7), 'start': 1, 'end': 7, 'weight': 5},
    {'id': (7, 8), 'start': 7, 'end': 8, 'weight': 6},
    {'id': (8, 9), 'start': 8, 'end': 9, 'weight': 7},
    {'id': (9, 10), 'start': 9, 'end': 10, 'weight': 10},
    {'id': (2, 11), 'start': 2, 'end': 11, 'weight': 9},
    {'id': (11, 12), 'start': 11, 'end': 12, 'weight': 8}
    ]
nodes = [Node(site, sample_edges) for site in nodes]
nodes_by_id = {node.id: node for node in nodes}
cluster_from_1 = {1: set(nodes)}
cluster_from_7 = {7: {nodes_by_id.get(node) for node in [7, 8, 9, 10]}}
cluster_from_2 = {2: {nodes_by_id.get(node) for node in [2, 3, 4, 5, 6, 11, 12]}}
divided_cluster = []

def test_cluster():
    assert cluster(1, [], nodes) == cluster_from_1
    assert cluster(7, [], nodes) == cluster_from_7
    assert cluster(2, [], nodes) == cluster_from_2
    

def test_divide():
    assert divide(cluster_from_1, nodes_by_id) == [
        {1: {nodes_by_id.get(node) for node in [1, 7, 8, 9, 10]}},
        cluster_from_2]


def test_get_cycle():
    assert get_cycle(sample_edges, sample_edges[0]) is None
    assert get_cycle(sample_cycle, sample_cycle[0]) == sample_cycle
    assert get_cycle(sample_edges_with_cycle, sample_edges_with_cycle[0]) == sample_cycle