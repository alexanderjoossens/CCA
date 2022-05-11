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
raw_data = open("raw_data.txt", "r")

def find_start_of_dataset(file):
    raw_data_row = raw_data.readline()
    while (raw_data_row[0:4] != "read"):
        raw_data_row = file.readline()
    return raw_data_row


# read QPS and p95 from file, store them in arrays for all runs
def create_data_arrays_per_run(first_row, file):
    x_data = []
    y_data = []
    i = 0
    while (first_row[:4] == "read"):
        raw_row_array = comma(first_row[4:])
        x_data.append(i*20)
        i += 1
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
        x_data.append(run1[0][i])
        y_data.append(run1[1][i] / 1000)
    return (x_data, y_data)

# get data from raw data for each benchmark
def create_all_data_arrays(file):
    x_data_arrays = []
    y_data_arrays = []
    (x, y) = create_avg_data_arrays(raw_data)
    x_data_arrays.append(x)
    y_data_arrays.append(y)
    return (x_data_arrays, y_data_arrays)

(x1, y1) = create_all_data_arrays(raw_data)



# Plot error bar
plt.figure(figsize=(15, 10))

plt.plot(x1[0], y1[0], marker="o", label="Run 1")
plt.axvline(x = 20, color = 'r', linestyle = '-')
plt.text(20, .1, ' start of all parsec jobs')


plt.xlabel("Time [s]")
plt.ylabel("95th percentile latency [ms]")
plt.xlim(0, 250)
plt.xticks([0, 20, 50, 100, 150, 200, 250, 300], ['0', '20', '50', '100', '150', '200', '250', '300'])
plt.ylim(0, 1)
plt.title("95th percentile latency of memcached over time for the first run")
plt.legend(loc="upper right")
plt.grid()

# Display graph

pylab.savefig('plot1.png')
plt.show()

(x1, y1) = create_all_data_arrays(raw_data)

# Plot error bar
plt.figure(figsize=(15, 10))

plt.plot(x1[0], y1[0], marker="o", label="Run 2")
plt.axvline(x = 20, color = 'r', linestyle = '-')
plt.text(20, .1, ' start of all parsec jobs')


plt.xlabel("Time [s]")
plt.ylabel("95th percentile latency [ms]")
plt.xlim(0, 250)
plt.xticks([0, 20, 50, 100, 150, 200, 250, 300], ['0', '20', '50', '100', '150', '200', '250', '300'])
plt.ylim(0, 1)
plt.title("95th percentile latency of memcached over time for the second run")
plt.legend(loc="upper right")
plt.grid()

# Display graph

pylab.savefig('plot2.png')
plt.show()

(x1, y1) = create_all_data_arrays(raw_data)



# Plot error bar
plt.figure(figsize=(15, 10))

plt.plot(x1[0], y1[0], marker="o", label="Run 3")
plt.axvline(x = 20, color = 'r', linestyle = '-')
plt.text(20, .1, ' start of all parsec jobs')


plt.xlabel("Time [s]")
plt.ylabel("95th percentile latency [ms]")
plt.xlim(0, 250)
plt.xticks([0, 20, 50, 100, 150, 200, 250, 300], ['0', '20', '50', '100', '150', '200', '250', '300'])
plt.ylim(0, 1)
plt.title("95th percentile latency of memcached over time for the third run")
plt.legend(loc="upper right")
plt.grid()

# Display graph

pylab.savefig('plot3.png')
plt.show()
