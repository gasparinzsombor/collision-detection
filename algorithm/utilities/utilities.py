class Vec:
    def __init__(self, v, w):
        self.v: tuple[int, int] = v
        self.w: tuple[int, int] = w
        self.multiset: dict[int, tuple[tuple[int,int], int]] = {}

    def insert_vector(self,
                      vector: tuple[int, int],
                      parallel_edges: list[tuple[tuple[int, int], tuple[int, int]]],
                      edge: tuple[tuple[int, int], tuple[int, int]]):
        hash_ = None
        if len(parallel_edges) != 0:
            parallel_edges.append(edge)
            sorted_tuples = [tuple(sorted(t)) for t in parallel_edges]
            sorted_tuple_list = sorted(sorted_tuples)
            hash_ = hash(tuple(sorted_tuple_list))
        if hash_ is not None:
            if self.multiset.__contains__(hash_):
                # one or more operation already in the multiset, we should add those together
                old_vector, multiplicity = self.multiset[hash_]
                self.multiset[hash_] = ((old_vector[0] + vector[0]),(old_vector[1] + vector[1])), multiplicity
            else:
                self.multiset[hash_] = (vector, 1)
        else:
            # there is no relation with other edges
            hash_ = hash(edge)
            if self.multiset.__contains__(hash_):
                new_multiplicity = self.multiset[hash_]
                new_multiplicity[1] = new_multiplicity[1] + 1
                self.multiset[hash_] = new_multiplicity
            else:
                self.multiset[hash_] = (vector, 1)
        # if self.multiset.__contains__(vector):
        #     self.multiset[vector] = self.multiset[vector] + 1
        # else:
        #     self.multiset[vector] = 1

    def get_vectors(self) -> list[tuple[int, int]]:
        vectors: list[tuple[int, int]] = []
        for e in self.multiset:
            entry = self.multiset[e]
            for i in range(0,entry[1]):
                vectors.append(entry[0])

        return vectors