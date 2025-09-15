from gaussxw import *

def trapezoid(function, a, b, N=10):
    deltax=(b-a)/N
    mysum=0
    for k in range(1,N+1): #goes to N since range doesn't include the endpoint
        mysum+=function(a+k*deltax)
    fa=function(a)
    fb=function(b)
    return deltax*(0.5*fa+0.5*fb+mysum)

def simpsons(function, a, b, N=10): #N must be even
    deltax=(b-a)/N
    mysum=function(a)+function(b)
    N2=int(N/2) #need to cast this as an int for the range function to work - could use integer division // instead
    for k in range (1, (N2)+1): #goes to N/2 since range doesn't include the endpoint
        mysum+=4*function(a+(2*k-1)*deltax)
    for k in range (1, N2): #goes to N/2 -1
        mysum+=2*function(a+2*k*deltax)
    return mysum*deltax/3

def gaussquad(function,a,b,N=3):
    points,weights=gaussxwab(N,a,b)
    mysum=0
    for k in range(0,N):
        mysum+=weights[k]*function(points[k])
    return mysum