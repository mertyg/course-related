from collections import Counter
from math import log
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

#only for visualization
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus


def splitting_function(dataset, labels, ratio_train=0.7, ratio_test=0.15):
    size = len(dataset)
    labels = np.asarray(labels)
    random_index = np.random.permutation(len(dataset))
    training_idx = random_index[:int(ratio_train*size)]
    val_idx = random_index[int(ratio_train*size):int((1-ratio_test)*size)]
    test_idx = random_index[int((1-ratio_test))*size:]
    X_train, X_val, X_test = dataset[training_idx], dataset[val_idx], dataset[test_idx]
    y_train, y_val, y_test = labels[training_idx], labels[val_idx], labels[test_idx]

    return X_train, X_val, X_test, y_train, y_val, y_test

def load_data():
    #load the data
    real_raw = open("clean_real.txt", "r")
    real_raw = real_raw.readlines()
    fake_raw = open("clean_fake.txt", "r")
    fake_raw = fake_raw.readlines()
    
    #add target label
    fake_label = ["fake" for raw in fake_raw]
    real_label = ["real" for raw in real_raw]
    
    #combine fake and real data
    all_raw = fake_raw+real_raw
    all_label = fake_label + real_label
    
    #call tokenizer
    tokenizer = CountVectorizer()
    processed_data = tokenizer.fit_transform(all_raw).toarray()
    
    #split into training, validation and test datasets, returning with tokenizer
    X_train, X_val, X_test, y_train, y_val, y_test = splitting_function(processed_data,all_label)

    return X_train, X_val, X_test, y_train, y_val, y_test , tokenizer

def select_model(train,val,y_train,y_val,depth_start=1,depth_count=20, by = 3):
    """
    train : training data; val = validation data; y_train,y_val: training and validation labels
    depth_start: Max_depth starting number/5 ; depth_count : how many depths to try out.
    by : depth incrementer.
    """
    
    results = dict()
    max_accuracy = 0
    
    for depth in range(depth_start,depth_count):
        for criterion in ["gini","entropy"]:
            classifier = DecisionTreeClassifier(max_depth=depth*by,criterion=criterion)
            classifier.fit(train,y_train)
            prediction = classifier.predict(val)
            result = (prediction==y_val).mean()
            results[(criterion,depth*by)] = result
            if result>max_accuracy:
                best_criterion = criterion
                best_depth = depth
                best_classifier = classifier
                max_accuracy = result
            
    
    for key, value in sorted(results.items(), key = lambda x: x[1]):
        print("Criterion: "+key[0]+".\t Max_Depth: "+str(key[1])+".\t Accuracy: "+ str(value))
    

    return best_criterion, best_depth, best_classifier

def entropy(counts):
    all_entropy = 0
    all_count = sum(counts.values())
    for key,value in counts.items():
        px = value/all_count
        logpx = log(px,2)
        all_entropy -= px*logpx
    return all_entropy

def compute_information_gain(features, train, y_train, word):
    counts = Counter(y_train)
    word = features.index(word)
    all_entropy = entropy(counts)
    after_split = 0
    
    exists = Counter()
    dne = Counter()
    
    for i in range(len(train)):
        if train[i][word]>0:
            if y_train[i]=="real": exists["real"]+=1
            else: exists["fake"]+=1
        else:
            if y_train[i]=="real": dne["real"]+=1
            else: dne["fake"]+=1
    
    p_exists = sum(exists.values())/len(y_train)
    p_dne = 1-p_exists
    after_split += p_exists*entropy(exists)
    after_split += p_dne*entropy(dne)
    
    return all_entropy-after_split


#execution

train, val, test, y_train, y_val, y_test, tokenizer = load_data()
best_criterion, best_depth, best_classifier = select_model(train,val,y_train,y_val,1,10,5)


#Visualization 

vizdata = StringIO()

export_graphviz(best_classifier, out_file=vizdata,  
                filled=True, rounded=True,
                special_characters=True, max_depth=2, feature_names = tokenizer.get_feature_names())

graph = pydotplus.graph_from_dot_data(vizdata.getvalue())  
Image(graph.create_png())

#information gain computation
words = ["the","trumps","hillary","gofundme","trump","what"]

for word in words:
    print("Using " + word +" Info Gain: "+ str(compute_information_gain(tokenizer.get_feature_names(), train,y_train,word)))
