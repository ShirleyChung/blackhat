def sum(a, b):
    n1 = conv_int(a)
    n2 = conv_int(b)
    r = n1 + n2
    return r

def conv_int(x):
    n = int(x)
    return n

print sum("1", "2")