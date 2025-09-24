import astropy.units as u
import math

#the unit functions are just internal to this file and will be called if the starting guesses are given astropy quantities instead of floats

def relax(f,x1=1,tol=1e-10,maxits=100000,**kwargs):#kwargs is to make this generalizable so the necessary arguments can vary based on f
    its=0
    if isinstance(x1, u.Quantity):
        return relax_unit(f,x1,tol,maxits,**kwargs)
    x2=f(x1,**kwargs)
    #while abs(x1-x2)>tol:
    while not math.isclose(x1, x2, rel_tol=tol, abs_tol=1e-12): #learned of this function from asking chatgpt how to modify the condition to focus on sig figs
        its+=1
        x1=x2
        x2=f(x1,**kwargs)
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    return x2

def relax_unit(f,x1,tol=1e-10,maxits=100000,**kwargs):
    its=0
    x2=f(x1,**kwargs)
    #while abs(x1.value-x2.value)>tol:
    while not math.isclose(x1.value, x2.value, rel_tol=tol, abs_tol=1e-12): #learned of this function from asking chatgpt how to modify the condition to focus on sig figs
        its+=1
        x1=x2
        x2=f(x1,**kwargs)
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    return x2

def Newton(f,fprime,x1,tol=1e-10,maxits=100000):
    its=0
    if isinstance(x1, u.Quantity):
        return Newton_unit(f,fprime,x1,tol,maxits)
    x2=x1-f(x1)/fprime(x1)
    #while abs(x1-x2)>tol:
    while not math.isclose(x1, x2, rel_tol=tol, abs_tol=1e-12): #learned of this function from asking chatgpt how to modify the condition to focus on sig figs
        its+=1
        x1=x2
        x2=x1-f(x1)/fprime(x1)
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    return x2

def Newton_unit(f,fprime,x1,tol=1e-10,maxits=100000):
    its=0
    x2=x1-f(x1)/fprime(x1)
    #while abs(x1.value-x2.value)>tol:
    while not math.isclose(x1.value, x2.value, rel_tol=tol, abs_tol=1e-12): #learned of this function from asking chatgpt how to modify the condition to focus on sig figs
        its+=1
        x1=x2
        x2=x1-f(x1)/fprime(x1)
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    return x2

def secant(f,x1,x2,tol=1e-10,maxits=100000):
    its=0
    if isinstance(x1, u.Quantity) or isinstance(x2, u.Quantity):
        unit1=x1.unit
        unit2=x2.unit
        if unit1!=unit2:
            print("Units don't match")
            return
        return secant_unit(f,x1,x2,tol,maxits)
    fx1=f(x1)
    fx2=f(x2)
    x3=x2-fx2*(x2-x1)/(fx2-fx1)
    #while abs(x2-x3)>tol:
    while not math.isclose(x2, x3, rel_tol=tol, abs_tol=1e-12): #learned of this function from asking chatgpt how to modify the condition to focus on sig figs
        its+=1
        x1=x2
        x2=x3
        fx1=fx2 #saves the trouble of recalculating this
        fx2=f(x2) #can think of this as f(x3) but already set x2 to x3
        x3=x2-fx2*(x2-x1)/(fx2-fx1)
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    if unit!=None:
        x3=x3*unit1
    return x3

def secant_unit(f,x1,x2,tol=1e-10,maxits=100000):
    its=0
    fx1=f(x1)
    fx2=f(x2)
    x3=x2-fx2*(x2-x1)/(fx2-fx1)
    #while abs(x2.value-x3.value)>tol:
    while not math.isclose(x2.value, x3.value, rel_tol=tol, abs_tol=1e-12): #learned of this function from asking chatgpt how to modify the condition to focus on sig figs
        its+=1
        x1=x2
        x2=x3
        fx1=fx2 #saves the trouble of recalculating this
        fx2=f(x2) #can think of this as f(x3) but already set x2 to x3
        x3=x2-fx2*(x2-x1)/(fx2-fx1)
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    return x3

#the bisection method will only work when f(xl) and f(xr) have opposite signs. won't do any range doubling to find a root.
def bisection(f,xl,xr,tol=10**-10,maxits=100000):
    if isinstance(xl, u.Quantity) or isinstance(xr, u.Quantity):
        unitl=xl.unit
        unitr=xr.unit
        if unitl!=unitr:
            print("Units don't match")
            return
        return bisection_unit(f,xl,xr,tol,maxits)
    
    if xl>xr or math.isclose(xl, xr, rel_tol=tol, abs_tol=1e-12):
        print('xl (left) guess must be less than xr (right) guess.')
        return
    fxl=f(xl)
    fxr=f(xr)
    if math.isclose(fxl, 0, rel_tol=tol, abs_tol=1e-12):
        print('xl guess is within tolerance of root.')
        return xl
    if math.isclose(fxr, 0, rel_tol=tol, abs_tol=1e-12):
        print('xr guess is within tolerance of root.')
        return xr
    if (fxl>0 and fxr>0) or (fxl<0 and fxr<0):
        print('f(xl) and f(xr) are either both positive or both negative. cannot guarantee that a root is present in that range, so will not evaluate.')
        return
    
    its=0
    xc=None
    while not math.isclose(xl, xr, rel_tol=tol, abs_tol=1e-12):
        its+=1
        xc=(xl+xr)/2
        fxc=f(xc) #only one function evaluation per loop
        if fxl*fxc<0: #will be negative if they have opposite signs, so the root is in that half
            xr=xc
            fxr=fxc
        elif fxr*fxc<0:
            xl=xc
            fxl=fxc
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    return xc

def bisection_unit(f,xl,xr,tol=10**-10,maxits=100000):
    if xl.value>xr.value or math.isclose(xl.value, xr.value, rel_tol=tol, abs_tol=1e-12):
        print('xl (left) guess must be less than xr (right) guess.')
        return
    fxl=f(xl)
    fxr=f(xr)
    if math.isclose(fxl.value, 0, rel_tol=tol, abs_tol=1e-12):
        print('xl guess is within tolerance of root.')
        return xl
    if math.isclose(fxr.value, 0, rel_tol=tol, abs_tol=1e-12):
        print('xr guess is within tolerance of root.')
        return xr
    if (fxl.value>0 and fxr.value>0) or (fxl.value<0 and fxr.value<0):
        print('f(xl) and f(xr) are either both positive or both negative. cannot guarantee that a root is present in that range, so will not evaluate.')
        return
    
    its=0
    xc=None
    while not math.isclose(xl.value, xr.value, rel_tol=tol, abs_tol=1e-12):
        its+=1
        xc=(xl+xr)/2
        fxc=f(xc) #only one function evaluation per loop
        if fxl*fxc<0: #will be negative if they have opposite signs, so the root is in that half
            xr=xc
            fxr=fxc
        elif fxr*fxc<0:
            xl=xc
            fxl=fxc
        if its>maxits:
            print(f"Did not converge after {maxits} iterations.")
            return
    return xc