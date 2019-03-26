##Robust Regression using huber loss

from sklearn.datasets import load_boston
import numpy as np
import matplotlib.pyplot as plt

def huber(x,delta = 2):
    ret = np.where(abs(x)<delta,.5*(x**2),0)
    ret = np.where(abs(x)>delta,delta*(abs(x)-(delta*.5)),ret)
    return ret


def print_losses():
    x = np.linspace(-20,20)
    deltas = [1,3,5]
    for delta in deltas:
        plt.plot(huber(x,delta),label = "Delta: "+str(delta))
        plt.ylabel("Loss")
        plt.legend(loc='center')
    plt.plot((x)**2,label = "Squared Loss")
    plt.legend(loc='center')
    plt.show()


def perform_gradient_descent(iterations=1000,learning_rate=0.00001,delta=1):
    dataset = load_boston()
    X = dataset["data"]
    t = dataset["target"]
    w = np.zeros(X.shape[1])
    b = 0
    
    for i in range(iterations+1):
        y = np.dot(X,w)+b
        print("Iter: ",i,"Current huber cost: ",(1/(X.shape[0]))*np.sum(huber(y-t,delta)))
        print(np.mean(abs(y-t)))
        print("Iter: ",i,"Current squared cost: ",(1/(X.shape[0]))*np.sum((y-t)**2))
        diff = y-t
        dl_dy = np.where(abs(diff)<=delta,diff,0)
        dl_dy = np.where(diff<-delta,-delta,dl_dy)
        dl_dy = np.where(diff>delta,delta,dl_dy)
        dl_dw = X.T.dot(dl_dy)
        grad = (dl_dw)*learning_rate*(1/X.shape[0])
        w = w-grad
        b = b-(np.sum(dl_dy)*(1/X.shape[0]))

def main():
    print_losses()
    perform_gradient_descent(delta=2)

if __name__ == "__main__":
    main()
