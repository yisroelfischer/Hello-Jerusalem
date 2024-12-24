""" 
Return an itinerary consisting of a list of short tours.

Arg:
nodes -- a list of IDs for the sites to be visited on the tour
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
    nodes = [Node(site, edges) for site in nodes] 

    # Validate edge format
    keys = ['id', 'start', 'end', 'weight']
    for edge in edges:
        if not isinstance(edge, dict) or not all(key in edge for key in keys):
            print(f'Error: edge {edge} is not formatted correctly')
            return 1
    
    # Get list of nodes sorted by number of edges less than maxpath
    nodes_by_neighbors = []
    for node in nodes:
        connected_nodes = [edge['end'] for edge in node.out_edges 
                           if edge['weight'] <= MAXPATH] 
        nodes_by_neighbors.append((node.id, connected_nodes))
    nodes_by_neighbors.sort(key = lambda x: len(x[1]))
    
    # Create clusters of nearby nodes
    clusters = []
    for node in nodes_by_neighbors:
        id = node[0] 
        if not any(id == n.id for node_cluster in clusters for n in node_cluster):
            clusters.append(cluster(id, clusters, nodes)) # cluster() returns a list of node objects
    
    # Divide clusters into tours less than maxtour
    new_clusters = []
    for node_cluster in clusters:
        if len(node_cluster) > MAXTOUR:
            new_clusters.extend(divide(node_cluster))
        else:
            new_clusters.remove(node_cluster)
    clusters = new_clusters
    
    # Generate tour of each neighborhood 
    tours = []
    for node_cluster in clusters:
        tree = spanning_tree(node_cluster) # Chu-Liu/Edmonds' algorithm
        cluster_tour = get_tour(tree, node_cluster, edges) # Generate tour starting with root node
        tours.append(cluster_tour)
    itinerary = [[e['id'] for e in tour]for tour in tours]
    
    return itinerary


def cluster(root, clusters, nodes): 
    """ Recursively gather neighboring nodes.

    Gather all nodes reachable from a given root node using paths smaller
    than MAXPATH. Return a list of node objects

    Positional arguments:
    root -- id of the root node.
    clusters -- list of clusters already created.
    nodes -- list of all nodes  in the graph.
    """
    
    # Get root node and validate it
    node = next((n for n in nodes if n.id == root), None)
    if node == None:
       raise ValueError('Invalid root node')
    
    # Return empty set if node is already in a cluster
    if any(node in c for c in clusters): 
        return set()
    
    # Initialize new cluster
    new_cluster = {node}  
    
    # Recursively add neighboring nodes
    neighbors = [edge['end'] for edge in node.out_edges]
    for neighbor in neighbors: 
        next_node = next((n for n in nodes if n.id == neighbor), None)
        if next_node == None:
            continue
        if not any(next_node in c for c in clusters) and not next_node in new_cluster:
            new_cluster.update(cluster(next_node, clusters, nodes))
    
    return list(new_cluster)        


def divide(cluster):     
    """ Divide cluster into subclusters. """
    # Create family tree for each node
    all_trees = []
    for node in cluster:
        if any(node in tree for tree in all_trees): # Already part of a tree
            continue
        new_tree = [node]
        while True: # Add all children to tree
            for n in new_tree:
                children = [o for o in cluster if any(edge <= MAXPATH and edge in o.in_edges 
                                                   for edge in n.out_edges )]
            if not children:
                break
            else: 
                new_tree.extend(children)
        # Add to trees if small enough        
        if len(new_tree) <= MAXTOUR:
            all_trees.append(new_tree)

    # Gather largest trees 
    final_trees = []
    all_trees.sort(reverse=True)
    for tree in all_trees:
        if not any(tree[0] in t for t in final_trees):
            final_trees.append(tree)

    # Add unused nodes
    unused = [node for node in cluster if not any(node in tree for tree in final_trees)]
    if unused:
        final_trees.insert(0, unused)

    if any(len(cluster) > MAXTOUR for cluster in final_trees):
        print('Error: could not divide cluster')
        return 2

    return final_trees

def spanning_tree(cluster):
    """ Chu-Liu/Edmond's algorithm """
    
    tree = []
    visited = [cluster[0].id]
    edges = [e for n in cluster for e in n.edges if any(e.end == o.id for o in cluster[1:])]
    
    # Add smallest incoming edge for each node to tree, skipping the root.
    for node in cluster:
        incoming_edge = sorted([e for e in edges if e['end'] == node.id], 
                               key=lambda x:x['weight'])[0]
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
    """Return list of edges forming a cycle if any exist.
    
    Use DFS to recursively add the next edge and check to see if a cycle 
    has been completed.

    Parameters:
    tree --- list of all edges to check
    current_edge --- edge being checked
    stack --- current stack
    """
    
    # Initialize stack
    if not stack:
        stack = [current_edge]
        
    for edge in tree:
        if edge['start'] == current_edge['end']: 
            # Check for completed cycle
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
    """ Condense cycle in spanning tree. 
    
    Called by the spanning_tree function when cycles are detected.
    Return updated tree and visited  lists, with the edges forming the 
    cycle replaced by a supernode object and all incoming and outgoing 
    edges removed except the smallest ones

    Parameters:
    cycle --- list of edges forming a cycle
    tree --- list of edges in the tree
    visited --- list of node objects already visited in spanning_tree
    edges --- list of all edges in graph
    """
    
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
    """ Construct tour based on MST.
     
    Create a tour while attempting to minimize retracing steps by
    replacing forks with alternate paths starting at dead ends. Return
    Return tour as list of edges.
    
    Parameters:
    tree --- list of edges forming MST of cluster
    cluster --- list of node objects to be visited
    edges --- list of all edges in graph
    """

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
            fork = next(b for b in branches if any(b[0]['start'] == n['start'] for n in branch))
            i = branches.index(fork)
            branches.insert(i, branch)

    itinerary = [n for branch in branches for n in branch]
    return itinerary


