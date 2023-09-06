class Error(Exception):
    pass

class Checknegative(Error):
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.c = c
        self.b = b
        if a < 0:
            self.status = ", сторона a отрицательная"
        elif b < 0:
            self.status = ", сторона b отрицательная"
        elif c < 0:
            self.status = ", сторона c отрицательная"

    def __str__(self):
        return f"Треугольника с отрицательными сторонами не существует{self.status}"

class Triangle:
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
        if self.a < 0 or self.b < 0 or self.c < 0:
            raise Checknegative(self.a, b, c)
       

    def total(self):
        if self.a != self.b and self.a != self.c and self.b != self.c:
            return f"Треугольник разносторонний"
        elif self.a == self.b or self.a == self.c or self.b == self.c:
            return f"Треугольник равнобедренный"


test = Triangle(-3, 2, 4)
print(test.total())