import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

#asked claude how to import files from sibling directory since the chatgpt solution didn't work
sys.path.append(os.path.join('..', 'importantfunctions')) #should work as long as the hierarchy is the same as within my GitHub folder since it doesn't have the full path name

from integrationmethods import *

def ftest(x): #tested with this function first
    return x**4-2*x+1

def f(t): #also tested this one by having wolfram alpha plot the erf(x) from 0 to 3
    return np.exp(-(t**2))

def main():
    #create parser and add arguments
    parser=argparse.ArgumentParser()
    parser.add_argument('--intmethod',
                        choices=['simpsons','trapezoid','gaussianquad'],
                        default='simpsons',
                        type=str.lower,
                        help='Method of integration (default: Simpsons)') #asked claude for help with the syntax of only having a few valid inputs and it also recommended how to make it not case sensitive
    parser.add_argument('--adaptive',
                        default=False,
                        action='store_true',
                        help='When this flag is used, the integration will be adaptive and continue until the tolerance level epsilon is reached. The parameter epsilon is used and the parameter N is not. Does not work if gaussianquad is the chosen integration method. Currently the interative steps are not nested (perhaps later).')
    parser.add_argument('-N',
                        default=10,
                        type=int,
                        help='Number of steps for integration (NOT for spacing of x values along plot). For Simpsons: must be even and recommended 10+ steps. For Trapezoid: recommended 1000+ steps. For Gaussian Quadrature: recommended 3+ steps. Used unless adaptive flag is true. Default is 10.') 
    parser.add_argument('--epsilon',
                        default=10**-5,
                        type=float,
                        help='Error tolerance for adaptive integration. Used if adaptive flag is true. Default is 10^-5.')
    parser.add_argument('--plotlowerbound',
                        default=0,
                        type=float,
                        help='Lower bound of plotted domain for E(x).')
    parser.add_argument('--plotupperbound',
                        default=3,
                        type=float,
                        help='Upper bound of plotted domain for E(x).')
    parser.add_argument('--plotxspacing',
                        default=0.1,
                        type=float,
                        help='Spacing of x points in E(x) plot (NOT step size used in integration).')
    parser.add_argument('--plotline',
                        default=False,
                        action='store_true',
                        help='When this flag is used, the plot is a smooth line instead of a scatterplot.')
    parser.add_argument('--printpoints',
                        default=False,
                        action='store_true',
                        help='When this flag is used, the x and E(x) arrays are printed.')

    #parse arguments
    args=parser.parse_args()
    intmethod=args.intmethod
    adaptive=args.adaptive
    N=args.N
    epsilon=args.epsilon
    plotlowerbound=args.plotlowerbound
    plotupperbound=args.plotupperbound
    plotxspacing=args.plotxspacing
    plotline=args.plotline
    printpoints=args.printpoints

    #restrictions on which inputs work together
    if adaptive and intmethod=='gaussianquad':
        print("Can't use adaptive integration with gaussianquad integration method.")
        return
    
    #create a dictionary of integration methods
    #i asked claude if this was possible and it showed me how to then call the functions
    intmethods={'trapezoid':trapezoid,
                'simpsons':simpsons,
                'gaussianquad':gaussquad,
                'adaptivetrapezoid':adaptivetrapezoid,
                'adaptivesimpsons':adaptivesimpsons}
    #now should be able to call the chosen integration method with intmethods[intmethod]()
    #this does mean they all have to have the same arguments
     
    #generate array of x values for E(x) plot
    Xs=np.arange(plotlowerbound,plotupperbound+plotxspacing,plotxspacing) #need to add plotxspacing to plotupperbound since arange does not include the end point by default
    
    #generate empty array which will later store E(x) values
    Es=np.zeros(Xs.size)

    #perform integration for each x value
    if adaptive==False:
        for i in range(Xs.size):
            Es[i]=intmethods[intmethod](f,0,Xs[i],N=N) #integrate f from 0 to x
    else: #adaptive==True
        method='adaptive'+intmethod
        for i in range (Xs.size):
            Es[i]=intmethods[method](f,0,Xs[i],epsilon=epsilon)

    #print points
    if printpoints:
        print('x: ',Xs)
        print('E(x): ',Es)
    
    #plot
    if plotline:
        plt.plot(Xs,Es,color='deeppink')
    else:
        plt.scatter(Xs,Es,color='deeppink')
    plt.xlabel(r'$x$')
    plt.ylabel(r'$E(x)$')
    if adaptive:
        title=r'$E(x)$ vs $x$ where $E(x)$ is the error function'+'\nwith adaptive '+intmethod+' integration and '+str(epsilon)+' error tolerance'
    else: #adaptive==False
        title=r'$E(x)$ vs $x$ where $E(x)$ is the error function'+'\nwith '+intmethod+' integration and '+str(N)+' steps'
    plt.title(title)
    plt.show()

if __name__=="__main__":
    main()