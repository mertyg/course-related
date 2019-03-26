#solution to the leetcode problem "Insert Delete GetRandom O(1)"
#Design a data structure that supports all following operations in average O(1) time.
#insert(val): Inserts an item val to the set if not already present.
#remove(val): Removes an item val from the set if present.
#getRandom: Returns a random element from current set of elements. Each element #must have the same probability of being returned.

class RandomizedSet:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.values = list()
        self.pos = dict()
        self.size = 0
        
    def insert(self, val):
        """
        Inserts a value to the set. Returns true if the set did not already contain the specified element.
        :type val: int
        :rtype: bool
        """
        if val not in self.pos:
            self.values.append(val)
            self.pos[val] = self.size
            self.size+=1
            return True
        return False
        

    def remove(self, val):
        """
        Removes a value from the set. Returns true if the set contained the specified element.
        :type val: int
        :rtype: bool
        """
        if (val not in self.pos) or self.size==0:
            return False
        current = self.pos[val]
        self.values[current] = self.values[self.size-1]
        self.pos[self.values[current]] = current
        self.values.pop()
        self.size-=1
        del self.pos[val]
        return True

    def getRandom(self):
        """
        Get a random element from the set.
        :rtype: int
        """
        length = len(self.values)
        toreturn = randint(0,length-1)
        return self.values[toreturn]
