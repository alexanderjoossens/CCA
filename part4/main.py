
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
raw_data = open("raw_data_2.txt", "r")

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
        x_data.append(raw_row_array[15])
        y_data.append(raw_row_array[11])
        first_row = file.readline()
    return (x_data, y_data)

# average data across 3 runs
def create_avg_data_arrays(file):
    raw_data_row = find_start_of_dataset(raw_data)
    run1 = create_data_arrays_per_run(raw_data_row, file)
    raw_data_row = find_start_of_dataset(raw_data)
    run2 = create_data_arrays_per_run(raw_data_row, file)
    raw_data_row = find_start_of_dataset(raw_data)
    run3 = create_data_arrays_per_run(raw_data_row, file)
    x_data = []
    y_data = []
    x_error = []
    y_error = []
    for i in range(len(run1[0])):
        x_data.append((run1[0][i] + run2[0][i] + run3[0][i]) / 3)
        y_data.append((run1[1][i] + run2[1][i] + run3[1][i]) / 3000)
        x_error.append(math.sqrt(((run1[0][i]-x_data[-1])**2 + (run2[0][i]-x_data[-1])**2 + (run2[0][i]-x_data[-1])**2))/2)
        y_error.append(math.sqrt(((run1[1][i]/1000-y_data[-1])**2 + (run2[1][i]/1000-y_data[-1])**2 + (run2[1][i]/1000-y_data[-1])**2))/2)
    return (x_data, y_data, x_error, y_error)

# get data from raw data for each benchmark
def create_all_data_arrays(file):
    x_data_arrays = []
    y_data_arrays = []
    x_error_arrays = []
    y_error_arrays = []
    for i in range(4):
        (x, y, x_err, y_err) = create_avg_data_arrays(raw_data)
        x_data_arrays.append(x)
        y_data_arrays.append(y)
        x_error_arrays.append(x_err)
        y_error_arrays.append(y_err)
    return (x_data_arrays, y_data_arrays, x_error_arrays, y_error_arrays)

(x1, y1, x1_err, y1_err) = create_all_data_arrays(raw_data)
print(x1_err[0])
print(y1_err[0])



# Plot error bar
plt.figure(figsize=(15, 10))

plt.errorbar(x1[0], y1[0], xerr=x1_err[0], yerr=y1_err[0], label="1 thread, 1 core", capsize=2)
plt.errorbar(x1[1], y1[1], xerr=x1_err[1], yerr=y1_err[1], label="1 thread, 2 cores", capsize=2)
plt.errorbar(x1[2], y1[2], xerr=x1_err[2], yerr=y1_err[2], label="2 threads, 1 core", capsize=2)
plt.errorbar(x1[3], y1[3], xerr=x1_err[3], yerr=y1_err[3], label="2 threads, 2 cores", capsize=2)

plt.xlabel("Queries per second [QPS]")
plt.ylabel("95th percentile latency [ms]")
plt.xlim(0, 130000)
plt.xticks([0, 20000, 40000, 60000, 80000, 100000, 120000], ['0', '20K', '40K', '60K', '80K', '100K', '120K'])
plt.ylim(0, 2.5)
plt.title("Memcached performance for different numbers of threads and cores, each averaged across 3 runs")
plt.legend(loc="upper left")
plt.grid()

# Display graph

pylab.savefig('plot4_try2.png')
plt.show()
