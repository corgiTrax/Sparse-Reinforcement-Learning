import math
import numpy as np
import matplotlib
from matplotlib import pyplot as plt


circle2 = plt.Circle((0.65, 0.65), 0.572, color='blue')

fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
fig = plt.gcf()
ax = fig.gca()
ax.xaxis.set_ticks(np.arange(-1.5, 1.5, 0.1))
ax.yaxis.set_ticks(np.arange(-1.5, 1.5, 0.1))

# change default range so that new circles will work
ax.set_xlim((0, 1.5))
ax.set_ylim((0, 1.5))

ax.add_artist(circle2)
ax.grid(color='g', linestyle='-', linewidth=2)

# unpack the first point
x = 0.65
y = 0.65

length = 0.572

for i in range(0,16):
    angle = 22.5*i

    # find the end point
    endy = y + length * math.sin(math.radians(angle-180))
    endx = x + length * math.cos(math.radians(angle-180))

    ax.plot([x, endx], [y, endy], color='r', linewidth=2)



plt.show()

