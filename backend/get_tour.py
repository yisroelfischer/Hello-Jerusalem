""" 
Return an itinerary consisting of a list of short tours.

Arg:
nodes -- a list of IDs for the sites to be visited on the tour
edges -- a list of dicts representing all paths in the database
"""

import math


class Settings:
    MAXTOUR = 10 # Max number of nodes per cluster
    MAXPATH = 37 # Max weight of edge within cluster
    SAMPLE = None # Track test number - delete this


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

   
def main(nodes, edges):
    # Track tests - delete this
    if len(nodes) == 20:
        Settings.SAMPLE = 5

    nodes = [Node(id, edges) for id in nodes]
    nodes_by_id = {node.id: node for node in nodes}

    # Validate edge format
    keys = ['id', 'start', 'end', 'weight']
    for edge in edges:
        if not isinstance(edge, dict) or not all(key in edge for key in keys):
            print(f'Error: edge {edge} is not formatted correctly')
            return 1
    
    # Get list of nodes sorted by number of edges less than MAXPATH.
    nodes_by_neighbors = []
    for node in nodes:
        connected_nodes = [edge['end'] for edge in node.out_edges 
                           if edge['weight'] <= Settings.MAXPATH] 
        nodes_by_neighbors.append((node.id, connected_nodes))
    nodes_by_neighbors.sort(key = lambda x: len(x[1]), reverse=True)

    # Create clusters of nearby nodes
    clusters = []
    clustered = set()
    for node in nodes_by_neighbors:
        root = node[0] 
        if not root in clustered:
            new_cluster = cluster(root, clusters, nodes)
            
            if new_cluster:
                clusters.append(new_cluster)
                clustered.add(new_cluster['root'])
                clustered.update([e['end'] for e in new_cluster['cluster']])
    # Divide clusters into tours less than Settings.MAXTOUR
    new_clusters = []
    for old_cluster in clusters:
        if len(old_cluster['cluster']) > Settings.MAXTOUR:
            new_clusters.extend(divide(old_cluster, nodes_by_id))
        else:
            new_clusters.append(old_cluster)
    clusters = new_clusters
    
    # Generate tour of each neighborhood 
    tours = []
    for c in clusters:
        root_node = nodes_by_id[c['root']]
        nodes = [nodes_by_id[e['end']] for e in c['cluster']]
        if not root_node:
            raise ValueError('empty cluster')
        if not nodes: # Isolated node
            tours.append(c['root'])
        if len(nodes) == 1: # Isolated edge
            tours.append(c['cluster'][0])
        else:           
            node_cluster = {'root': root_node, 'nodes': nodes}                  
            tree = spanning_tree(node_cluster) # Chu-Liu/Edmonds' algorithm
            cluster_tour = get_cluster_tour(tree, node_cluster, edges) # Generate tour starting with root node
            tours.append(cluster_tour)
    itinerary = []
    for tour in tours:
        if isinstance(tour, int): # Isolated node
            itinerary.append(tour)
        if isinstance(tour, list):
            itinerary.extend([e['id'] for e in tour])
    
    return itinerary


def cluster(root, clusters, nodes): 
    """ Gather neighboring nodes.

    Gather all nodes reachable from a given root node using paths smaller
    than MAXPATH. Return a dict with the root and edges as ids

    Positional arguments:
    root -- id of the root node.
    clusters -- list of clusters already created.
    nodes -- list of all nodes  in the graph.
    """
    # Get root node and validate it
    node = next((n for n in nodes if n.id == root), None)
    clustered = {n for cluster in clusters for n in cluster}

    if node is None:
       raise ValueError('Invalid root node')
    if node in clustered:
        return []
    
    cluster = set()
    visited = {node.id}
    children = [edge['end'] for edge in node.out_edges 
                if edge['weight'] <= Settings.MAXPATH and not edge['end'] in clustered]
    while children:
        child = next((n for n in nodes if n == children[0] and n not in cluster), None)
        if child is None:
            return {'root': root, 'cluster': cluster}
        children.remove(child)
        cluster.add(children[0])
        visited.add(child)
        children.extend([edge['end'] for edge in child.out_edges 
                         if edge['weight'] <= Settings.MAXPATH and not edge['end'] in children])

     
    return {'root': root, 'cluster': cluster}

def divide(cluster):     
    """ Divide cluster into subclusters smaller than MAXTOUR. """
    
    new_clusters = []
    
    # Get root node
    root = cluster['root']
    current_node = root
    
    # Traverse cluster 
    visited = {current_node}
    while True:
        children = [edge['end'] for edge in cluster['cluster']
                    if edge['start'] == current_node
                    and edge['weight'] <= Settings.MAXPATH]

        if len(children) == 1: # Not a fork
            visited.add(current_node)
            current_node = children[0]

        elif len(children) == 0: # End of cluster
            # Divide cluster into equal parts if no fork exists
            divisor = math.ceil(len(cluster['cluster']) / Settings.MAXTOUR) # Number of parts
            length = len(cluster['cluster'] // divisor) # Length of each part

            for i in range(divisor):
                j = i * length
                new_clusters.append({'root': cluster['cluster'][j],
                                     'cluster': cluster['cluster'][j:j + length]})
                i += 1

            return new_clusters
        
        else: # Fork found
            break
    
    # Split cluster at fork
    subclusters = []
    for child in children:
        subclusters.append({'root': child, 'cluster': {child}, 'current': [child]})
                   
    clustered = {current_node}
    finished = False

    while not finished:
        finished = True
        for subcluster in subclusters:
            # Get next generation
            next_generation = [edge['end'] for child in subcluster['current']
                                for edge in cluster.values()
                                if edge['start'] == child
                                and edge['weight'] <= Settings.MAXPATH 
                                and not edge['end'] in clustered]
            subcluster['current'] = [child for child in next_generation]
            if subcluster['current']:
                finished = False   
            # Validate and update 
            for child in subcluster['current']:
                if not child:
                    raise  ValueError('child')
                subcluster['cluster'].add(child)
                clustered.add(child.id)
                
    # Add back in visited nodes to smallest cluster
    subclusters.sort(key=lambda x:len(x['cluster']))
    subclusters[0]['root'] = root
    subclusters[0]['cluster'].update(visited)

    for subcluster in subclusters:
        subcluster = {'root': subcluster['root'].id, 'cluster': subcluster['cluster']} # Refactor

        # Rinse and repeat
        if len([n for s in subcluster.values() for n in s]) <= Settings.MAXTOUR:
            new_clusters.append(subcluster)
        else:
            divided = divide(subcluster)
            for c in divided:
                new_clusters.extend(c) 

        
    return new_clusters


def spanning_tree(cluster):
    """ Chu-Liu/Edmond's algorithm """
    root = cluster['root']
    cluster = [n for n in cluster['nodes']] # Convert cluster to list
    if not cluster:
        return root
    tree = []
    visited = [cluster[0].id]
    edges = [e for n in cluster for e in n.out_edges 
             if any(e['end'] == o.id and o.id is not root for o in cluster)]
    
    # Add smallest incoming edge for each node to tree, skipping the root.
    for node in cluster:
        incoming_edges = sorted([e for e in edges if e['end'] == node.id], 
                               key=lambda x:x['weight'])
        if not incoming_edges:
            continue
        incoming_edge = incoming_edges[0]
        tree.append(incoming_edge)
        visited.extend([incoming_edge['start'] + incoming_edge['end']])
        
    # Condense cycles until none exist 
    starting_edges = [edge for edge in tree if edge['start'] == root]
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
    """Return list of edges forming a cycle if any exist in the given tree."""
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
    
    
def get_cluster_tour(tree, cluster, edges):
    """ Construct tour based on MST.
     
    Create a tour while attempting to minimize retracing steps by
    replacing forks with alternate paths starting at dead ends.
    Return tour as list of edges or a single node id
    
    Parameters:
    tree --- list of edges forming MST of cluster
    cluster --- list of node objects to be visited
    edges --- list of all edges in graph
    """
    root = cluster['root']
    cluster = {n for n in cluster['nodes']} # Convert cluster to set
    #print(f'tree:{[e['id'] for e in tree]}\ncluster: {[n.id for n in cluster]}')
    nodes = {n.id for n in cluster}
    if isinstance(tree, Node): # Isolated node
        return tree
    available_edges = [e for e in edges if e['start'] in nodes 
                       and e['end'] in nodes 
                       and e['weight'] <= Settings.MAXPATH]
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
            if current_route is None:
                continue
            alt_branches = [f for f in tree if f['start'] == current_route['start'] 
                            and f != current_route]
            if alt_branches:
                tree.append(e)
                tree.remove(current_route)

    # Form itinerary
    visited = set()
    branches = [[edge] for edge in tree if edge['start'] == root]
    visited.update([e['start'] for b in branches for e in b] + [e['end'] for b in branches for e in b])
    finished = False

    # Begin adding edges to branches, adding branching paths to new_branches
    while not finished: 
        finished = True

        for branch in branches:
            next_edges = [edge for edge in tree if edge['start'] == branch[-1]['end']]
            if next_edges:
                finished = False
                branch.append(next_edges[0])
                visited.add(next_edges[0]['end'])
            if len(next_edges) > 1:
                for edge in next_edges[1:]:
                    branches.append([edge]) 
                    visited.add(edge['end'])
            if visited == nodes:
                finished = True
            
    # Sort branches so the tour retraces the smallest number of steps first
    itinerary = branches[0] # Trunk
    branches.pop(0)

    while True:
        branches_from_itinerary = [b for b in branches 
                                   if any(b[0]['start'] == e['start'] for e in itinerary)]
        if not branches_from_itinerary:
            break
        for edge in reversed(itinerary):
            last_branch = next((b for b in branches_from_itinerary
                                if b[0]['start'] == edge['start']), None)
            if last_branch:
                break
        itinerary.extend(last_branch)
        branches.remove(last_branch)
            


    return itinerary


