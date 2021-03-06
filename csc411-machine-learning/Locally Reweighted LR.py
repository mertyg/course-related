# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 20:39:09 2017

"""
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_boston
from scipy.special import logsumexp

np.random.seed(0)

# load boston housing prices dataset
boston = load_boston()
x = boston['data']
N = x.shape[0]
x = np.concatenate((np.ones((506, 1)), x), axis=1)  # add constant one feature - no bias needed
d = x.shape[1]
y = boston['target']

idx = np.random.permutation(range(N))


# helper function
def l2(A, B):
    '''
    Input: A is a Nxd matrix
           B is a Mxd matirx
    Output: dist is a NxM matrix where dist[i,j] is the square norm between A[i,:] and B[j,:]
    i.e. dist[i,j] = ||A[i,:]-B[j,:]||^2
    '''
    A_norm = (A ** 2).sum(axis=1).reshape(A.shape[0], 1)
    B_norm = (B ** 2).sum(axis=1).reshape(1, B.shape[0])
    dist = A_norm + B_norm - 2 * A.dot(B.transpose())
    return dist


# to implement
def LRLS(test_datum, x_train, y_train, tau, lam=1e-5):
    '''
    Input: test_datum is a dx1 test vector
           x_train is the N_train x d design matrix
           y_train is the N_train x 1 targets vector
           tau is the local reweighting parameter
           lam is the regularization parameter
    output is y_hat the prediction on test_datum
    '''
    test_datum = test_datum.reshape(1,test_datum.shape[0])
    a = np.exp(-l2(test_datum,x_train)/(2*(tau**2)))/np.exp(logsumexp(-l2(test_datum,x_train)/(2*(tau**2))))
    a = np.diagflat(a)
    w = np.linalg.solve(x_train.T.dot(a).dot(x_train)+lam*np.eye(x_train.shape[1]),x_train.T.dot(a).dot(y_train))
    y_hat = test_datum.dot(w)

    return y_hat
    ## TODO


def run_validation(x, y, taus, val_frac):
    '''
    Input: x is the N x d design matrix
           y is the N x 1 targets vector
           taus is a vector of tau values to evaluate
           val_frac is the fraction of examples to use as validation data
    output is
           a vector of training losses, one for each tau value
           a vector of validation losses, one for each tau value
    '''
    ## TODO
    size = len(x)
    random_index = np.random.permutation(size)
    training_idx = random_index[:int((1-val_frac) * size)]
    val_idx = random_index[int((1-val_frac) * size):]
    x_train,y_train = x[training_idx],y[training_idx]
    x_val, y_val = x[val_idx],y[val_idx]
    training_losses = list()
    val_losses = list()

    for i in range(len(taus)):
        loscur = 0
        valcur = 0
        for j in range(len(x_train)):
            pred_train = LRLS(x_train[j],x_train,y_train,taus[i])
            loscur+=(pred_train-y_train[j])**2
        for j in range(len(x_val)):
            pred_val = LRLS(x_val[j], x_train, y_train, taus[i])
            valcur += (pred_val - y_val[j]) ** 2
        training_losses.append(loscur)
        val_losses.append(valcur)
    return training_losses,val_losses
    ## TODO


if __name__ == "__main__":
    # In this excersice we fixed lambda (hard coded to 1e-5) and only set tau value. Feel free to play with lambda as well if you wish
    taus = np.logspace(1.0, 3, 200)
    train_losses, test_losses = run_validation(x, y, taus, val_frac=0.3)
    plt.semilogx(train_losses,label = "Training Losses")
    plt.semilogx(test_losses, label = "Validation Losses")
    plt.legend(loc='upper left')
    plt.show()

