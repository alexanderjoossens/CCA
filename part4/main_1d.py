
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
    time_start = []
    time_end = []
    while (first_row[:4] == "read"):
        raw_row_array = comma(first_row[4:])
        x_data.append(raw_row_array[15])
        y_data.append(raw_row_array[11])
        time_start.append(raw_row_array[-2])
        time_end.append(raw_row_array[-1])
        first_row = file.readline()
    return (x_data, y_data, time_start, time_end)

# average data across 3 runs
def create_avg_data_arrays(file):
    raw_data_row = find_start_of_dataset(raw_data)
    run1 = create_data_arrays_per_run(raw_data_row, file)
    x_data = []
    y_data = []
    time_start = []
    time_end = []
    for i in range(len(run1[0])):
        x_data.append(run1[0][i])
        y_data.append((run1[1][i]) / 1000)
        time_start.append(run1[2][i])
        time_end.append(run1[3][i])
    return (x_data, y_data, time_start, time_end)

# get data from raw data for each benchmark
def create_all_data_arrays(file):
    x_data_arrays = []
    y_data_arrays = []
    time_start_arrays = []
    time_end_arrays = []
    for i in range(1):
        (x, y, time_start, time_end) = create_avg_data_arrays(raw_data)
        x_data_arrays.append(x)
        y_data_arrays.append(y)
        time_start_arrays.append(time_start)
        time_end_arrays.append(time_end)
    return (x_data_arrays, y_data_arrays, time_start_arrays, time_end_arrays)

def create_all_cpu_arrays(file, qps, start, end):
    raw_data_row = raw_data.readline()
    while (raw_data_row[0:3] != "165"):
        raw_data_row = file.readline()
    x_data = []
    y_data = [0] * len(qps)
    raw_row_array = comma(raw_data_row)
    x_min = raw_row_array[0]
    i = 0
    n_values = 0
    while (raw_data_row[:3] == "165" and i < len(start)):
        raw_row_array = comma(raw_data_row)
        if (raw_row_array[0] * 1000 >= start[i] and raw_row_array[0] * 1000 <= end[i]):
            if (i > 10 and raw_row_array[2] < 5):
                pass
            else:
                y_data[i] += raw_row_array[2]
                n_values += 1
        elif (raw_row_array[0] * 1000 < start[i]):
            pass
        elif (raw_row_array[0] * 1000 > end[i]):
            if (n_values > 0):
                y_data[i] /= n_values
            i += 1
            n_values = 0
        raw_data_row = file.readline()
    return (x_data, y_data)
    
def create_all_cpu_arrays_2(file, qps, start, end):
    raw_data_row = raw_data.readline()
    while (raw_data_row[0:3] != "165"):
        raw_data_row = file.readline()
    x_data = []
    y_data = [0] * len(qps)
    raw_row_array = comma(raw_data_row)
    x_min = raw_row_array[0]
    i = 0
    n_values = 0
    while (raw_data_row[:3] == "165" and i < len(start)):
        raw_row_array = comma(raw_data_row)
        if (raw_row_array[0] * 1000 >= start[i] and raw_row_array[0] * 1000 <= end[i]):
            if (i > 10 and raw_row_array[2] < 5):
                pass
            else:
                y_data[i] += raw_row_array[2] + raw_row_array[3]
                n_values += 1
        elif (raw_row_array[0] * 1000 < start[i]):
            pass
        elif (raw_row_array[0] * 1000 > end[i]):
            if (n_values > 0):
                y_data[i] /= n_values
            i += 1
            n_values = 0
        raw_data_row = file.readline()
    return (x_data, y_data)

print("start program")
(x1, y1, time_start1, time_end1) = create_avg_data_arrays(raw_data)
(x2, y2) = create_all_cpu_arrays(raw_data, x1, time_start1, time_end1)
(x1_2, y1_2, time_start2, time_end2) = create_avg_data_arrays(raw_data)
(x2_2, y2_2) = create_all_cpu_arrays_2(raw_data, x1_2, time_start2, time_end2)


# Plot error bar
plt.figure(figsize=(15, 10))
fig, ax = plt.subplots()

plt.plot(x1, y1, label="latency [ms]", color="blue")

plt.xlabel("Queries per second [QPS]")
plt.ylabel("95th percentile latency [ms]")
plt.yticks(color="blue")
plt.xlim(0, 120000)
plt.xticks([0, 20000, 40000, 60000, 80000, 100000, 120000], ['0', '20K', '40K', '60K', '80K', '100K', '120K'])
plt.ylim(0, 2)
plt.title("Memcached performance for 2 threads and 1 core")
plt.axhline(y=1.5, linestyle='dotted', color="red")
plt.text(1000, 1.52, "Latency SLO")
#plt.legend(loc="upper left")
plt.grid()

ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('CPU usage [%]')  # we already handled the x-label with ax1
ax2.plot(x1, y2, color="green", label="CPU usage [%]")
ax2.tick_params(axis='y', labelcolor="green")
ax2.set_ylim([0, 100])

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, loc="upper left")

# Display graph

pylab.savefig('plot4_1d_1.png')
plt.show()


plt.figure(figsize=(15, 10))
fig, ax = plt.subplots()

plt.plot(x1_2, y1_2, label="latency [ms]", color="blue")

plt.xlabel("Queries per second [QPS]")
plt.ylabel("95th percentile latency [ms]")
plt.yticks(color="blue")
plt.xlim(0, 120000)
plt.xticks([0, 20000, 40000, 60000, 80000, 100000, 120000], ['0', '20K', '40K', '60K', '80K', '100K', '120K'])
plt.ylim(0, 2)
plt.title("Memcached performance for 2 threads and 2 cores")
plt.axhline(y=1.5, linestyle='dotted', color="red")
plt.text(1000, 1.52, "Latency SLO")
#plt.legend(loc="upper left")
plt.grid()

ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('CPU usage [%]')  # we already handled the x-label with ax1
ax2.plot(x1_2, y2_2, color="green", label="CPU usage [%]")
ax2.tick_params(axis='y', labelcolor="green")
ax2.set_ylim([0, 200])

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, loc="upper left")
# Display graph

pylab.savefig('plot4_1d_2.png')
plt.show()