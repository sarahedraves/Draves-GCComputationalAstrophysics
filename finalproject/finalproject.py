import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy
import argparse
from RKadaptivemultieq import *
from diffeqs import *
from plottingfns import * #still have to update animate to handle varying size time steps
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
                        choices=['my_rk4, myadaptive_rk4, scipy_rk45'],
                        default='scipyRK45',
                        type=str.lower,
                        help="Choose which ODE solver to use. Default: scipy_rk45 (because it is much faster).") 
    parser.add_argument('--displaychoice',
                        choices=['plot','animatefullpath','animatetrailingpath'],
                        default='plot',
                        type=str.lower,
                        help="Choose what will be displayed after the simulation has run. Plot displays line graphs of the positions, animatefullpath shows a gif of the line graphs growing as the simulation continues, and animatetrailingpath shows a similar gif, but with only the most recent part of the lines plotted. Default: plot.")
    parser.add_argument('--initialconditionchoice',
                        choice=['recommended','random','input'],
                        default='recommended',
                        type=str.lower,
                        help="Choose whether to use the recommended initial conditions for the given scenario, generate random ones, or input your own. Default: recommended.")
    parser.add_argument('--filename',
                        default='None',
                        type=str,
                        help="If filename is set, will save the plot or animation with that name. Do not include a file extension. If filename is left as its default value None, the file will not be saved.")

    #parse arguments
    args=parser.parse_args()
    scenario=args.scenario
    solver=args.solver
    displaychoice=args.displaychoice
    filename=args.filename

    #set ICs - update
    R01=np.array([-1,0,0.306893,0.125507])
    R02=np.array([1,0,0.306893,0.125507])
    R03=np.array([0,0.3133550361,-0.613786,-0.251014])
    R0=np.concatenate([R01,R02,R03])
    t_span=(0,10)

    #run simulation
    if solver=='scipy_rk45':
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
        if scenario=='threestars':
            Ts,Rs=RK4adapt(threestars,errf,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='threestarsandplanet':
            Ts,Rs=RK4adapt(threestarsandplanet,errf,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='twostars':
            Ts,Rs=RK4adapt(twostars,errf,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='twostarsandplanet':
            Ts,Rs=RK4adapt(twostarsandplanet,errf,R0,t_span,hstart=1e-6,tol=1e-12)
        elif scenario=='oneorbit':
            Ts,Rs=RK4adapt(oneorbit,errf,R0,t_span,hstart=1e-6,tol=1e-12)
            
    #display results
    if filename=='None':
        filename=None
    colors=getcolors(scenario,displaychoice)
    if displaychoice=='plot':
        plot(Ts,Rs,colors,filename=filename)
    elif displaychoice=='animatefullpath':
        animate(Ts,Rs,colors,trailing=False,filename=filename)
    elif displaychoice=='animatetrailingpath':
        animate(Ts,Rs,colors,trailing=False,filename=filename)

if __name__=="__main__":
    main()