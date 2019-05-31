class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    # multiple a constant
    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    # divide a constant
    def __truediv__(self, other):
        return Point(self.x / other, self.y / other, self.z / other)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    def module2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def module(self):
        return self.module2() ** 0.5

    def unit(self):
        return self / self.module()

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def mul(self, other):
        return Point(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def dist2(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def dist(self, other):
        return self.dist2(other) ** 0.5
