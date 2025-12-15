import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy
import argparse
from RKadaptivemultieq import *
from diffeqs import *
from diffeqs_forscipy import *
from plottingfns import * #still have to update animate to handle varying size time steps
from getICs import *
from errorfunctions import *
import sys
import os
sys.path.append(os.path.join('..', 'importantfunctions'))
from ODEsolvers import *

def main():
    #create parser and add arguments 
    parser=argparse.ArgumentParser()
    parser.add_argument('--scenario',
                        choices=['threestars','threestarsandplanet','twostars','twostarsandplanet','oneorbit'],
                        default='threestars',
                        type=str.lower,
                        help="Choose which scenario to simulate. Default: threestars.")
    parser.add_argument('--solver',
                        choices=['my_rk4','myadaptive_rk4','scipy_rk45'],
                        default='myadaptive_rk4',
                        type=str.lower,
                        help="Choose which ODE solver to use. Default: myadaptive_rk4.") 
    parser.add_argument('--displaychoice',
                        choices=['plot','animatefullpath','animatetrailingpath'],
                        default='plot',
                        type=str.lower,
                        help="Choose what will be displayed after the simulation has run. Plot displays line graphs of the positions, animatefullpath shows a gif of the line graphs growing as the simulation continues, and animatetrailingpath shows a similar gif, but with only the most recent part of the lines plotted. Default: plot.")
    parser.add_argument('--ICchoice',
                        choices=['recommended','random','input'],
                        default='recommended',
                        type=str.lower,
                        help="Choose whether to use the recommended initial conditions for the given scenario, generate random ones, or input your own. Default: recommended.")
    parser.add_argument('--filename',
                        default='None',
                        type=str,
                        help="If filename is set, will save the plot or animation with that name. Do not include a file extension. If filename is left as its default value None, the file will not be saved.")
    parser.add_argument('--maxT',
                        default=10,
                        type=float,
                        help="T value that the solver will continue until. Default: 10.")
    parser.add_argument('--plotHs',
                        default=False,
                        action='store_true',
                        help='When this flag is used, a plot of log of step-size vs time will also display. This will only do anything if myadaptive_rk4 is used as the solver and plot is used as the displaychoice.')

    #parse arguments
    args=parser.parse_args()
    scenario=args.scenario
    solver=args.solver
    displaychoice=args.displaychoice
    ICchoice=args.ICchoice
    filename=args.filename
    maxT=args.maxT
    plotHs=args.plotHs

    #set ICs - update
    R0=getICs(scenario,ICchoice)
    if ICchoice=='random':
        print(R0)
    
    #run simulation
    t_span=(0,maxT)
    Ts=None
    Rs=None
    Hs=None #will only get filled in if using adaptive method
    if solver=='scipy_rk45': #using really low tolerances for all of these because it's so fast anyways
        Ts=np.linspace(t_span[0],t_span[1],10000)
        if scenario=='threestars':
            results=scipy.integrate.solve_ivp(threestars_forscipy,t_span=t_span,y0=R0,first_step=1e-6,t_eval=Ts,rtol=1e-12,atol=1e-12)
            Rs=results.y.T
        elif scenario=='threestarsandplanet':
            results=scipy.integrate.solve_ivp(threestarsandplanet_forscipy,t_span=t_span,y0=R0,first_step=1e-6,t_eval=Ts,rtol=1e-12,atol=1e-12)
            Rs=results.y.T
        elif scenario=='twostars':
            results=scipy.integrate.solve_ivp(twostars_forscipy,t_span=t_span,y0=R0,first_step=1e-6,t_eval=Ts,rtol=1e-12,atol=1e-12)
            Rs=results.y.T
        elif scenario=='twostarsandplanet':
            results=scipy.integrate.solve_ivp(twostarsandplanet_forscipy,t_span=t_span,y0=R0,first_step=1e-6,t_eval=Ts,rtol=1e-12,atol=1e-12)
            Rs=results.y.T
        elif scenario=='oneorbit':
            results=scipy.integrate.solve_ivp(oneorbit_forscipy,t_span=t_span,y0=R0,first_step=1e-6,t_eval=Ts,rtol=1e-12,atol=1e-12)
            Rs=results.y.T
    elif solver=='my_rk4':
    #these step sizes will not always produce results that match the other two solver options but it will be really slow otherwise
        if scenario=='threestars':
            Ts,Rs=RK4(threestars, R0, t0=t_span[0], h=0.00001, maxt=t_span[1])
        elif scenario=='threestarsandplanet':
            Ts,Rs=RK4(threestarsandplanet, R0, t0=t_span[0], h=0.00001, maxt=t_span[1])
        elif scenario=='twostars':
            Ts,Rs=RK4(twostars, R0, t0=t_span[0], h=0.00001, maxt=t_span[1])
        elif scenario=='twostarsandplanet':
            Ts,Rs=RK4(twostarsandplanet, R0, t0=t_span[0], h=0.00001, maxt=t_span[1])
        elif scenario=='oneorbit':
            Ts,Rs=RK4(oneorbit, R0, t0=t_span[0], h=0.00001, maxt=t_span[1])
    elif solver=='myadaptive_rk4': 
        #for tolerances here, tested different tolerances with scipy in 12.15_findtols.ipynb and then double checked by running this program that the tolerances work to keep the recommended IC plots looking the same
        #nevermind! a small fix in the adaptive method made it so much faster so will just use 1e-12 for everything
        if scenario=='threestars':
            Ts,Rs,Hs=RK4adapt(threestars,errf_threebody,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='threestarsandplanet':
            Ts,Rs,Hs=RK4adapt(threestarsandplanet,errf_fourbody,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='twostars':
            Ts,Rs,Hs=RK4adapt(twostars,errf_twobody,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='twostarsandplanet':
            Ts,Rs,Hs=RK4adapt(twostarsandplanet,errf_threebody,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='oneorbit':
            Ts,Rs,Hs=RK4adapt(oneorbit,errf_onebody,R0,t_span,hstart=1e-6,tol=1e-12)
            
    #display results
    if filename=='None':
        filename=None
    colors=getcolors(scenario,displaychoice)
    
    if displaychoice=='plot':
        fig=plot(Ts,Rs,Hs,plotHs,colors,filename=filename)
    elif displaychoice=='animatefullpath':
        anim=animate(Ts,Rs,colors,trailing=False,filename=filename)
    elif displaychoice=='animatetrailingpath':
        anim=animate(Ts,Rs,colors,filename=filename)
    plt.show() #consider adding another plot of time vs h for when adaptive integrator is used

if __name__=="__main__":
    main()