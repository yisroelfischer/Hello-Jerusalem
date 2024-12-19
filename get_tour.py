""" 
Return an itinerary consisting of a list of short tours.

Arg:
nodes -- a list of IDs for the attrictions to be visited on the tour
"""
    
# Settings
MAXTOUR = 10 # Max number of nodes per cluster
MAXPATH = 10 # Max weight of edge within cluster


class Node: 
    
    def __init__(self, id, edges):
        self.id = id
        self.in_edges = [edge for edge in edges if edge['end'] == self.id] # Incoming edges
        self.out_edges = [edge for edge in edges if edge['start'] == self.id] # outgoing edges
        
        
        def __eq__(self, other):
            return isinstance(other, Node) and self.id == other.id


class Supernode:
    """ Temporary object representing a group of nodes for use in the algorithm """

    def __init__(self, itinerary, incoming, outgoing):
        self.id = itinerary[0]['start']
        self.itinerary = itinerary
        self.entrance = incoming['end']
        self.exit = outgoing['start']


class Data:
    # Sample edges
    sample_edges = [{'id': (1, 2), 'start': 1, 'end': 2,'weight': 1},
                    {'id': (1, 3), 'start': 1, 'end': 3,'weight': 2},
                    {'id': (2, 1), 'start': 2, 'end': 1,'weight': 3}, 
                    {'id': (2, 3), 'start': 2, 'end': 3,'weight': 4},
                    {'id': (3, 1), 'start': 3, 'end': 1,'weight': 1},
                    {'id': (3, 2), 'start': 3, 'end': 2,'weight': 3}
                   ]

   
def main(nodes):
    edges = Data.sample_edges
    nodes = [Node(site.id, edges) for site in nodes] 
    
    # Get list of nodes sorted by number of edges less than maxpath
    nodes_by_neighbors = []
    for node in nodes:
        connected_nodes = [edge['end'] for edge in node.out_edges 
                           if edge['weight'] <= MAXPATH] 
        nodes_by_neighbors.append({node.id: connected_nodes})
    nodes_by_neighbors.sort(key = lambda x: len(list(x.values())[0]))
    
    # Create clusters of nearby nodes
    clusters = []
    for node in nodes_by_neighbors:
        id = list(node.keys())[0] 
        if not any(id == n.id for cluster in clusters for n in cluster):
            clusters.append(cluster(id, clusters, nodes)) # cluster() returns a list of node objects
    
    # Divide clusters into tours less than maxtour
    for cluster in clusters:
        if len(cluster) > MAXTOUR:
            clusters.extend(divide(cluster))
            clusters.remove(cluster)
    
    # Generate tour of each neighborhood 
    tours = []
    for cluster in clusters:
        tree = spanning_tree(cluster) # Chu-Liu/Edmonds' algorithm
        cluster_tour = get_tour(tree, cluster, edges) # Generate tour starting with root node
        tours.append(cluster_tour)
    itinerary = [[e['id'] for e in tour]for tour in tours]
    
    return itinerary


def cluster(root, clusters, nodes): 
    """ Return a list of all nodes reachable from a given root node using only edges smaller than MAXPATH.

    Positional arguments:
    root -- id of the root node.
    clusters -- list of clusters already created. Each cluster is a list of node objects
    nodes -- list of all node objects in the graph.
    """
    
    # Get starting node
    node = next(n for n in nodes if n.id == root)
    
    # Return empty set if node is already in a cluster
    if any(node in c for c in clusters): 
        return set()
    
    # Initialize new cluster
    new_cluster = {node}  
    
    # Recursively add neighboring nodes
    neighbors = [edge['end'] for edge in node.out_edges]
    for neighbor in neighbors: 
        next_node = next((n for n in nodes if n.id == neighbor), None)
        if not any(next_node in c for c in clusters):
            new_cluster.update(cluster(next_node, clusters, nodes))
    
    return new_cluster        


def divide(cluster, groups=None):     
    """ Divide cluster into largest possible subclusters which are less than maxtour."""
    # Initialize sibling groups
    if not groups:
        # Get list of nodes which don't lead to any others in the cluster
        lowest_nodes = []
        for node in cluster:
            neighbors = [edge['end'] for edge in node.out_edges if edge['weight'] <= MAXPATH]
            if not neighbors:
                lowest_nodes.append(node) 

        # Create a group of any node leading to an end node, along with its children
        for node in cluster:
            new_group = [end_node for end_node in lowest_nodes if edge['end'] == end_node.id for edge in node.out_edges] # Children in end_nodes
            if new_group:
                new_group.insert(0, node)
                groups.append(new_group)

    
    # Delete too-large clusters
    groups = [g for g in groups if len(g) <= MAXTOUR]  
    
    # Recursively combine groups
    recurse = False
    
    for node in cluster:
        parent = next((n for n in cluster if any(n.id == edge['start'] for edge in node.in_edges)), None)
        if not parent: # This is the root node
            continue
        node_group = next((group for group in groups if node in group), None)
        parent_group = next((group for group in groups if parent in group), None)

        if node_group == parent_group:
            continue
        if node_group and not parent_group: 
            node_group.insert(0, parent)
        if parent_group and not node_group:
            parent_group.append(node)
        if node_group and parent_group:
            

                    
    
            
        siblings = [p] +[g for g in groups if g[0].id in p.edges]
        
        for s in siblings:
            combo = [n for n in s]
            if len(combo) > MAXTOUR:
                continue
            groups.append(combo)
            # Remove now-combined groups
            groups = [g for g in groups if not any(g[0].id == c.id for c in combo)] 
            recurse = True
            
    if recurse:
        return divide(cluster, groups)
    
    # Group remaining nodes
    if ungrouped:
        groups.append(ungrouped)
            
    return groups
    

def spanning_tree(cluster):
    """ Chu-Liu/Edmond's algorithm """
    
    tree = []
    visited = [cluster[0].id]
    edges = [e for n in cluster for e in n.edges if any(e.end == o.id for o in cluster[1:])]
    
    # Add smallest incoming edge for each node to tree, skipping the root.
    for node in cluster:
        incoming_edge = sorted([e for e in edges if e['end'] == node.id], 
                               key=lambda x:x['weight'][0])
        tree.append(incoming_edge[0])
        visited.extend(incoming_edge['start'], incoming_edge['end'])
        
    # Condense cycles until none exist 
    starting_edges = [edge for edge in tree if edge['start'] == cluster[0].id]
    for edge in starting_edges:
        while True:
            cycle = get_cycle(tree, tree[0])
            if cycle:
                condense(cycle, tree, visited, edges)
            else:
                break
                    
    # Expand supernodes
    new_tree = [] 
    for edge in tree:
        new_tree.append(edge)
        # Check for supernode
        node = edge['end']
        if isinstance(node, Supernode):
            new_tree.extend(node.itinerary) # Expand supernode
            
    tree = new_tree
        
        # Update edges
    for edge in edges:
        if isinstance(edge['end'], Supernode):
            edge['end'] = edge['end'].entrance
        if isinstance(edge['start'], Supernode):
            edge['start'] = edge['start'].exit           
             
    return tree


def get_cycle(tree, current_edge, stack=None):
    """Uses DFS to find a cycle, returns cycle as list of edges"""
    
    # Initialize stack
    if not stack:
        stack = [current_edge]
        
    for edge in tree:
        if edge['start'] == current_edge['end']: 
            # Check for cycle
            for i, n in enumerate(stack):
                if edge['end'] == n['start'] :
                    # Return cycle
                    return stack[i:] + [edge]
                
            # Recursively add edges
            stack.append(edge)      
            cycle = get_cycle(tree, edge, stack)             
            stack.pop()
            if cycle:
                return cycle 
               
    return None

def condense(cycle, tree, visited, edges):
    """ Condenses cycle into supernode. Returns updated tree and visited list. """
    
    # Gather cycle edges and nodes
    internal, outgoing, incoming, cycle_nodes = [], [], [], []
    
    for edge in edges:
        if edge['start'] in cycle and edge['end'] in cycle:
            internal.append(edge)
            cycle_nodes.append(edge['end'])
        elif edge['start'] in cycle:
            outgoing.append(edge)
        elif edge['end'] in cycle:
            incoming.append(edge)
    
    # Create supernode
    incoming.sort(key=lambda x:x['weight'])
    outgoing.sort(key=lambda x:x['weight'])
    supernode = Supernode(cycle, incoming[0], outgoing[0])
    
    # Update tree and visited list
    for edge in outgoing:
        edge['start'] = supernode
    for edge in incoming:
        edge['end'] = supernode
    
    delete_edges = internal + incoming[1:] + outgoing[1:]
    if delete_edges:
        for edge in delete_edges:
            tree.remove(edge)

    visited = [node for node in visited if node not in cycle_nodes]
    visited.append(supernode)
    
    return tree, visited
    
    
def get_tour(tree, cluster, edges):
    """ Construct tour based on MST, minimizing dead ends """
    nodes = [n.id for n in cluster]
    available_edges = [e for e in edges if e['start'] in nodes 
                       and e['end'] in nodes 
                       and e['weight'] <= MAXPATH]
    end_edges = [e for e in tree if not any(e['end'] == f['start'] for f in tree)] # Dead ends  
        
    # Get outgoing edges from dead ends sorted by weight
    for edge in end_edges:
        out_edges = [e for e in available_edges if edge['end'] == e['start']]                                                         
        if not out_edges:
            continue
        out_edges.sort(key=lambda x:x['weight'])

        # Add to tree
        for e in out_edges:
            current_route = next((x for x in tree if x['end'] == e['end']), None)
            alt_branches = [f for f in tree if f['start'] == current_route['start'] 
                            and f != current_route]
            if alt_branches:
                tree.append(e)
                tree.remove(current_route)

    # Form itinerary
    branches = [[edge] for edge in tree if edge['start'] == nodes[0]]
    while True:
        new_branches = []
        for branch in branches:
            next_edges = [edge for edge in tree if edge['start'] == branch[-1]['end']]
            if next_edges:
                branch.append(next_edges[0])
            if len(next_edges) > 1:
                for edge in next_edges[1:]:
                    new_branches.append(branch + [edge])    
        if not new_branches:
            break              
        
        for branch in new_branches:
            fork = branches.next(lambda x:branch[0] in branches[x])
            i = branches.index(fork)
            branches.insert(i, branch)

    itinerary = [n for branch in branches for n in branch]
    return itinerary

            
test_ = [1, 2, 3, 4]
       
if __name__ == '__main__':
    main(test_)
