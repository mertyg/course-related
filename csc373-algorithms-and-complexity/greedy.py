

#Interval scheduling problem solution using the greedy algorithm.
# Input is eventlist, consisting of starting and finishing times of each event.
# i.e. [(1,2),(3,5),(1,4)....,(15,34)]


def interval_scheduler(eventlist):
    eventlist = sorted(eventlist,key=lambda x: x[1])
    execution = list()
    while len(eventlist)!=0:
       curr_start,curr_end= eventlist.pop(0)
       execution.append((curr_start,curr_end))
       while( len(eventlist)>0 and eventlist[0][0]<curr_end):
           eventlist.pop(0)
    return execution


#here begins huffman tree implementation

import heapq

class BTNode:
    def __init__(self,val,let):
        self.val = val
        self.letter = let
        self.left = None
        self.right = None

#assuming pairs consist of (frequency,letter) tuples.
testinput = [(5,"a"),(9,"b"),(12,"c"),(13,"d"),(16,"e"),(45,"f")]

def print_tree(root):
    if root:
        print(str(root.val)+" "+root.letter)
        print_tree(root.left)
        print_tree(root.right)

        
#insert encoding algorithm using the huffman tree
def encoding_tree(node,encode_dict,current):
    if node is not None:
        if node.letter!="":
            encode_dict[node.letter]=current
        encoding_tree(node.left,encode_dict,current+"0")
        encoding_tree(node.right,encode_dict,current+"1")

def huffman_tree(pairs):
    for i in range(len(pairs)):
        pairs[i] = (pairs[i][0],BTNode(pairs[i][0],pairs[i][1]))
    heapq.heapify(pairs)
    while(len(pairs)>1):
        freq1, node1 = heapq.heappop(pairs)
        freq2, node2 = heapq.heappop(pairs)
        parent =  BTNode(freq1+freq2,"")
        parent.left = node1
        parent.right = node2
        heapq.heappush(pairs,(freq1+freq2,parent))
    encode_dict = dict()
    encoding_tree(pairs[0][1],encode_dict,"")
    return encode_dict

print("Frequencies and input of huffman encoding algorithm: ")
print(testinput)
print("Encoding, result of the huffman: ")
print(huffman_tree(testinput))



