from gaussxw import *

def trapezoid(function, a, b, N=10, adaptive=False):
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

def errortest(calctype,I1,I2):
    if calctype=='trapezoid':
        return (1/3)*abs(I2-I1)
    elif calctype=='simpsons':
        return (1/15)*abs(I2-I1)
    else:
        print("Can't estimate error for this calc type.")

def adaptivetrapezoid(function, a, b, epsilon=10**-5):
    N=2
    I1=trapezoid(function,a,b,N=N)
    I2=trapezoid(function,a,b,N=N*2)
    error=errortest('trapezoid',I1,I2)
    while error>epsilon:
        N*=2
        I1=I2
        I2=trapezoid(function,a,b,N=N*2)
        error=errortest('trapezoid',I1,I2)
    return I2

def adaptivesimpsons(function, a, b, epsilon=10**-5):
    N=2
    I1=simpsons(function,a,b,N=N)
    I2=simpsons(function,a,b,N=N*2)
    error=errortest('simpsons',I1,I2)
    while error>epsilon:
        N*=2
        I1=I2
        I2=simpsons(function,a,b,N=N*2)
        error=errortest('simpsons',I1,I2)
    return I2