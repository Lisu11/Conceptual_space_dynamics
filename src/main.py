#!/usr/bin/python3

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



W = np.genfromtxt('data/w.csv', delimiter=',')
n = len(W)
L = np.identity(n) - np.diag(np.diag(W))
C = np.genfromtxt('data/c.csv', delimiter=',')
m = len(C)
mu = np.genfromtxt('data/mu.csv', delimiter=',')
l = len(mu[0])
M = []
for i in range(n):
    for il in range(l):
        row = []
        for j in range(n):
            row = row + [ mu[i][il] * mu[j][jl] for jl in range(l)]
        M.append(row)
M = np.array(M)
u = np.vstack(np.genfromtxt('data/u.csv', delimiter=','))

x = np.copy(u)
print('l=', l)
print('n=', n)
print('m=', m)
Il   = np.identity(l)
Inlm = np.identity(n*l*m)
Ilm  = np.identity(l*m)

operator = np.kron(np.matmul(np.kron(np.matmul(L, W), Il), M), C)
tail     = np.matmul(Inlm - np.kron(L, Ilm), u) 


fig, ax = plt.subplots()
lns = []
for i in range(n):
    ln, = plt.plot(u[i*l*m:(i+1)*l*m:m], u[i*l*m+1:(i+1)*l*m:m], 'o')
    lns.append(ln)



def step(frame):
    global x
    print(x)
    x = np.matmul(operator, x) + tail
    for i in range(n):
        lns[i].set_data(x[i*l*m:(i+1)*l*m:m], x[i*l*m+1:(i+1)*l*m:m])
    plt.title('step: ' + str(frame))
    return lns[0],

def init():
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    plt.title("step: 0")
    return ln,


ani = FuncAnimation(fig, func=step, frames=np.arange(1, 100), init_func=init, interval=1000)
plt.show()
