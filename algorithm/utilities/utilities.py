from Node import Node
from Vector import Vector

Edge = tuple[Node, Node]

class Vec:
    def __init__(self, v: Node, w: Node):
        self.v: Node = v
        self.w: Node = w
        self.multiset: dict[int, tuple[Vector, int]] = {}

    def insert_vector(self,
                      vector: Vector,
                      parallel_edges: list[Edge],
                      edge: Edge):
        hash_ = None
        if len(parallel_edges) != 0:
            parallel_edges.append(edge)
            sorted_tuples = [tuple(sorted(t)) for t in parallel_edges]
            sorted_tuple_list = sorted(sorted_tuples)
            hash_ = hash(tuple(sorted_tuple_list))
        if hash_ is not None:
            if hash_ in self.multiset:
                # one or more operation already in the multiset, we should add those together
                old_vector, multiplicity = self.multiset[hash_]
                self.multiset[hash_] = old_vector.add(vector), multiplicity
            else:
                self.multiset[hash_] = (vector, 1)
        else:
            # there is no relation with other edges
            hash_ = hash(edge)
            if hash_ in self.multiset:
                new_multiplicity = self.multiset[hash_]
                new_multiplicity[1] = new_multiplicity[1] + 1
                self.multiset[hash_] = new_multiplicity
            else:
                self.multiset[hash_] = (vector, 1)
        # if self.multiset.__contains__(vector):
        #     self.multiset[vector] = self.multiset[vector] + 1
        # else:
        #     self.multiset[vector] = 1

    def get_vectors(self) -> list[Vector]:
        vectors: list[Vector] = []
        for e in self.multiset:
            entry = self.multiset[e]
            for i in range(0,entry[1]):
                vectors.append(entry[0])

        return vectors