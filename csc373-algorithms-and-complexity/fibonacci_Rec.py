#Computes fibonacci reciprocal, up to a given integer n.
import sys
lookup = {0: 0}

def fracnum(N,D,R):
    v, d = abs(N), abs(D)
    while R:
        (v, R) = (v*10,R-1) if v < d else ((v%d)*10,R-1)
    return v/d

def rf(n,pos=1):
    if n in lookup:
        return fracnum(1,lookup[n],pos-1)
    if n<=2:
        lookup[n]=1
        return fracnum(1,lookup[n],pos-1)
    else:
        lookup[n] = lookup[n-2]+lookup[n-1]
        return fracnum(1,lookup[n],pos-1)

def generate(n):
    a = list()
    cur_sum = 0
    i=1
    print_count = 1
    while print_count != n+1:
        current = rf(i,print_count)
        if i>6*print_count:
            i = 0
            print(int(cur_sum%10))
            sys.stdout.flush()
            a.append(str(int(cur_sum%10)))
            print_count+=1
            cur_sum=0
        else:
            cur_sum+=current
        i+=1

if __name__=="__main__":
    n = int(sys.argv[1])
    res = generate(n)
