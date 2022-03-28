
"""
========================
Errorbar limit selection
========================

Illustration of selectively drawing lower and/or upper limit symbols on
errorbars using the parameters ``uplims``, ``lolims`` of `~.pyplot.errorbar`.

Alternatively, you can use 2xN values to draw errorbars in only one direction.
"""

import numpy as np
import matplotlib.pyplot as plt
import re
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import pylab


def comma(inputs):
    with_commas = re.sub("\s+", ",", inputs.strip())
    return list(map(float,with_commas.split(',')))

upperlimits = [True, False] * 5
lowerlimits = [False, True] * 5

# Define Data

x = comma("432.0   540.3   173.5   270.0   296.1   393.7   430.4   451.9   466.5   486.9   511.0   559.4   795.2  8846.0 19752.7   4936.6     5000")
x = comma("500.7   363.5   173.5   245.1   274.7   476.6   559.6   599.4   628.0   661.8   705.7   790.0  1083.3  4162.8 15670.8  14984.0    15000")
print("x: ",x)
x = [1.2, 2, 3, 5]
y = [9, 15, 20, 25]

# Plot error bar

plt.errorbar(x, y, xerr=0.9)

plt.xlabel("Queries per second (QPS)")
plt.ylabel("95th percentile latency")
plt.xlim(0, 80)
plt.ylim(0, 100)

# Display graph

pylab.savefig('plot.png')
plt.show()
