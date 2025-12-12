#scipy needs t and then state and all my solvers are the other way around
#it's easier just to make a separate set of diffeqs for scipy because if i updated all my solvers
#then all the notebooks that currently call those solvers would break
#and that is a lot of notebooks (and some past hw assignments)

import numpy as np

#this is the diffeq that does the effect of body b on a
def Fab(ra,rb,t,mb,G=1): #where ra is the vector (x,y,vx,vy) for body a and rb is for body b
    dx=rb[0]-ra[0]
    dy=rb[1]-ra[1]
    
    vx=ra[2]
    vy=ra[3]
    
    R=(dx**2+dy**2)**0.5

    ax=G*mb*dx/(R**3)
    ay=G*mb*dy/(R**3)
    
    return np.array([vx,vy,ax,ay],float)

def threestars_forscipy(t,state,m1=1,m2=1,m3=1):
    r1=state[0:4]
    r2=state[4:8]
    r3=state[8:12]

    dr1=Fab(r1,r2,t,m2)+Fab(r1,r3,t,m3) #just adding up the effects of the different stars on each other
    dr2=Fab(r2,r1,t,m1)+Fab(r2,r3,t,m3)
    dr3=Fab(r3,r1,t,m1)+Fab(r3,r2,t,m2)

    return np.concatenate([dr1,dr2,dr3])

def threestarsandplanet_forscipy(t,state,m1=1,m2=1,m3=1):
    r1=state[0:4]
    r2=state[4:8]
    r3=state[8:12]
    planet=state[12:16]

    dr1=Fab(r1,r2,t,m2)+Fab(r1,r3,t,m3) #just adding up the effects of the different stars on each other but effects from planet
    dr2=Fab(r2,r1,t,m1)+Fab(r2,r3,t,m3)
    dr3=Fab(r3,r1,t,m1)+Fab(r3,r2,t,m2)

    dplanet=Fab(planet,r1,t,m1)+Fab(planet,r2,t,m2)+Fab(planet,r3,t,m3) #planet is affected by all three stars

    return np.concatenate([dr1,dr2,dr3,dplanet])

def twostars_forscipy(t,state,m1=1,m2=1):
    r1=state[0:4]
    r2=state[4:8]

    dr1=Fab(r1,r2,t,m2)
    dr2=Fab(r2,r1,t,m1)

    return np.concatenate([dr1,dr2])

def twostarsandplanet_forscipy(t,state,m1=1,m2=1):
    r1=state[0:4]
    r2=state[4:8]
    planet=state[8:12]

    dr1=Fab(r1,r2,t,m2)
    dr2=Fab(r2,r1,t,m1)

    dplanet=Fab(planet,r1,t,m1)+Fab(planet,r2,t,m2)

    return np.concatenate([dr1,dr2,dplanet])

#this is the diffeq to do one body orbiting a fixed point
def oneorbit_forscipy(t,r,M=1,G=1): #where r is the vector (x,y,vx,vy)
    x=r[0]
    y=r[1]
    vx=r[2]
    vy=r[3]
    R=(x**2+y**2)**0.5
    return np.array([vx,vy,-G*M*x/(R**3),-G*M*y/(R**3)],float)