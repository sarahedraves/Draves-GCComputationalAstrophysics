import numpy as np

def errf_fourbody(r1,r2):
    r1=np.concatenate((r1[0:2],r1[4:6],r1[8:10],r1[12:14])) #we just want the positions
    r2=np.concatenate((r2[0:2],r2[4:6],r2[8:10],r2[12:14]))
    return np.linalg.norm(r1-r2)

def errf_threebody(r1,r2):
    r1=np.concatenate((r1[0:2],r1[4:6],r1[8:10])) #we just want the positions
    r2=np.concatenate((r2[0:2],r2[4:6],r2[8:10]))
    return np.linalg.norm(r1-r2)

def errf_twobody(r1,r2):
    r1=np.concatenate((r1[0:2],r1[4:6])) #we just want the positions
    r2=np.concatenate((r2[0:2],r2[4:6]))
    return np.linalg.norm(r1-r2)

def errf_onebody(r1,r2):
    r1=r1[0:2] #we just want the positions
    r2=r2[0:2]
    return np.linalg.norm(r1-r2)