from RSA import RSA
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
    def findOtherPoint(self,point1:tuple[int,int]):
        pass
    def resetValues(self,p,a,b):
        self._p=p
        self._a=a
        self._b=b
ell=EllipticCurve(23,1,1)
print(ell.isOnCurve(3,10))