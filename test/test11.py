import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure()
ax = plt.axes()

# fc = face color, ec = edge color

r = patches.Rectangle(xy=(0, 0), width=0.25, height=0.5, ec='#000000', fill=False)

ax.add_patch(r)

plt.axis('scaled')
ax.set_aspect('equal')

