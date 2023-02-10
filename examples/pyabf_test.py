# -*- coding: utf-8 -*-
import pyabf
import matplotlib.pyplot as plt

abf = pyabf.ABF("demo.abf")
abf.setSweep(14)
plt.plot(abf.sweepX, abf.sweepY)
plt.show()