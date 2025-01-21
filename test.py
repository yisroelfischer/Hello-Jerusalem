import get_tour


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

print(f' Tour: {get_tour.main(nodes, sample_edges)}')