from math import *

def t_sum(a, b):
    return tuple(a[i] + b[i] for i in range(len(a)))

def t_prod(s, t):
    return tuple(s * e for e in t)

def norm(v):
    return sqrt(sum(e**2 for e in v))