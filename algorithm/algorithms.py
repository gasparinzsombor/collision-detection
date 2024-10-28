from webbrowser import Opera
from networkx.classes import Graph
from utilities.utilities import Vec
from Node import Node
from Vector import Vector

Edge = tuple[Node, Node]
Operations = dict[
            Edge,
            tuple[str, list[Edge]]
        ]

def traverse_from_node(
        graph: Graph,
        v: Node,
        operations: Operations
        # key is the two coord of an edge
        # value is a tuple of type of operation (expansion / contraction) and a list of coupled operations
        # the coupled operations are also part of the operations dict
    ):

    visited: set[Node] = set()
    stack: list[
        tuple[
            Node, # w: coord of the actual node
            list[Node], # path from v starting point to actual node
            Vec # multiset of vectors on the path from v to actual node
        ]
    ] = [(v, [v], Vec(v,v))]
    while stack:
        (w, path, vec) = stack.pop()
        if w not in visited:
            visited.add(w)

            prev = path[len(path) - 2]
            edge = (prev, w)
            operation = graph.get_edge_data(prev,w)
            if operation is not None and len(operation) != 0:
                op: str = operation['operation']
                parallel_edges: list = operation['parallel_edges']
                unit_vector = unit_vector_for_movement(op, edge)
                vec.insert_vector(unit_vector, parallel_edges, edge)
                #print(f"node: {w} operation: {operation} on edge {edge}")
            #else:
                #print(f"node: {w} no operation on edge {edge}")

            print(f"node: {w}, edge: {edge}, vec: {vec.get_vectors()}")

            if check_interception(vec.get_vectors(), len(graph.nodes), v, w):
                print(f"Collision detected between {v} and {w}")
            else:
                print(f"No collision between {v} and {w}")

            # add all neighbours to the stack
            if w in graph.nodes:
                for w0 in graph.neighbors(w):
                    if w0 not in visited:
                        new_vec = Vec(v, w0)
                        new_vec.multiset = vec.multiset.copy()
                        stack.append((w0, path + [w0], new_vec))

            # there is a possibility of creating a new node with expansion, in this case we have to add that node
            # to the stack and traverse that coordinate as well
            maybe_new_node = get_op_potential_new_node(w, operations, graph.nodes)
            if maybe_new_node is not None:
                if maybe_new_node.get("edge")[0] in graph.nodes:
                    new_node: Node = maybe_new_node.get("edge")[1]
                else:
                    new_node: Node = maybe_new_node.get("edge")[0]
                new_vec = Vec(v, new_node)
                new_vec.multiset = vec.multiset.copy()
                stack.append((new_node, path + [new_node], new_vec))



def get_op_potential_new_node(w: Node, operations: Operations, nodes) -> dict[str, str | list[Edge] | Edge] | None:
    for edge, op_info in operations.items():
        if w in edge and (edge[0] not in nodes or edge[1] not in nodes):
            return {'operation': f'{op_info[0]}', 'parallel_edges': op_info[1], 'edge': edge}

    return None

def determine_edge_orientation(edge: Edge):
    node1, node2 = edge

    if node1.y == node2.y:
        return "horizontal"  # The edge is horizontal if the y-coordinates are the same
    else:
        return "vertical"  # The edge is vertical if the x-coordinates are the same


def unit_vector_for_movement(operation: str, edge: Edge):
    # Determine if the edge is horizontal or vertical
    edge_orientation = determine_edge_orientation(edge)

    if edge_orientation == "horizontal":
        # if we step from right to left:
        # edge = (prev, w)
        if edge[0].x > edge[1].x:
            if operation == "contraction":
                return Vector(1, 0)
            else:
                return Vector(-1, 0)

        # we step from left to right:
        else:
            if operation == "contraction":
                return Vector(-1, 0)
            else:
                return Vector(1, 0)
    else: # vertical edge
        # if we step from down to up
        # edge = (prev, w)
        if edge[0].y < edge[1].y:
            if operation == "contraction":
                return Vector(0, -1)
            else:
                return Vector(0, 1)

        # we step from up to down
        else:
            if operation == "contraction":
                return Vector(0, 1)
            else:
                return Vector(0, -1)


def check_interception(unit_vectors: list[tuple[Vector, list[Edge]]], n: int, target_v: Node, start_w: Node) -> bool:
    possible_locations = Node.possible_locations(unit_vectors, n)
    print(f"possible movements for {start_w}: {possible_locations}")

    return any(start_w.moved_by(loc) == target_v for loc,edges in possible_locations)