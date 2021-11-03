import turtle
import random
import numpy as np
from matplotlib import pyplot as plt

# pen = turtle.Turtle()
# pen.speed(0)
# pen.color("green")
# pen.penup()

x = 0
y = 0

ans = []

barnsley = [0.01, 0.86, 0.93]

bounds = barnsley

# bounds = [a, b, c]

for n in range(11000):
    # pen.goto(65 * x, 37 * y - 252)  # scale the fern to fit nicely inside the window
    # pen.pendown()
    # pen.dot(3)
    # pen.penup()
    r = random.random()
    if r < bounds[0]:
        x, y =  0.00 * x + 0.00 * y,  0.00 * x + 0.16 * y + 0.00
    elif r < bounds[1]:
        x, y =  0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.60
    elif r < bounds[2]:
        x, y =  0.20 * x - 0.26 * y,  0.23 * x + 0.22 * y + 1.60
    else:
        x, y = -0.15 * x + 0.28 * y,  0.26 * x + 0.24 * y + 0.44
    ans.append([x,y])

ans = np.asarray(ans)

x = ans[:,0]
y = ans[:,1]
plt.scatter(x,y, 0.2, color = 'green')
plt.show()