from random import randint


#leetcode.com problem with the same name as the function.
#Given a string of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators. The valid operators are +, - and *.
#simple divide and conquer approach.

def operations(ch,a,b):
    if ch=="+": return a+b
    if ch=="-": return a-b
    else: return a*b

def diffWaysToCompute(input):
    """
    :type input: str
    :rtype: List[int]
    """
    res = list()
    ops = ["+","-","*"]
    if input.isdigit():
        temp = int(input)
        return list([temp])
    else:
        for i in range(len(input)):
            if input[i] in ops:
                left = diffWaysToCompute(input[:i])
                right = diffWaysToCompute(input[i+1:])
                for res1 in left:
                    for res2 in right:
                        res.append(operations(input[i],int(res1),int(res2)))
        return list(res)


#another leetcode question
#calculating the majority element(that is occured in a given array more than length/2 times)
#divide and conquer approach

def majorityElement(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    if nums is None:
        return None
    if len(nums)==1:
        return nums[0]
    mid = len(nums)//2
    left = majorityElement(nums[:mid])
    right = majorityElement(nums[mid:])
    return [left,right][nums.count(right)>len(nums)//2]

#divide and conquer algorithm for counting inversions.
#an inversion is defined as:
#i and j are inverted if i < j, but ai > aj
#also known as sort-count.

def count_inversions(arr):
    if len(arr)==1:
        return 0,arr
    size = len(arr)//2
    left, leftarr = self.count_inversions(arr[:size])
    right, rightarr = self.count_inversions(arr[size:])
    merged,mergedarr = self.merge_count(leftarr,rightarr)
    return left+right+merged , mergedarr

def merge_count(left,right):
    count = 0
    lf = 0
    rf = 0
    final = list()
    while lf!=len(left) and rf!=len(right):
        if left[lf]<right[rf]:
            final.append(left[lf])
            lf+=1
        elif right[rf]<left[lf]:
            count+=(len(left)-lf)
            final.append(right[rf])
            rf+=1
    while lf!=len(left):
        final.append(left[lf])
        lf+=1
    while rf!=len(right):
        final.append(right[rf])
        rf+=1
    return count,final


#randomized quicksort algorithm.
#divide and conquer approach, picking the pivot randomly.

def quicksort(arr):
    if len(arr) in list([0,1]):
        return arr
    pivot = randint(0,len(arr)-1)
    smaller = quicksort([item for item in arr if item<arr[pivot]])
    larger = quicksort([item for item in arr if item>arr[pivot]])
    smaller.append(arr[pivot])
    smaller.extend(larger)
    return smaller


#not done
def majority_element_2(arr):
    if len(arr)==1:
        return [(arr[0],1),(0,0)]
    elif len(arr)==2:
        if (arr[0]!=arr[1]):
            return [(arr[0],1),(arr[1],1)]
        return [(arr[0],2),(0,0)]
    mid = len(arr)/2
    left = majority_element_2(arr[:mid])
    right = majority_element_2(arr[mid:])
    return find_help(left,right)


