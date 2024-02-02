class A:
    __slots__ = ["a", "b", "c"]
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def __eq__(self, other):
        return self.__slots__ == other.__slots__

print(A(1, 2, 3) == A(1, 2, 3))