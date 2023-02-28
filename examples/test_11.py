import numpy as np
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

data = np.random.rand(4, 4)

plt.imshow(data, origin='lower', extent=[-4, 4, -1, 1], aspect=4)

plt.show()