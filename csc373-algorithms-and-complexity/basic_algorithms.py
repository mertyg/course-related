#workaround for CSC373 - Complexity Design and Analysis of Algorithms

from random import randint

#polynomial time in the order of input size(bits)
def exponentiation(x, y):
    if y == 0 :
        return 1
    z = exponentiation(x,y//2)
    if y%2==0:
        return z*z
    else:
        return x*z*z

#euclidean gcd algorithm
def euclid_gcd(x,y):
    if y==0:
        return x
    return euclid_gcd(y,x%y)

def is_prime(x):
    y = randint(2,x-1)
    return exponentiation(y,x-1)%x==1


#mergesort implementation
def mergesort(arr):
    l = len(arr)
    if l<=1:
        return arr
    print(arr)
    return merge(mergesort(arr[:(l//2)]),mergesort(arr[(l//2):]))


#not completed, fix concatenation
def merge(arr1,arr2):
    print(arr1,arr2)
    if not arr1 or len(arr1)==0:
        return list(arr2)
    if not arr2 or len(arr2)==0:
        return list(arr1)
    if arr1[0]<arr2[0]:
        a = list([arr1[0]])
        return list([arr1[0]]) + merge(arr1[1:],arr2)
    else:
        a = list([arr2[0]])
        return list([arr2[0]]) + merge(arr1,arr2[1:])

#pick the kth smallest element in an array
#randomized divide and conquer algorithm
#worst case O(n^2), avg case O(n)
def selection(arr,k):
    n = randint(0,len(arr)-1)
    smallcount = 0
    eqcount = 0
    small = list()
    large = list()
    eq = list()
    for i in range(len(arr)):
        if arr[i]<arr[n]:
            smallcount+=1
            small.append(arr[i])
        elif arr[i]==arr[n]:
            eqcount+=1
            eq.append(arr[n])
        else:
            large.append(arr[i])

    if k<=smallcount:
        return selection(small,k)
    elif k<=smallcount+eqcount:
        return arr[n]
    else:
        return selection(large,k-smallcount-eqcount)

#prints the number of bits in numbers from 1 to num)
def bit_counts(num):
    toreturn = list()
    toreturn.append(0)
    while(len(toreturn)<num+1):
        toreturn.extend([a+1 for a in toreturn])
        toreturn = toreturn[:num+1]
    return toreturn

#returns the maximum subarray of a given array.
#o(n)
def maxsubarray(nums):
    if len(nums)==0:
        return 0
    if len(nums)==1:
        return nums[0]
    current_sum = 0
    current_max = -2e9
    for i in range(len(nums)):
        current_sum += nums[i]
        if current_sum > current_max:
            current_max = current_sum
        if current_sum<0:
            current_sum = 0
    return current_max


#Searches for a value in an m x n matrix. This matrix has the following properti#es:

#Integers in each row are sorted in ascending from left to right.
#Integers in each column are sorted in ascending from top to bottom.
#This is taken from a problem with the given function's name, from leetcode.
def searchMatrix(self, matrix, target):
    """
    :type matrix: List[List[int]]
    :type target: int
    :rtype: bool
    """
    
    if len(matrix)==0 or len(matrix[0])==0:
        return False
    row = 0
    col = len(matrix[0])-1
    while(1):
        if target==matrix[row][col]:
            return True
        if target>matrix[row][col]:
            if row==len(matrix)-1:
                return False
            row+=1
        else:
            if col==0:
                return False
            col-=1


class TreeNode:
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = None

#solution for leetcode problem "Merge Two Binary Trees"

def mergeTrees(t1, t2):
    """
    :type t1: TreeNode
    :type t2: TreeNode
    :rtype: TreeNode
    """
    if t1 is None and t2 is None:
        return None
    if t1 and (t2 is None):
        return t1
    if t1 is None and t2:
        return t2
    else:
        t1.val += t2.val
        t1.left = mergeTrees(t1.left,t2.left)
        t1.right = mergeTrees(t1.right,t2.right)
    return t1


            
