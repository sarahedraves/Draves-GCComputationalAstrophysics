import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def mfp(n,sigma): #mean free path
    return 1/(n*sigma)

def transform(z,l): #z is the random number and l is the mean free path
    mu=1/l
    return -(1/mu)*np.log(1-z) #transformation of exponential equation

def pathplot(Rs,Ts,R,numits,slaborsun):
    plt.plot(Ts,Rs,color='lightpink',marker='.',zorder=2)
    plt.scatter(Ts,Rs,color='deeppink',zorder=3)
    plt.xlabel('Time (s)') 
    plt.ylabel('Position (m)')
    if slaborsun=='slab':
        plt.axhline(y=R,color='black',zorder=1)
    elif slaborsun=='sun':
        plt.axhline(y=R,color='black',zorder=1)
        plt.axhline(y=-R,color='black',zorder=1)
    plt.title(f'Photon escapes the {slaborsun} in {numits} time steps')
    plt.show()

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def pathanimate(Ts, Rs, slaborsun, numits, R, interval=50): #from claude with a few modifications
    # Create figure and axis
    fig, ax = plt.subplots()
    
    # Set up the plot limits and labels
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position (m)')
    ax.set_xlim(min(Ts) - 0.1 * (max(Ts) - min(Ts)), max(Ts) + 0.1 * (max(Ts) - min(Ts)))
    ax.set_ylim(min(Rs) - 0.1 * (max(Rs) - min(Rs)), max(Rs) + 0.1 * (max(Rs) - min(Rs)))
    
    # Add the horizontal line(s)
    if slaborsun=='slab':
        ax.axhline(y=R,color='black',zorder=1)
    elif slaborsun=='sun':
        ax.axhline(y=R,color='black',zorder=1)
        ax.axhline(y=-R,color='black',zorder=1)

    ax.set_title(f'Photon escapes the {slaborsun} in {numits} time steps')
    
    # Initialize empty line and scatter plot
    line, = ax.plot([], [], color='lightpink', marker='.', zorder=2)
    scatter = ax.scatter([], [], color='deeppink', zorder=3)
    
    # Initialization function
    def init():
        line.set_data([], [])
        scatter.set_offsets(np.empty((0, 2)))
        return line, scatter
    
    # Animation function
    def animate(frame):
        # Update line data up to current frame
        line.set_data(Ts[:frame+1], Rs[:frame+1])
        # Update scatter data up to current frame
        scatter.set_offsets(np.column_stack([Ts[:frame+1], Rs[:frame+1]]))
        return line, scatter
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, init_func=init, 
                                  frames=len(Ts), interval=interval, 
                                  blit=True, repeat=True)
    
    # Display the animation
    plt.show()
    
    return anim


def runslab(sigmaT,c,maxits,R):
    ne=1e26 #1e20 cm^-3 converted to m^-3
    slab_mfp=mfp(ne,sigmaT)
    
    Rs=np.zeros(1) #only one zero
    Xs=np.zeros(1) #this will be the total distance traveled
    numits=1 #starting at the second element
    while Rs[numits-1]<R: #while the photon is still inside the slab
        if numits>=maxits: #emergency escape to prevent it hanging
            print(f'Maximum ({maxits}) iterations reached without photon escaping the slab.')
            break
        
        z=np.random.rand() #get single random number
        x=transform(z,slab_mfp) #transform it into the right distribution
        Xs=np.append(Xs,Xs[numits-1]+x)
        
        if numits==1: #just go straight on first iteration
            theta=0
        else:
            theta=np.random.rand()*np.pi #get a single random number between 0 and pi
        rdelt=x*np.cos(theta) #change in r is x*cos(theta)
        Rs=np.append(Rs,Rs[numits-1]+rdelt) #new position is previous position plus change 
    
        if Rs[numits]<0:
            Rs[numits]=0 #if the photon dips below the bottom of the slab, it just resets - reasoning for this handling is in playground notebook
        numits+=1
    Ts=Xs/c
    return numits,Rs,Ts

def main():
    #create parser and add arguments 
    parser=argparse.ArgumentParser()
    parser.add_argument('--slaborsun',
                        choices=['slab','sun'],
                        default='slab',
                        type=str.lower,
                        help="Choose whether to run the slab or sun simulation. Default: slab.")
    parser.add_argument('--displaychoice', #make this a choice between plotting, animating, and running it N times to report averages
                        choices=['plot','animate','statistics'],
                        default='plot',
                        type=str.lower,
                        help="Plot and animate will each run the simulation once and either plot or animate it. Statistics will run the simulation numtests times and report the mean and standard deviation for number of time steps and total travel time. Default: plot.")
    parser.add_argument('--numtests',
                        default=1000,
                        type=int,
                        help="If displaychoice is set to statistics, this will be the number of times the simulation is run. Otherwise the parameter won't do anything.")

    #parse arguments
    args=parser.parse_args()
    slaborsun=args.slaborsun
    displaychoice=args.displaychoice
    numtests=args.numtests

    #set constants
    sigmaT=6.652e-29 #6.652e-25 cm^2 converted to m^2
    c=3e8 #speed of light in meters per second
    maxits=10000
    if slaborsun=='slab':
        R=1e3 #1km converted to m
    elif slaborsun=='sun':
        R=696340*1000 #696,340km converted to m

    if displaychoice=='plot':
        if slaborsun=='slab':
            numits,Rs,Ts=runslab(sigmaT,c,maxits,R)
            pathplot(Rs,Ts,R,numits,slaborsun)
        elif slaborsun=='sun':
            print('plot sun')
    elif displaychoice=='animate':
        if slaborsun=='slab':
            numits,Rs,Ts=runslab(sigmaT,c,maxits,R)
            pathanimate(Ts, Rs, slaborsun, numits, R)
        elif slaborsun=='sun':
            print('animate sun')
    elif displaychoice=='statistics':
        if slaborsun=='slab':
            timesteps=np.full(numtests, np.nan) #not doing zeros because if one of the simulations fails, don't want that to be averaged in
            times=np.full(numtests, np.nan)
            for i in range(numtests):
                numits,Rs,Ts=runslab(sigmaT,c,maxits,R)
                timesteps[i]=numits
                times[i]=Ts[-1] #total time is just the last element in the times array
            print(f'The photon escaped the slab in an average of {np.nanmean(timesteps):.1f} steps, taking an average of {np.nanmean(times):.2e} seconds. The standard deviations were {np.nanstd(timesteps):.1f} steps and {np.nanstd(times):.2e} seconds, respectively.')
        elif slaborsun=='sun':
            print('statistics sun')

if __name__=="__main__":
    main()