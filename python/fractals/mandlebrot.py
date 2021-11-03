import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm

def mbrot(z,c):
    for n in range(50):
        if abs(z)<=2:  
            z = z**2 + c
        else:
            return n
    return 1e100

ans = []

sstep = 0.01

c_interesting = -0.8

c = c_interesting

c = -0.9

for i in np.arange(-2.0,2.0,sstep):
    for j in np.arange(-2.0,2.0,sstep):
        z = complex(i,j)
        z = mbrot(z, c)
        if abs(z) != 1e100:
            ans.append((i,j,z))

ans = np.asarray(ans)

if len(ans) > 0:

    # xy = ans[:,2]
    # x = xy.real
    # y = xy.imag

    x = ans[:,0]
    y = ans[:,1]
    c = cm.rainbow( 1 /(0.1 + ans[:,2]) )
    plt.scatter(x, y, 0.01, color = c)
    plt.show()



