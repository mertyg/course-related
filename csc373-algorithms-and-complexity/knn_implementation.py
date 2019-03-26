#very naive K-Nearest Neighbors Algorithm.

import pandas as pd
import os
from sklearn.cross_validation import train_test_split


def split_data(dataname):
    cwd = os.getcwd()
    data_path = cwd+"/input_folder/"+dataname+".csv"
    train_path = cwd+"/input_folder/"+dataname+"_train.csv"
    test_path = cwd+"/input_folder/"+dataname+"_test.csv"
    
    if not os.path.isfile(train_path) or not os.path.isfile(test_path):
        data = pd.read_csv(data_path,header=None)
        x_train,x_test,y_train,y_test= train_test_split(data.iloc[:,:1],data.iloc[:,-1],test_size=0.2)
        pd.concat([x_train,y_train],axis=1).to_csv(train_path)
        pd.concat([x_test,y_test],axis=1).to_csv(test_path)
    

def knn(training_file_path, test_file_path, k=1):
    split_data("iris")
    train = pd.read_csv(training_file_path,header=None)
    test = pd.read_csv(test_file_path,header=None)
    train_target = train.iloc[:,-1]
    train = train.iloc[:,:-1]
    test_target = test.iloc[:,-1]
    test = test.iloc[:,:-1]
    
    test_predictions = list()
    for row in test.iterrows():
        distances = (train - row[1])**2
        distances = distances.sum(axis=1)
        distances = pd.concat([distances,train_target],axis=1)
        distances.sort_values([0], inplace= True)
        prediction = distances.iloc[:k,-1].mode()
        test_predictions.append(prediction[0])
    return (test_predictions==test_target).mean()

cwd = os.getcwd()
dataname = "iris"
train_path = cwd+"/input_folder/"+dataname+"_train.csv"
test_path = cwd+"/input_folder/"+dataname+"_test.csv"
print(knn(train_path,test_path,5))

    
    
