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

def makeplot(root,G,M,m,R,omega):
    rootbuffer=R*0.025 #plus or minus 2.5%
    Xs=np.linspace(root-rootbuffer,root+rootbuffer,1000)
    Ys=np.zeros(Xs.size)* (u.m**5 / u.s**2) #unit of Lagrange2 formula
    for i,x in enumerate(Xs):
        Ys[i]=Lagrange2(x,G,M,m,R,omega)
    plt.plot(Xs,Ys,color='blue')
    plt.axhline(y=0,color='limegreen')
    plt.scatter(root,0,color='deeppink',zorder=3) #z order makes sure the dot is on top of the lines. from chatgpt.
    plt.xlabel('r (m)')
    plt.show()

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
    parser.add_argument('--constants', nargs=4, type=float, 
                   default=None,
                   metavar=('M', 'm', 'R', 'omega'),
                   help='Values for all the constants in the Lagrange point equation, except for G which is fixed. Defaults are for the Earth and Moon situation. Order must be mass of more massive object in kg, mass of less massive object in kg, average distance between objects in m, and angular velocity in inverse seconds.') #got this syntax for a list of arguments from Claude

    #parse arguments
    args=parser.parse_args()
    method=args.solvemethod
    plot=args.plot
    constants=args.constants

    default=False
    if constants==None:
        constants=[const.M_earth.value, 7.348e22, 3.844e8, 2.662e-6]
        default=True

    #constants
    G=const.G
    M=constants[0]*u.kg
    m=constants[1]*u.kg
    R=constants[2]*u.m
    omega=constants[3]/u.s

    #set initial guesses
    x1,x2=None,None
    if default==True: #don't really need to bother with this since the calculated initial guesses below would work
        #but i took the time to figure out these initial guesses before i added the parameters so might as well
        if method=='secant':
            x1=3.3e8*u.m #see hw3_playground notebook for how I determined the starting guesses
            x2=3.35e8*u.m
        elif method=='newton':
            x1=3.26e8*u.m 
        elif method=='bisection':
            x1=3.2e8*u.m 
            x2=3.3e8*u.m
    else:
        if method=='secant':
            x1=0.5*R #halfway and close by seems as good a guess as any since secant converges quickly
            x2=x1+0.01*R
        elif method=='newton':
            x1=0.1*R #after some testing, this seems to actually converge more quickly when the guess is very wrong than when it's quite close to accurate, i think because the slope is very shallow close to the actual root so each iteration makes little progress, so the default guess is close to the more massive object because that's definitely wrong
        elif method=='bisection':
            x1=0*u.m #default is the whole range of possible values to make sure there's no bisection issues
            x2=R #already has unit

    root=0
    if method=='secant':
        root=secant(Lagrange2,x1,x2,G,M,m,R,omega,tol=1e-6)
    elif method=='newton':
        root=Newton(Lagrange2,Lprime,x1,G,M,m,R,omega,tol=1e-4) #four sig figs - any more and it will hit the maxits limit. still takes a few seconds.
    elif method=='bisection':
        root=bisection(Lagrange2,x1,x2,G,M,m,R,omega,tol=1e-6)
    print(f'L1 point is {root.value:.5e} {root.unit} from the more massive object along the direct path to the less massive object.')

    if plot:
        makeplot(root,G,M,m,R,omega)

if __name__=="__main__":
    main()