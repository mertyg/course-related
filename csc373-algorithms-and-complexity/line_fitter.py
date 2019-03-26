from scipy.optimize import linprog
import sys

##given a set of points, this program fits a linear line
##s.t. minimizes the maximum absolute error.

def solver(points):
    eq1 = lambda p: [-1,p[0],1]
    eq2 = lambda p: [-1,-p[0],-1]
    c = [1,0,0]
    A = [eq(p) for p in points for eq in (eq1,eq2)]
    b = [p[1]*pow(-1,i) for p in points for i in range(2)]
    res = linprog(c, A_ub=A, b_ub=b)
    return res["x"][1:]

def main():
    words = sys.argv[1]
    dict_file = open(words,"r")
    points = dict_file.readline().strip().split("),")
    points[-1] = points[-1].replace(")","")
    points = [p.replace("(","") for p in points]
    points = [eval(p) for p in points]
    a,b = solver(points)
    print("{},{}".format(a,b))
    return a,b

if __name__ == "__main__":
    main()