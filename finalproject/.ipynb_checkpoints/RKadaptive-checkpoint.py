import numpy as np

#this will execute a single step of the RK4 process
def RK4step(f,r,t,h,*args):
    k1=h*f(r,t, *args)
    k2=h*f(r+0.5*k1,t+0.5*h, *args)
    k3=h*f(r+0.5*k2,t+0.5*h, *args)
    k4=h*f(r+k3,t+h, *args)
    rnew=r+(1/6)*(k1+2*k2+2*k3+k4)
    return rnew, t+h

def RK4doublestep(f,r,t,h,*args):
    h2=h/2
    rhalf,thalf=RK4step(f,r,t,h2,*args)
    rnew,tnew=RK4step(f,rhalf,thalf,h2,*args)
    return rnew,tnew

def rhoratio(x1,x2,h,tol):
    return 30*h*tol/abs(x1-x2)

def hprime(h,rho):
    return h*(rho**0.25)

def adaptivestep(f,r,t,h,tol,*args):
    x1,t1=RK4step(f,r,t,h,*args)
    x2,t2=RK4doublestep(f,r,t,h,*args)

    hog=h
    if abs(x1-x2)<1e-15: #won't be able to calculate rho if this is less than machine precision because will get divide by 0 error
        return x2,t2,h

    rho=rhoratio(x1,x2,h,tol)
    
    while rho<1:
        h=hprime(h,rho)
        x1,t1=RK4step(f,r,t,h,*args)
        x2,t2=RK4doublestep(f,r,t,h,*args)
        if abs(x1-x2)<1e-15: #need to check each time
            break
        rho=rhoratio(x1,x2,h,tol)
        
    hnew=hprime(h,rho)
    hnew=min(hnew,hog*2) #makes sure that the returned hnew is not more than 2 times as large as the original h
    return x2,t2,hnew

def RK4adapt(f,r0,t_range,*args,hstart=1e-3,tol=1e-12):
    r_list=[r0]
    t_list=[t_range[0]]
    h=hstart

    while t_list[-1]<t_range[1]:
        rnew,tnew,h=adaptivestep(f,r_list[-1],t_list[-1],h,tol,*args)
        r_list.append(rnew)
        t_list.append(tnew)

    return np.array(t_list), np.array(r_list)

    