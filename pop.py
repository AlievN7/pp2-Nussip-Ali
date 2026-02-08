class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    def show(self):
        return self.x, self.y
    def dist(self, other):
        return (((other.x - self.x)**2 + (other.y - self.y)**2)**0.5)
    
x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
x3, y3 = map(int, input().split())
n1 = Point(x1, y1)
print(n1.show())
n2 = Point(x2, y2)
print(n2.show())
n1.move(n2.x, n2.y)
n3 = Point(x3, y3)
print(f"{n2.dist(n3):.2f}")