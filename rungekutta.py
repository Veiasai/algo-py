import numpy as np
from math import *
from scipy import optimize
import matplotlib.pyplot as plt
import base64
import io
import json

def rungekutta4(f,y0,h,a,b):
    n = int(np.floor((b-a)/h))
    x = np.zeros(n)
    y = np.zeros((y0.shape[0],n))
    x[0] = a
    y[:,0] = y0
    for i in range(n-1):
        x[i+1] = x[i]+h
        k1 = f(x[i],y[:,i])
        k2 = f(x[i]+h/2,y[:,i]+h*k1/2)
        k3 = f(x[i]+h/2,y[:,i]+h*k2/2)
        k4 = f(x[i]+h,y[:,i]+h*k3)
        y[:,i+1] = y[:,i] + h*(k1+2*k2+2*k3+k4)/6
    return x, y

def rungekutta(paras):
    def f(x, y):
        loc = {'ret': None, 'x': x, 'y': y}
        exec(paras['f'], globals(), loc)
        return loc['ret']
    y0 = np.array(paras['data'])
    h  = float(paras['h'])
    a  = float(paras['a'])
    b  = float(paras['b'])

    x,y = rungekutta4(f,y0,h,a,b)
    fig = plt.Figure()
    ax = fig.subplots()
    for index in range(len(y)):
        ax.plot(x,y[index],label="y"+str(index+1))
    ax.legend()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return {'img': img, 'x': x, 'y': y}


if __name__ == "__main__":
    paras = {'f': '''
dy = np.zeros(3)
dy[0] = y[1]*y[2]
dy[1] = -y[0]+y[2]
dy[2] = -0.51*y[0]*y[1]
ret = dy
''', 'data': [1,1,3], 'h': "0.15", 'a': 0, 'b': 15}

    ret = rungekutta(paras)
    print(ret['x'])
    print(ret['y'])
    img = open('./rungekutta.png', 'w')
    img.write(ret['img'])
    img.close()