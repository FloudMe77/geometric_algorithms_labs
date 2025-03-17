from copy import deepcopy
import math
class Point:
    def __init__(self,cords,number=None):
        self.cords = cords
        self.axes = len(self.cords)
        self.number = number

    def __str__(self):
        return f"({self.cords}),{self.number}"
    
    def __repr__(self):
        return self.__str__()

class Rectangle:
    def __init__(self,lower_left,upper_right,list_of_Point=None):
        if list_of_Point:
            self.lower_left, self.upper_right = self.from_Point_list(list_of_Point)
        else:
            self.lower_left = lower_left
            self.upper_right = upper_right

    # def devide_by_two(self, axes, division_line):
    #     ll1 = self.lower_left
    #     ur2 = self.upper_right

    #     ur1_cords = self.upper_right.cords
    #     ur1_cords[axes] = division_line
    #     ur1 = Point(ur1_cords)

    #     ll2_cords = self.lower_left.cords
    #     ll2_cords[axes] = division_line
    #     ll2 = Point(ur1_cords)
        
    #     return Rectangle(ll1,ur1), Rectangle(ll2,ur2)
    
    def from_Point_list(self,list_of_Point):
        lower_left = list(list_of_Point[0].cords)
        upper_right = list(list_of_Point[0].cords)
        for point in list_of_Point[1:]:
            for axis,cord in enumerate(point.cords):
                lower_left[axis] = min(lower_left[axis], cord)
                upper_right[axis] = max(upper_right[axis], cord)
        return Point(lower_left), Point(upper_right)

    def __str__(self):
        return f"(ro jest prostokąt{self.lower_left}),{self.upper_right}"
    
    def __repr__(self):
        return self.__str__()

    def is_intersect(self,other):
        
        p1, p2 = self.lower_left.cords, self.upper_right.cords
        q1, q2 = other.lower_left.cords, other.upper_right.cords

        # Sprawdź brak przecięcia dla każdego wymiaru
        for i in range(len(p1)):  # Zakładamy, że p1, p2, q1, q2 mają ten sam wymiar
            if p2[i] < q1[i] or q2[i] < p1[i]:
                return False  # Prostokąty się nie przecinają
        return True  # Prostokąty się przecinają
    
    def is_contained(self, other):
        """
        Sprawdza, czy other zawiera się w self.
        """
        # R2 = (q1, q2) to prostokąt `other`
        # R1 = (p1, p2) to prostokąt `self`
        p1, p2 = self.lower_left.cords, self.upper_right.cords
        q1, q2 = other.lower_left.cords, other.upper_right.cords

        # Sprawdź zawieranie dla każdego wymiaru
        for i in range(len(p1)):  # Zakładamy, że p1, p2, q1, q2 mają tę samą długość
            if not (p1[i] <= q1[i] <= q2[i] <= p2[i]):
                return False  # R2 nie jest w całości w R1
        return True  # R2 jest w całości w R1
    
    def intersection(self, other):
        p1, p2 = self.lower_left.cords, self.upper_right.cords
        q1, q2 = other.lower_left.cords, other.upper_right.cords
        ll = deepcopy(p1)
        ur = deepcopy(p2)
        for i in range(len(p1)):  # Zakładamy, że p1, p2, q1, q2 mają tę samą długość
            ll[i] = max(ll[i],p1[i],q1[i])
            ur[i] = min(ur[i],p2[i],q2[i])
        return Rectangle(Point(ll),Point(ur))  # R2 jest w całości w R1
    
    def points_in_rectangle(self,points):
        res = []
        for point in points:
            print(point)
            for axes,cord in enumerate(point.cords):
                flag = True
                if not (self.lower_left.cords[axes] <= cord <= self.upper_right.cords[axes]):
                    flag = False
                    break
            if flag:
                res.append(point)
        return res


class KdTreeNode:
    def __init__(self,points,axes,depth,rectangle=None):
        self.axes = axes
        self.depth = depth
        self.points = points
        self.left = None
        self.right = None
        self.rectangle = rectangle
        self.rectangle = Rectangle(None,None,points)
        self.build()

    def build(self):
        if len(self.points)==1: return
        self.points.sort(key = lambda x: x.cords[self.depth])
        print(self.points[math.ceil(len(self.points)/2)].cords[self.depth])
        left_rec, right_rec = self.devide_by_two(self.rectangle, self.depth, self.points[math.ceil(len(self.points)/2)].cords[(self.depth+1)%self.axes])
        self.left = KdTreeNode(deepcopy(self.points[0:math.ceil(len(self.points)/2)]),self.axes, (self.depth+1)%self.axes, left_rec)
        self.right = KdTreeNode(deepcopy(self.points[math.ceil(len(self.points)/2):]),self.axes, (self.depth+1)%self.axes, right_rec )
    
    def print_tree(self):
        print(self.points,self.depth, self.rectangle)
        if self.left:
            self.left.print_tree()
        if self.right:
            self.right.print_tree()

    def devide_by_two(self,rec, axes, division_line):
        ll1 = rec.lower_left
        ur2 = rec.upper_right

        ur1_cords = deepcopy(rec.upper_right.cords)
        ur1_cords[axes] = division_line
        ur1 = Point(ur1_cords)

        ll2_cords = deepcopy(rec.lower_left.cords)
        ll2_cords[axes] = division_line
        ll2 = Point(ur1_cords)
        
        return Rectangle(ll1,ur1), Rectangle(ll2,ur2)
    
    def search(self,region):
        
        if self.left is None and self.right is None: # jesteśmy w liściu
            # print(self.points)
            print(region.points_in_rectangle(self.points),"cos")
            return region.points_in_rectangle(self.points)
        if region.is_contained(self.rectangle):
            print(self.points)
            return self.points
        if region.is_intersect(self.rectangle):
            return self.left.search(region) + self.right.search(region)
        return []
    
class KdTree:
    def __init__(self, points, axes, begining_depth=0):
        points = [Point(point,e+1) for e,point in enumerate(points)]
        print(points)
        self.begining_depth = begining_depth
        self.root = KdTreeNode(points,axes,begining_depth,Rectangle(None,None,points))
        self.axes = axes
        self.points = points
        
    def search(self, region):
        print(region)
        region = self.root.rectangle.intersection(region)
        return self.root.search(region)

    
test = [(-5,1.5),(-3,4),(-2.5,1),(-5,7),(-2,6),(5,0),(0,3),(7,1),(2,7),(3,5)]
a = KdTree(test,2)
print(a.root.print_tree())

print(a.search(Rectangle(Point((0,0)),Point((3,10)))))
# print([12,32]+[53,1])
