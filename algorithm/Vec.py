from algorithm.Node import Node
from algorithm.Vector import Vector

Edge = tuple[Node, Node]

class Vec:
    def __init__(self, v: Node, w: Node):
        self.v: Node = v
        self.w: Node = w
        self.multiset: dict[int, tuple[Vector, list[tuple[Edge, str]]]] = {}
        #                   hash key -> movement vector, multiplicity, list of edges where the operations are
        #                   we need all of these information to be able to get back a schedule when we are detecting a collision

    def insert_vector(self,
                      vector: Vector,
                      parallel_edges: list[tuple[Edge, str]],
                      edge: tuple[Edge, str]):
        hash_ = None
        if len(parallel_edges) != 0:
            parallel_edges.append(edge)
            sorted_tuples = [tuple(sorted(edge)) for edge, op in parallel_edges]
            sorted_tuple_list = sorted(sorted_tuples)
            hash_ = hash(tuple(sorted_tuple_list))
        if hash_ is not None:
            if hash_ in self.multiset:
                # one or more operation already in the multiset, we should add those together
                old_vector, edges = self.multiset[hash_]
                edges.append(edge)
                self.multiset[hash_] = old_vector.add(vector), edges
            else:
                self.multiset[hash_] = (vector, [edge])
        else:
            # there is no relation with other edges
            hash_ = hash(edge)
            self.multiset[hash_] = (vector, [edge])


    def get_vectors(self) -> list[tuple[Vector, list[tuple[Edge, str]]]]:
        vectors: list[tuple[Vector,list[tuple[Edge, str]]]] = []
        for e in self.multiset:
            entry = self.multiset[e]
            vectors.append(entry)

        return vectors