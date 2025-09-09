def simpsons(function, a, b, N=10): #make sure that N is even
    deltax=(b-a)/N
    mysum=function(a)+function(b)
    N2=int(N/2) #need to cast this as an int for the range function to work - could use integer division // instead
    for k in range (1, (N2)+1): #goes to N/2 since range doesn't include the endpoint
        mysum+=4*function(a+(2*k-1)*deltax)
    for k in range (1, N2): #goes to N/2 -1
        mysum+=2*function(a+2*k*deltax)
    return mysum*deltax/3