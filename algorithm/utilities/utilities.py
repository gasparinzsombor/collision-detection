import networkx
from networkx import Graph
import ast
from algorithm.Node import Node
from algorithm.algorithms import Edge, Operations

def read_from_file(filename: str) -> list[str] | None:
    try:
        with open(filename, 'r') as file:
            content = file.readlines()
            content = [line.strip() for line in content]
            return content
    except FileNotFoundError as ke:
        print(f"Error: file not found {ke}")
    except Exception as e:
        print(f"Error: An error occurred: {e}")

    return None

def parse_graph(filename: str) -> tuple[Graph,Operations]:
    lines = read_from_file(filename)

    if lines is None:
        raise Exception("Couldn't read file")

    nodes_str = lines[0]
    edges_str = lines[1]
    operations_str = lines[2]

    g: Graph = networkx.Graph()

    nodes = parse_nodes(nodes_str)

    for node in nodes:
        g.add_node(node)

    operations = parse_operations(operations_str)
    edges = parse_edges(edges_str)

    for edge in edges:
        start = edge[0]
        end = edge[1]

        if (start, end) in operations or (end,start) in operations:
            g.add_edge(start, end, operation=operations[(start, end)][0], parallel_edges=operations[(start, end)][1])
        else:
            g.add_edge(start, end)

    return g, operations

def parse_nodes(nodes_str: str) -> list[Node]:
    nodes: list[Node] = []
    split_nodes: list[str] = nodes_str.split(";")
    for node_str in split_nodes:
        node_tuple: tuple[int, int] = eval(node_str)
        nodes.append(Node(node_tuple[0],node_tuple[1]))

    return nodes

def parse_edges(edges_str: str) -> list[Edge]:
    edges: list[Edge] = []
    split_edges: list[str] = edges_str.split(";")
    for edge_str in split_edges:
        edge_tuple: Edge = eval(edge_str)
        edges.append(
            (Node(edge_tuple[0][0],edge_tuple[0][1]),
             Node(edge_tuple[1][0],edge_tuple[1][1]))
        )

    return edges

def parse_operations(operations_str: str) -> Operations:
    operations: Operations = {}
    split_operations: list[str] = operations_str.split(";")
    for operation_str in split_operations:
        tuple_operation = ast.literal_eval(operation_str)
        main_edge = (Node(tuple_operation[0][0][0], tuple_operation[0][0][1]), Node(tuple_operation[0][1][0], tuple_operation[0][1][1]))
        parallel_operations = []
        for edge in tuple_operation[2]:
            parallel_operations.append(
                (Node(edge[0][0], edge[0][1]),
                 Node(edge[1][0], edge[1][1]))
            )
        operations[main_edge] = tuple_operation[1], parallel_operations

    return operations