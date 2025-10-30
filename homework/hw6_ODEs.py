import sys
import os
import argparse
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
sys.path.append(os.path.join('..', 'importantfunctions'))
from ODEsolvers import * #see this file for the different solvers methods

def f(r,t,G,M,L): #where r is the vector (x,y,vx,vy)
    x=r[0]
    y=r[1]
    vx=r[2]
    vy=r[3]
    R=(x**2+y**2)**0.5
    return np.array([vx,vy,
                     -G*M*x/(R**2*(R**2+0.25*L**2)**0.5),
                     -G*M*y/(R**2*(R**2+0.25*L**2)**0.5)],float)

def main():
    #create parser and add arguments 
    parser=argparse.ArgumentParser()

    #initialize constants
    G=1
    M=10
    L=2
    x0=1
    y0=0
    vx0=0
    vy0=1
    R0s=np.array([x0,y0,vx0,vy0])
    h=0.01
    maxt=100
    
    Ts,Rs=RK4(f,R0s,G,M,L,h=h,maxt=maxt)
    fig=go.Figure(data=go.Scatter(x=Rs[:,0],y=Rs[:,1],mode='lines'))
    fig.update_yaxes(scaleanchor="x", scaleratio=1) #from chatgpt
    fig.show()

if __name__=="__main__":
    main()