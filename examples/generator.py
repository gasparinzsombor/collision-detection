import random
import os

def generate_connected_tree_positive(num_nodes):
    """
    Generate a connected tree structure as a graph with `num_nodes` nodes.
    Ensures nodes are placed on a grid with only positive coordinates.
    """
    coords = [(1, 1)]  # Start with the root node at (1, 1)
    edges = []
    while len(coords) < num_nodes:
        # Choose a random existing node as a parent
        parent = random.choice(coords)
        px, py = parent

        # Generate a random neighbor for the new node with positive coordinates
        possible_neighbors = [(px + dx, py + dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]
                              if px + dx > 0 and py + dy > 0]
        new_neighbors = [n for n in possible_neighbors if n not in coords]

        if not new_neighbors:
            continue  # Skip if no valid neighbors are found (rare edge case)

        new_node = random.choice(new_neighbors)
        coords.append(new_node)
        edges.append((parent, new_node))

    return coords, edges

def generate_operations_with_restrictions_and_bidirectional_consistency(edges, graph_type, cause_collision=True):
    """
    Generate operations for the graph with specific restrictions, balance, and bidirectional consistency:
    If an edge is part of a related_edges list, it must also have its own operation and link back bidirectionally.
    """
    operations = []
    edge_to_operation = {}

    # Filter edges based on type
    vertical_edges = [e for e in edges if e[0][0] == e[1][0]]
    horizontal_edges = [e for e in edges if e[0][1] == e[1][1]]

    if graph_type == 1:  # Vertical connections allowed, standalone horizontal operations possible
        main_edges = vertical_edges
        standalone_edges = horizontal_edges
    elif graph_type == 2:  # Horizontal connections allowed, standalone vertical operations possible
        main_edges = horizontal_edges
        standalone_edges = vertical_edges
    else:  # Mixed connections with no restrictions
        main_edges = edges
        standalone_edges = []

    # Generate connected operations
    for edge in main_edges:
        if edge in edge_to_operation or random.random() > 0.5:  # Not all edges need an operation
            continue

        operation = "expansion" if random.random() > 0.5 else "contraction"
        potential_related = [e for e in main_edges if e not in edge_to_operation and e != edge]

        related_edges = random.sample(potential_related, k=min(2, len(potential_related))) if cause_collision else []

        # Ensure related edges have their own operations
        for related_edge in related_edges:
            if related_edge not in edge_to_operation:
                edge_to_operation[related_edge] = ("expansion" if random.random() > 0.5 else "contraction", [])

        edge_to_operation[edge] = (operation, related_edges)

    # Add standalone operations
    for edge in standalone_edges:
        if edge in edge_to_operation or random.random() > 0.5:
            continue

        operation = "expansion" if random.random() > 0.5 else "contraction"
        edge_to_operation[edge] = (operation, [])

    # Ensure bidirectional consistency for related_edges
    for edge, (operation, related_edges) in edge_to_operation.items():
        for related_edge in related_edges:
            if edge not in edge_to_operation[related_edge][1]:
                edge_to_operation[related_edge][1].append(edge)

    # Convert edge_to_operation back to a consistent operation list
    for edge, (operation, related_edges) in edge_to_operation.items():
        operations.append((edge, operation, related_edges))

    # Ensure at least one operation exists
    if not operations and main_edges:
        operations.append((main_edges[0], "expansion", []))

    return operations

def save_graph_to_file(filepath, coords, edges, operations):
    """Save graph components to a file."""
    with open(filepath, 'w') as file:
        file.write(';'.join(map(str, coords)) + '\n')
        file.write(';'.join(map(str, edges)) + '\n')
        file.write(';'.join([f"{op[0]},'{op[1]}',{op[2]}" for op in operations]) + '\n')

# Parameters for graph generation
node_counts = [5, 12, 20, 30, 40]
base_folder = "./data/generated_graphs"
os.makedirs(base_folder, exist_ok=True)

# Generate graphs with adjusted rules
for graph_type in range(1, 4):  # Three types of graphs
    for idx, num_nodes in enumerate(node_counts):
        # Generate graph components
        coords, edges = generate_connected_tree_positive(num_nodes)
        cause_collision = idx % 2 == 0  # Alternate between causing and not causing collisions
        operations = generate_operations_with_restrictions_and_bidirectional_consistency(edges, graph_type, cause_collision)

        # Save to file
        filename = f"graph_type{graph_type}_size{num_nodes}.txt"
        filepath = os.path.join(base_folder, filename)
        save_graph_to_file(filepath, coords, edges, operations)

print(f"Graphs have been saved to {base_folder}")
