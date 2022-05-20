
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

#upperlimits = [True, False] * 5
#lowerlimits = [False, True] * 5

# open file with raw data, go to first line with data
raw_data = open("raw_data_1d.txt", "r")

def find_start_of_dataset(file):
    raw_data_row = raw_data.readline()
    while (raw_data_row[0:4] != "read"):
        raw_data_row = file.readline()
    return raw_data_row


# read QPS and p95 from file, store them in arrays for all runs
def create_data_arrays_per_run(first_row, file):
    x_data = []
    y_data = []
    while (first_row[:4] == "read"):
        raw_row_array = comma(first_row[4:])
        x_data.append(raw_row_array[-2])
        y_data.append(raw_row_array[11])
        first_row = file.readline()
    return (x_data, y_data)

# average data across 3 runs
def create_avg_data_arrays(file):
    raw_data_row = find_start_of_dataset(raw_data)
    run1 = create_data_arrays_per_run(raw_data_row, file)
    x_data = []
    y_data = []
    for i in range(len(run1[0])):
        x_data.append((run1[0][i] - run1[0][0]) / 1000)
        y_data.append((run1[1][i]) / 1000)
    return (x_data, y_data)

# get data from raw data for each benchmark
def create_all_data_arrays(file):
    print("create_all_data_arrays")
    x_data_arrays = []
    y_data_arrays = []
    for i in range(1):
        (x, y) = create_avg_data_arrays(raw_data)
        x_data_arrays.append(x)
        y_data_arrays.append(y)
    return (x_data_arrays, y_data_arrays)

def create_all_cpu_arrays(file):
    raw_data_row = raw_data.readline()
    while (raw_data_row[0:3] != "165"):
        raw_data_row = file.readline()
    x_data = []
    y_data = []
    raw_row_array = comma(raw_data_row)
    x_min = raw_row_array[0]
    print(x_min)
    while (raw_data_row[:3] == "165"):
        raw_row_array = comma(raw_data_row)
        if (int(raw_row_array[0]) > 1 and int(raw_row_array[1]) > 1 and int(raw_row_array[2]) > 1 and int(raw_row_array[3]) > 1):
            x_data.append(int(raw_row_array[0] - x_min))
            y_data.append(raw_row_array[2])
        raw_data_row = file.readline()
    print(len(x_data))
    print(x_data)
    return (x_data, y_data)
    
def create_all_cpu_arrays_2(file):
    raw_data_row = raw_data.readline()
    while (raw_data_row[0:3] != "165"):
        raw_data_row = file.readline()
    x_data = []
    y_data = []
    raw_row_array = comma(raw_data_row)
    x_min = raw_row_array[0]
    print(x_min)
    while (raw_data_row[:3] == "165"):
        raw_row_array = comma(raw_data_row)
        if (int(raw_row_array[1]) > 1 and int(raw_row_array[2]) > 1 and int(raw_row_array[3]) > 1 and int(raw_row_array[4]) > 1):
            x_data.append(int(raw_row_array[0] - x_min))
            y_data.append(raw_row_array[2] + raw_row_array[3])
        raw_data_row = file.readline()
    print(len(x_data))
    print(x_data)
    return (x_data, y_data)

print("start program")
(x2, y2) = create_all_cpu_arrays(raw_data)
(x1, y1) = create_all_data_arrays(raw_data)
(x2_2, y2_2) = create_all_cpu_arrays_2(raw_data)
(x1_2, y1_2) = create_all_data_arrays(raw_data)



# Plot error bar
plt.figure(figsize=(15, 10))
fig, ax = plt.subplots()

plt.plot(x1[0], y1[0], label="latency [ms]", color="blue")

plt.xlabel("Time [s]")
plt.ylabel("95th percentile latency [ms]")
plt.xlim(0, 160)
plt.yticks(color="blue")
plt.xticks([0, 50, 100, 150], ['0', '50', '100', '150'])
plt.ylim(0, 2)
plt.title("Memcached performance for 2 threads and 1 core over time")
#plt.legend(loc="upper left")
plt.grid()

ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('CPU usage [%]')  # we already handled the x-label with ax1
ax2.plot(x2, y2, color="red", label="CPU usage [%]")
ax2.tick_params(axis='y', labelcolor="red")
ax2.set_ylim([0, 100])

# Display graph

pylab.savefig('plot4_1d_1.png')
plt.show()


plt.figure(figsize=(15, 10))
fig, ax = plt.subplots()

plt.plot(x1_2[0], y1_2[0], label="latency [ms]", color="blue")

plt.xlabel("Time [s]")
plt.ylabel("95th percentile latency [ms]")
plt.xlim(0, 160)
plt.yticks(color="blue")
plt.xticks([0, 50, 100, 150], ['0', '50', '100', '150'])
plt.ylim(0, 2)
plt.title("Memcached performance for 2 threads and 2 cores over time")
#plt.legend(loc="upper left")
plt.grid()

ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('CPU usage [%]')  # we already handled the x-label with ax1
ax2.plot(x2_2, y2_2, color="red", label="CPU usage [%]")
ax2.tick_params(axis='y', labelcolor="red")
ax2.set_ylim([0, 200])

# Display graph

pylab.savefig('plot4_1d_2.png')
plt.show()