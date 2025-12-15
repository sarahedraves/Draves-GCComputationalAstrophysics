import numpy as np
import argparse

def recommendedICs(scenario):
    R0=None
    if scenario=='threestars':
        #this is the butterfly I sequence orbit 1.2.A from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
        R01=np.array([-1,0,0.306893,0.125507])
        R02=np.array([1,0,0.306893,0.125507])
        R03=np.array([0,0.3133550361,-0.613786,-0.251014])
        R0=np.concatenate([R01,R02,R03])
    elif scenario=='threestarsandplanet':
        #see 12.8_introduceplanet.ipynb for selection process
        R0=np.array([1,0,0,0.57735,-0.5,0.8660254,-0.28867513,-0.5,-0.5,-0.8660254,
                     0.28867513,-0.5,2,0,0,0.9797959])
    elif scenario=='twostars':
        #see 12.12_ICfinding.ipynb for selection process for this and the two below
        R0=np.array([-0.1,0,0,1,0.6,0,0,-1])
    elif scenario=='twostarsandplanet':
        R0s=np.array([-0.1,0,0,1,0.6,0,0,-1])
        planet0=np.array([0.3,0,0.4,0.4]) 
        R0=np.concatenate([R0s,planet0])
    elif scenario=='oneorbit':
        R0=np.array([0.50006284, 0.82040306, 0.4801929,  0.17642735])
    return R0

def randomICs(scenario):
    size=0
    if scenario=='threestars':
        size=12
    elif scenario=='threestarsandplanet':
        size=16
    elif scenario=='twostars':
        size=8
    elif scenario=='twostarsandplanet':
        size=12
    elif scenario=='oneorbit':
        size=4
    R0=np.random.uniform(low=-1,high=1,size=size)
    return R0

def float_pm1(value): #refined this function with chatgpt
    try:
        x = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a float in [-1, 1]")
    if not (-1.0 <= x <= 1.0):
        raise argparse.ArgumentTypeError("must be in [-1, 1]")
    return x

def prompt_float_pm1(name): #refined this function with chatgpt
    while True:
        try:
            return float_pm1(input(f"Enter {name} in [-1, 1]: "))
        except argparse.ArgumentTypeError:
            print("Value must be a float between -1 and 1, inclusive.")

def inputICs(scenario):
    R0=None
    if scenario=='threestars':
        X1=prompt_float_pm1('initial x-coord of star 1')
        Y1=prompt_float_pm1('initial y-coord of star 1')
        VX1=prompt_float_pm1('initial x-velocity of star 1')
        VY1=prompt_float_pm1('initial y-velocity of star 1')
        X2=prompt_float_pm1('initial x-coord of star 2')
        Y2=prompt_float_pm1('initial y-coord of star 2')
        VX2=prompt_float_pm1('initial x-velocity of star 2')
        VY2=prompt_float_pm1('initial y-velocity of star 2')
        X3=prompt_float_pm1('initial x-coord of star 3')
        Y3=prompt_float_pm1('initial y-coord of star 3')
        VX3=prompt_float_pm1('initial x-velocity of star 3')
        VY3=prompt_float_pm1('initial y-velocity of star 3')
        R0=np.array([X1,Y1,VX1,VY1,X2,Y2,VX2,VY2,X3,Y3,VX3,VY3])
    elif scenario=='threestarsandplanet':
        X1=prompt_float_pm1('initial x-coord of star 1')
        Y1=prompt_float_pm1('initial y-coord of star 1')
        VX1=prompt_float_pm1('initial x-velocity of star 1')
        VY1=prompt_float_pm1('initial y-velocity of star 1')
        X2=prompt_float_pm1('initial x-coord of star 2')
        Y2=prompt_float_pm1('initial y-coord of star 2')
        VX2=prompt_float_pm1('initial x-velocity of star 2')
        VY2=prompt_float_pm1('initial y-velocity of star 2')
        X3=prompt_float_pm1('initial x-coord of star 3')
        Y3=prompt_float_pm1('initial y-coord of star 3')
        VX3=prompt_float_pm1('initial x-velocity of star 3')
        VY3=prompt_float_pm1('initial y-velocity of star 3')
        Xp=prompt_float_pm1('initial x-coord of planet')
        Yp=prompt_float_pm1('initial y-coord of planet')
        VXp=prompt_float_pm1('initial x-velocity of planet')
        VYp=prompt_float_pm1('initial y-velocity of planet')
        R0=np.array([X1,Y1,VX1,VY1,X2,Y2,VX2,VY2,X3,Y3,VX3,VY3,Xp,Yp,VXp,VYp])
    elif scenario=='twostars':
        X1=prompt_float_pm1('initial x-coord of star 1')
        Y1=prompt_float_pm1('initial y-coord of star 1')
        VX1=prompt_float_pm1('initial x-velocity of star 1')
        VY1=prompt_float_pm1('initial y-velocity of star 1')
        X2=prompt_float_pm1('initial x-coord of star 2')
        Y2=prompt_float_pm1('initial y-coord of star 2')
        VX2=prompt_float_pm1('initial x-velocity of star 2')
        VY2=prompt_float_pm1('initial y-velocity of star 2')
        R0=np.array([X1,Y1,VX1,VY1,X2,Y2,VX2,VY2])
    elif scenario=='twostarsandplanet':
        X1=prompt_float_pm1('initial x-coord of star 1')
        Y1=prompt_float_pm1('initial y-coord of star 1')
        VX1=prompt_float_pm1('initial x-velocity of star 1')
        VY1=prompt_float_pm1('initial y-velocity of star 1')
        X2=prompt_float_pm1('initial x-coord of star 2')
        Y2=prompt_float_pm1('initial y-coord of star 2')
        VX2=prompt_float_pm1('initial x-velocity of star 2')
        VY2=prompt_float_pm1('initial y-velocity of star 2')
        Xp=prompt_float_pm1('initial x-coord of planet')
        Yp=prompt_float_pm1('initial y-coord of planet')
        VXp=prompt_float_pm1('initial x-velocity of planet')
        VYp=prompt_float_pm1('initial y-velocity of planet')
        R0=np.array([X1,Y1,VX1,VY1,X2,Y2,VX2,VY2,Xp,Yp,VXp,VYp])
    elif scenario=='oneorbit':
        X1=prompt_float_pm1('initial x-coord of orbiting object')
        Y1=prompt_float_pm1('initial y-coord of orbiting object')
        VX1=prompt_float_pm1('initial x-velocity of orbiting object')
        VY1=prompt_float_pm1('initial y-velocity of orbiting object')
        R0=np.array([X1,Y1,VX1,VY1])
        size=4
    return R0

def getICs(scenario,ICchoice):
    if ICchoice=='recommended':
        return recommendedICs(scenario)
    elif ICchoice=='random':
        return randomICs(scenario)
    elif ICchoice=='input':
        return inputICs(scenario)