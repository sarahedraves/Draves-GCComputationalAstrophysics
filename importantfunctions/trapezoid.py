def trapezoid(function, a, b, N=10):
    deltax=(b-a)/N
    mysum=0
    for k in range(1,N+1):
        mysum+=function(a+k*deltax)
    fa=function(a)
    fb=function(b)
    return deltax*(0.5*fa+0.5*fb+mysum)