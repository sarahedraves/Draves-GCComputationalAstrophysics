import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.constants as const
sys.path.append(os.path.join('..', 'importantfunctions'))
from nonlinearsolvingmethods import * #see this file for newton, secant, and bisection methods

#input for all three functions must be a quantity with units u.m
def Lagrange(r): #don't actually call this one anymore
    #constants
    G=const.G
    Me=const.M_earth
    Mm=7.348e22*u.kg
    R=3.844e8*u.m
    omega=2.662e-6/u.s
    return (G*Me/r**2)-(G*Mm/(R-r)**2)-r*omega**2

def Lagrange2(r,G,M,m,R,omega): #this is better since we don't have the R-r squared. tested to make sure they both give the same result.
    r5=-omega**2*r**5
    r4=2*R*omega**2*r**4
    r3=-omega**2*R**2*r**3
    r2=G*(M-m)*r**2
    r1=-2*G*M*R*r
    r0=G*M*R**2
    return r5+r4+r3+r2+r1+r0

def Lprime(r,G,M,m,R,omega):
    #constants
    r4=-5*omega**2*r**4
    r3=8*R*omega**2*r**3
    r2=-3*omega**2*R**2*r**2
    r1=2*G*(M-m)*r
    r0=-2*G*M*r
    return r4+r3+r2+r1+r0

def main():
    #create parser and add arguments
    parser=argparse.ArgumentParser()
    parser.add_argument('--solvemethod',
                        choices=['newton','secant','bisection'],
                        default='secant',
                        type=str.lower,
                        help='Method of integration (default: secant)')
    parser.add_argument('--plot',
                        default=False,
                        action='store_true',
                        help='When this flag is used, a plot will be shown of the function around the root with an autosized range.')

    #parse arguments
    args=parser.parse_args()
    method=args.solvemethod

    #constants
    G=const.G
    M=const.M_earth
    m=7.348e22*u.kg
    R=3.844e8*u.m
    omega=2.662e-6/u.s

    root=0
    if method=='secant':
        x1=3.3e8*u.m #see hw3_playground notebook for how I determined the starting guesses
        x2=3.35e8*u.m
        root=secant(Lagrange2,x1,x2,G,M,m,R,omega,tol=1e-6)
    elif method=='newton':
        x1=3.26e8*u.m #see hw3_playground notebook for how I determined the starting guesses
        root=Newton(Lagrange2,Lprime,x1,G,M,m,R,omega,tol=1e-4) #four sig figs - any more and it will hit the maxits limit. still takes a few seconds.
    elif method=='bisection':
        xl=3.2e8*u.m #see hw3_playground notebook for how I determined the starting guesses
        xr=3.3e8*u.m
        root=bisection(Lagrange2,xl,xr,G,M,m,R,omega,tol=1e-6)
    print(f'L1 point is {root.value:.5e} {root.unit} from Earth along the direct path to the Moon.')

    

if __name__=="__main__":
    main()