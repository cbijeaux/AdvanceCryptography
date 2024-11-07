from RSA import RSA
import math
class EllipticCurve:
    def __init__(self,p,a,b):
        self._p=p
        self._a=a
        self._b=b
    def isOnCurve(self,x,y):
        return (y**2)%self._p==((x**3)+(self._a)*x+self._b)%self._p
    def findIntersection(self, point1: tuple[int, int], point2: tuple[int, int]=None)->tuple[int,int]:
        inverse=RSA.euclidian.extendedEuclidean(point2[0]-point1[0],self._p)
        difference=(inverse*(point2[1]-point1[1]))%self._p
        xr=((difference**2)-point1[0]-point2[0])%self._p
        yr=((difference)*(point1[0]-xr)-point1[1])%self._p
        return (xr,yr)
    def addPoint(self,point1, point2):
            if point1 is None: 
                return point2
            if point2 is None: 
                return point1
            (x1, y1) = point1
            (x2, y2) = point2
            
            if point1 == point2:
                if y1 == 0:
                    return None  # Point at infinity
                slope = (3 * x1**2 + self._a) * RSA.euclidian.extendedEuclidean(2 * y1, self._p) % self._p
            else:
                if x1 == x2:
                    return None  # Point at infinity
                slope = (y2 - y1) * RSA.euclidian.extendedEuclidean(x2 - x1, self._p) % self._p
            
            x3 = (slope**2 - x1 - x2) % self._p
            y3 = (slope * (x1 - x3) - y1) % self._p
            return (x3, y3)
    def isGenerator(self, point: tuple[int, int]) -> bool:
        notfinished = True
        current = point
        visited_points = {point}
        
        while notfinished:
            current = self.addPoint(current, point)  # Add the point to itself
            if current is None:  # Reached the point at infinity
                notfinished = False
            if current in visited_points:  # Cycle detected
                return False
            visited_points.add(current)
        print(visited_points)
        return len(visited_points) == self._p
    def scalarMultiplication(self,point:tuple[int,int])->tuple[int,int]:
        pass
    def findAllPoints(self):
        points = []
        for x in range(self._p):
            rhs = (x**3 + self._a * x + self._b) % self._p
            for y in range(self._p):
                if (y**2) % self._p == rhs:
                    points.append((x, y))
        points.append("O")
        return points
    def resetValues(self,p,a,b):
        self._p=p
        self._a=a
        self._b=b
ell=EllipticCurve(3,1,1)
print(ell.isGenerator((0,2)))
