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

def plotpoints(Ts,Rs): #asked chatgpt for how to modify different parts of the figure
    fig=go.Figure(data=go.Scatter(x=Rs[:,0],y=Rs[:,1],mode='lines',
                                  marker=dict(color="black"),
                                  customdata=np.column_stack((Rs[:,2:4],Ts)), 
                                  hovertemplate=(
                                      'X: %{x:.3f}<br>'
                                      'Y: %{y:.3f}<br>'
                                      'Vx: %{customdata[0]:.3f}<br>'
                                      'Vy: %{customdata[1]:.3f}<br>'
                                      'T: %{customdata[2]:.3f}<extra></extra>')))
    fig.update_yaxes(scaleanchor='x', scaleratio=1) 
    fig.update_layout(title="Spatial Coordinates of Ball Bearing", title_x=0.5,
                      xaxis_title="X Coordinate", yaxis_title="Y Coordinate",
                      showlegend=False)
    fig.add_trace(go.Scatter(x=[Rs[0,0]],y=[Rs[0,1]],mode="markers+text",
                             marker=dict(size=12, color='green'),    
                             text=["Start Point"],    
                             textposition="bottom center",
                             textfont=dict(color="green",family="Arial Black"),
                             hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=[Rs[-1,0]],y=[Rs[-1,1]],mode="markers+text",
                             marker=dict(size=12, color='red'),    
                             text=["End Point"],    
                             textposition="bottom center",
                             textfont=dict(color="red",family="Arial Black"),
                             hoverinfo='skip'))
    fig.show()
    
def main():
    #create parser and add arguments 
    parser=argparse.ArgumentParser()
    parser.add_argument('--solver',
                        choices=['rk4','euler'],
                        default='rk4',
                        type=str.lower,
                        help="Choose which ODE solver to use. Default: RK4.")
    parser.add_argument('--initconds', nargs=4, type=float, 
                        default=[1,0,0,1],
                        metavar=('x0', 'y0', 'vx0', 'vy0'),
                        help='Values for the initial conditions. Default: [1,0,0,1].')
    parser.add_argument('--timestep',
                        default=0.01,
                        type=float,
                        help='The h value used by the solver. Consider the solver type when selecting. Default: 0.01.')
    parser.add_argument('--maxt',
                        default=10,
                        type=float,
                        help='The final time that the solver will go to. Default: 10.')

    #parse arguments
    args=parser.parse_args()
    solver=args.solver
    R0s=np.array(args.initconds)
    h=args.timestep
    maxt=args.maxt
    
    #initialize constants
    G=1
    M=10
    L=2

    if solver=='rk4':
        Ts,Rs=RK4(f,R0s,G,M,L,h=h,maxt=maxt)
    elif solver=='euler':
        Ts,Rs=Euler(f,R0s,G,M,L,h=h,maxt=maxt)
    plotpoints(Ts,Rs)

if __name__=="__main__":
    main()