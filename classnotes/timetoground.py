import sys

print(sys.argv)
height=float(sys.argv[1])

def timetoground(h,g=9.8):
    t=(h*2/g)**0.5
    return t

print(timetoground(height))