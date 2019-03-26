import sys
import random



def go_parse(words,sentence):
    query = dict()
    interpret = dict()
    for i in range(len(sentence)+1):
        query[i] = False
        interpret[i] = []
    stop = [-1]
    interpret[-1] = []
    for i in range(1,len(sentence)+1):
        found = False
        for p in range(len(stop)):
            if sentence[stop[len(stop)-1-p]+1:i+1] in words:
                found = True
                interpret[i] = interpret[stop[len(stop)-1-p]] + [sentence[stop[len(stop)-1-p]+1:i+1]]
                stop.append(i)
                break
    return interpret[len(sentence)]


def main():
    words = sys.argv[1]
    dict_file = open(words,"r")
    word_list = dict_file.readline().strip().split(",")
    sentence = dict_file.readline()
    parsed=go_parse(set(word_list),sentence)
    if parsed!=[]:
        for word in parsed[:-1]:
            print(word,end=" ")
        print(parsed[-1],end="")


if __name__ == "__main__":
    main()
