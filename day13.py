from parse import parse
import numpy as np

"""Button A: X+49, Y+27
Button B: X+35, Y+65
Prize: X=4326, Y=4898
"""

class Grabber:
    def __init__(self):
        self.ax = 0
        self.ay = 0
        self.bx = 0
        self.by = 0
        self.tx = 0
        self.ty = 0

    def GetXYABMatrix(self):
        """
        |Sa|   |Xa Xb|^-1  |Xt|
        |Sb| = |Ya Yb|     |Yt|
        """
        return np.matrix([[self.ax, self.bx], [self.ay, self.by]], dtype=np.int64)
    
    def GetXYTMatrix(self):
        return np.matrix([[self.tx], [self.ty]], dtype=np.int64)
    
    def Solve(self):
        A = self.GetXYABMatrix()
        
        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        # manually calculat determinant
        det = a*d - b*c

        if det == 0:
            return 0
        
        inv = np.matrix([[d, -b], [-c, a]], dtype=np.int64)
        T = self.GetXYTMatrix()

        solution = inv @ T

        solution_valid = (solution % det)
        if not (solution_valid == 0).all():
            return 0
        
        solution = solution // det

        if not np.all(solution >= 0):
            return 0
        
        test = A @ solution
        good = test == T

        assert(good.all())
        costs = solution.T @ np.asarray([3, 1], dtype=np.int64)
        return (costs).sum()



with open("13.txt") as intxt:
    grabbers = []
    for i, line in enumerate(intxt):
        if i % 4 == 0:
            grabbers.append(Grabber())
            xy = parse('Button A: X{}, Y{}', line)
            x, y = [int(x.strip()) for x in xy]
            grabbers[-1].ax = x
            grabbers[-1].ay = y
        if i % 4 == 1:
            xy = parse('Button B: X{}, Y{}', line)
            x, y = [int(x.strip()) for x in xy]
            grabbers[-1].bx = x
            grabbers[-1].by = y
        if i % 4 == 2:
            xy = parse('Prize: X={}, Y={}', line)
            x, y = [int(x.strip()) for x in xy]
            grabbers[-1].tx = x
            grabbers[-1].ty = y

p1 = sum([g.Solve() for g in grabbers])

print(p1)

def ConvertToP2(grabber):
    grabber.tx += 10000000000000
    grabber.ty += 10000000000000
    return grabber

p2 = sum([ConvertToP2(g).Solve() for g in grabbers])
print(p2)