import numpy as np
from matplotlib.pyplot import *

#Implentation of a basic optimal policy finder by using value iteration method.
#Uses Belman Optimality Operator to evaluate the optimal policy.

P = np.array([[[0.,1.],[0.,1.]],[[1.,0.],[1.,0.]]])
R = np.array([[-1.,1.],[0.,5.]])


def value_iteration(P, R, gamma, iterations=1000):
    iterations = min(iterations,(20./(1-gamma)))
    actions_no, states_no = np.shape(P)[0:2]
    Q = np.zeros((states_no,actions_no))
    for i in range(int(iterations)):
        Q_new = Q
        for s in range(states_no):
            for a in range(actions_no):
                value_next = 0
                for s_next in range(states_no):
                    value_next += P[a,s,s_next]*max(Q[s_next])
                Q_new[s,a] = R[s,a] + gamma*value_next
    return Q

Q=value_iteration(P,R,.9)
print(Q)
print("Optimal Policy:",[np.argmax(Q[0]),np.argmax(Q[1])])

gammas = np.linspace(0,0.99,100)
Q_res = []
Policy_res = []
V_res = []
for gamma in gammas:
    Q = value_iteration(P,R,gamma)
    policy = [np.argmax(Q[0]),np.argmax(Q[1])]
    V = np.max(Q,axis=1)
    Q_res.append(Q*(1. - gamma))
    V_res.append(V*(1. - gamma))
    Policy_res.append(policy)

subplot(1,2,1)
plot(gammas, np.array(Policy_res)[:,0],'o')
xlabel('$\gamma$')
ylabel('Policy at state $s_1$')
ylim((-0.05,1.05))
subplot(1,2,2)
plot(gammas, np.array(Policy_res)[:,1],'o')
ylim((-0.05,1.05))
xlabel('$\gamma$')
ylabel('Policy at state $s_2$')
figure()
plot(gammas, V_res)
legend(['State 1', 'State 2'])
xlabel('$\gamma$')
ylabel('(Normalized) optimal value function')
show()