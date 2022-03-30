
"""
========================
Errorbar limit selection
========================

Illustration of selectively drawing lower and/or upper limit symbols on
errorbars using the parameters ``uplims``, ``lolims`` of `~.pyplot.errorbar`.

Alternatively, you can use 2xN values to draw errorbars in only one direction.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import re

from matplotlib import pylab


def comma(inputs):
    with_commas = re.sub("\s+", ",", inputs.strip()).split(',')
    return list(map(float,with_commas))



x = [1,3,6,12]
y = [
    [224.153, 90.810, 65.906, 55.897],
    [287.336, 149.368, 128.412, 123.193],
    [50.664, 19.900, 21.517, 34.721],
    [690.735, 239.192, 185.162, 170.390],
    [142.686],
    [456.131, 155.372, 105.863, 98.807]
]

for i in range(len(y)):
    t1 = y[i][0]
    for j in range(len(y[i])):
        y[i][j] = t1 / y[i][j]


# Plot error bar
plt.figure(figsize=(15, 10))

plt.plot(x, y[0], label="blackscholes")
plt.plot(x, y[1], label="canneal")
plt.plot(x, y[2], label="dedup")
plt.plot(x, y[3], label="ferret")
#plt.plot(x[0], y[4], label="fft")
plt.plot(x, y[5], label="freqmine")

# exercise 1d)
#plt.axhline(y = 1500, color = 'r', linestyle = '-')
#plt.axvline(x = 65000, color = 'r', linestyle = '-')

plt.xlabel("Number of threads")
plt.ylabel("Speedup")
plt.xlim(0, 12)
plt.ylim(0, 10)
plt.title("Speedup of multiple threads for different workloads")
plt.legend(loc="upper right")

# Display graph

pylab.savefig('plot_part2.png')
plt.show()
