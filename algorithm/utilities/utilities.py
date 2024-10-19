class Vec:
    def __init__(self, v, w):
        self.v: tuple[int, int] = v
        self.w: tuple[int, int] = w
        self.multiset: dict[tuple[int,int], int] = {}

    def insert_vector(self, vector: tuple[int, int]):
        if self.multiset.__contains__(vector):
            self.multiset[vector] = self.multiset[vector] + 1
        else:
            self.multiset[vector] = 1

    def get_vectors(self) -> list[tuple[int, int]]:
        vectors: list[tuple[int, int]] = []
        for e in self.multiset:
            for i in range(0,self.multiset[e]):
                vectors.append(e)

        return vectors