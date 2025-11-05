import numpy as np

def Euler(f, r0s, *args, t0=0, h=0.1, N=None, maxt=None): #args is to make this generalizable so the necessary arguments can vary based on the parameters for diffeq
    if type(r0s)!=np.ndarray: #so this still works for only one equation instead of multiple ODEs
        r0s=np.array([r0s])
    if (N is None and maxt is None) or (N is not None and maxt is not None):
        print('Exactly one of the N and maxt parameters must have a value.')
        return None,None

    #initialize arrays
    if N is not None: #go N steps so need N+1 points
        Ts=np.linspace(t0,t0+N*h,N+1)
    elif maxt is not None: #go to maxt
        Ts=np.arange(t0,maxt+h,h)
    Rs=np.zeros((Ts.size,r0s.size))
    Rs[0,:]=r0s

    for i in range(1, len(Ts)): #starting at the second point
        Rs[i]=Rs[i-1]+h*f(Rs[i-1],Ts[i-1], *args)
    return Ts, Rs

def RK4(f, r0s, *args, t0=0, h=0.1, N=None, maxt=None): #args is to make this generalizable so the necessary arguments can vary based on the parameters for diffeq
    if type(r0s)!=np.ndarray: #so this still works for only one equation instead of multiple ODEs
        r0s=np.array([r0s])
    if (N is None and maxt is None) or (N is not None and maxt is not None):
        print('Exactly one of the N and maxt parameters must have a value.')
        return None,None

    #initialize arrays
    if N is not None: #go N steps so need N+1 points
        Ts=np.linspace(t0,t0+N*h,N+1)
    elif maxt is not None: #go to maxt
        Ts=np.arange(t0,maxt+h,h)
    Rs=np.zeros((Ts.size,r0s.size))
    Rs[0,:]=r0s

    for i in range(1, len(Ts)): #starting at the second point
        t=Ts[i-1]
        r=Rs[i-1]
        k1=h*f(r,t, *args)
        k2=h*f(r+0.5*k1,t+0.5*h, *args)
        k3=h*f(r+0.5*k2,t+0.5*h, *args)
        k4=h*f(r+k3,t+h, *args)
        Rs[i]=r+(1/6)*(k1+2*k2+2*k3+k4)
    return Ts, Rs