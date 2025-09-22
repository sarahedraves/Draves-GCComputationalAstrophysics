def centereddiff(f,x,h):
    fplus=f(x+h/2)
    fminus=f(x-h/2)
    return (fplus-fminus)/h