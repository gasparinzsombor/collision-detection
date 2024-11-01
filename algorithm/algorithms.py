from networkx.classes import Graph
from algorithm.Vec import Vec
from algorithm.Node import Node
from algorithm.Vector import Vector
import copy

Edge = tuple[Node, Node]
Operations = dict[
            Edge,
            tuple[str, list[Edge]]
        ]

def do(g: Graph, operations: Operations) -> list[tuple[Node, Node, list[list[tuple[Edge, str]]]]]:
    result: list[tuple[Node, Node, list[list[tuple[Edge, str]]]]] = []

    for node in g.nodes:
        print("=== From node: " + str(node) + " ===")
        result += traverse_from_node(g, node, operations)
        print("===============================")

    #print(result)
    return result

def traverse_from_node(
        graph: Graph,
        v: Node,
        operations: Operations
        # key is the two coord of an edge
        # value is a tuple of type of operation (expansion / contraction) and a list of coupled operations
        # the coupled operations are also part of the operations dict
    ) ->  list[tuple[Node, Node, list[list[tuple[Edge, str]]]]]:

    visited: set[Node] = set()
    stack: list[
        tuple[
            Node, # w: coord of the actual node
            list[Node], # path from v starting point to actual node
            Vec # multiset of vectors on the path from v to actual node
        ]
    ] = [(v, [v], Vec(v,v))]
    interceptions: list[tuple[Node, Node, list[list[tuple[Edge, str]]]]] = []
    while stack:
        (w, path, vec) = stack.pop()
        if w not in visited:
            visited.add(w)

            prev = path[len(path) - 2]
            edge = (prev, w)
            operation = graph.get_edge_data(prev,w)
            if operation is not None and len(operation) != 0:
                op: str = operation['operation']
                parallel_edges: list = list(map(lambda e: (e, ''),operation['parallel_edges']))

                unit_vector = unit_vector_for_movement(op, edge)
                vec.insert_vector(unit_vector, parallel_edges, (edge, op))

            #print(f"node: {w}, edge: {edge}, vec: {vec.get_vectors()}")

            possible_interceptions = check_interception(vec.get_vectors(), len(graph.nodes), v, w, operations, path)
            for unit_vec, edges in possible_interceptions:
                interceptions.append((v,w,edges))

            # add all neighbours to the stack
            if w in graph.nodes:
                for w0 in graph.neighbors(w):
                    if w0 not in visited:
                        new_vec = Vec(v, w0)
                        new_vec.multiset = copy.deepcopy(vec.multiset)
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
                new_vec.multiset = copy.deepcopy(vec.multiset)
                stack.append((new_node, path + [new_node], new_vec))

    return interceptions



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


def check_interception(
        unit_vectors: list[tuple[Vector, list[tuple[Edge, str]]]],
        n: int,
        target_v: Node,
        start_w: Node,
        operations: Operations,
        path: list[Node]) -> list[tuple[Vector, list[list[tuple[Edge, str]]]]]:
    possible_locations = Node.possible_locations(unit_vectors, n, False)
    #print(f"possible movements for {start_w}: {possible_locations}")

    # here we should check if there is any interception with the following parameters:
    # if 2 nodes are intercepting but there is exactly that many contraction operation
    # between the 2 nodes that many nodes is between them, then it means we detect
    # collision between 2 nodes who would end up as 1 node at the end
    # An example is simple with neighbours:
    # if there is a big graph and we check v and w node in the graph who are neighbours
    # and there is a contraction between them: [v] -><- [w]
    # then when we check that whether w's position can intercept with v we will get a
    # result True for this case, but in reality it is not a collision

    # filter out the above mentioned situation
    false_positive_collisions = []
    for possible_location in possible_locations:
        flatten_operations = [operation for ops in possible_location[1] for operation in ops]
        contraction_between_v_w = 0
        for op in flatten_operations:
            if op[1] == 'contraction':
                contraction_between_v_w += 1
            # try:
            #     if operations[op][0] == 'contraction':
            #         contraction_between_v_w += 1
            # except(KeyError):
            #     if operations[op[::-1]][0] == 'contraction':
            #         contraction_between_v_w += 1

        if contraction_between_v_w == len(path) - 1:
            false_positive_collisions.append(possible_location)

    for false_positive_collision in false_positive_collisions:
        possible_locations.remove(false_positive_collision)

    possible_collisions: list[tuple[Vector, list[list[tuple[Edge, str]]]]] = list(filter(lambda possible_loc: start_w.moved_by(possible_loc[0]) == target_v, possible_locations))

    return possible_collisions