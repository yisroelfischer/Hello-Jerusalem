import get_tour

sample_data = [
    # Original example
    {
        'id': 1,
        'nodes': list(range(1, 13)),
        'edges': [
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
    },
    # Simple, fully connected graph
    {
        'id': 2,
        'nodes': [1, 2, 3, 4],
        'edges': [
            {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 10},
            {'id': (1, 3), 'start': 1, 'end': 3, 'weight': 15},
            {'id': (1, 4), 'start': 1, 'end': 4, 'weight': 20},
            {'id': (2, 3), 'start': 2, 'end': 3, 'weight': 25},
            {'id': (2, 4), 'start': 2, 'end': 4, 'weight': 30},
            {'id': (3, 4), 'start': 3, 'end': 4, 'weight': 35},
        ]
    },
    # Sparse graph with isolated nodes
    {
        'id': 3,
        'nodes': [1, 2, 3, 4, 5],
        'edges': [
            {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 10},
            {'id': (2, 3), 'start': 2, 'end': 3, 'weight': 20},
            {'id': (5, 1), 'start': 5, 'end': 1, 'weight': 30},
        ]
    },
    # Disconnected subgraphs
    {
        'id': 4,
        'nodes': [1, 2, 3, 4, 5, 6],
        'edges': [
            {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 5},
            {'id': (2, 3), 'start': 2, 'end': 3, 'weight': 10},
            {'id': (4, 5), 'start': 4, 'end': 5, 'weight': 8},
            {'id': (5, 6), 'start': 5, 'end': 6, 'weight': 12},
        ]
    },
    # Large graph
    {
        'id': 5,
        'nodes': list(range(1, 21)),
        'edges': [
            {'id': (i, i + 1), 'start': i, 'end': i + 1, 'weight': i * 2} for i in range(1, 20)
        ] + [
            {'id': (i, i + 2), 'start': i, 'end': i + 2, 'weight': i * 3} for i in range(1, 19)
        ] + [
            {'id': (1, 20), 'start': 1, 'end': 20, 'weight': 50}
        ]
    },
    # Single-node graph
    {
        'id': 6,
        'nodes': [1],
        'edges': []
    },
    # Fully connected small graph
    {
        'id': 7,
        'nodes': [1, 2, 3],
        'edges': [
            {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 1},
            {'id': (1, 3), 'start': 1, 'end': 3, 'weight': 1},
            {'id': (2, 3), 'start': 2, 'end': 3, 'weight': 1},
        ]
    },
    # Graph with a single edge
    {
        'id': 8,
        'nodes': [1, 2],
        'edges': [
            {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 10}
        ]
    },
    # Complex structure with high variance in weights
    {
        'id': 9,
        'nodes': [1, 2, 3, 4, 5],
        'edges': [
            {'id': (1, 2), 'start': 1, 'end': 2, 'weight': 1},
            {'id': (1, 3), 'start': 1, 'end': 3, 'weight': 50},
            {'id': (2, 4), 'start': 2, 'end': 4, 'weight': 10},
            {'id': (3, 5), 'start': 3, 'end': 5, 'weight': 100},
            {'id': (4, 5), 'start': 4, 'end': 5, 'weight': 5},
        ]
    }
]

for sample in sample_data:
    print(f"Sample {sample['id']}: {get_tour.main(sample['nodes'], sample['edges'])}")
