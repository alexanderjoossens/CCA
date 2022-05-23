
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
import matplotlib.colors as mcolors

from matplotlib import pylab


def comma(inputs):
    with_commas = re.sub("\s+", ",", inputs.strip()).split(',')
    return list(map(float,with_commas))

def comma_str(inputs):
    with_commas = re.sub("\s+", ",", inputs.strip()).split(',')
    return list(with_commas)

#upperlimits = [True, False] * 5
#lowerlimits = [False, True] * 5

# open file with raw data, go to first line with data
raw_data = open("raw_data_4_3_1.txt", "r")

def find_start_of_dataset(file, start_str):
    raw_data_row = raw_data.readline()
    while (raw_data_row[0:len(start_str)] != start_str):
        raw_data_row = file.readline()
        if (raw_data_row == ""):
            break
    return raw_data_row


# read QPS and p95 from file, store them in arrays for all runs
def create_data_arrays_per_run(first_row, file):
    x_data = []
    y_data = []
    z_data = []
    while (first_row[:4] == "read"):
        raw_row_array = comma(first_row[4:])
        z_data.append(raw_row_array[15])    # qps
        y_data.append(raw_row_array[11])    # 95 latency
        #x_data.append(raw_row_array[17])    # start time
        first_row = file.readline()
    return (x_data, y_data, z_data)

# average data across 3 runs
def create_avg_data_arrays(file):
    raw_data_row = find_start_of_dataset(raw_data, "read")
    run1 = create_data_arrays_per_run(raw_data_row, file)
    x_data = []
    y_data = []
    z_data = []
    for i in range(len(run1[1])):
        x_data.append(10*i)
        y_data.append((run1[1][i]) / 1000)
        z_data.append(run1[2][i])
    return (x_data, y_data, z_data)

# get data from raw data for each benchmark
def create_all_data_arrays(file):
    print("create_all_data_arrays")
    x_data_arrays = []
    y_data_arrays = []
    z_data_arrays = []
    for i in range(1):
        (x, y, z) = create_avg_data_arrays(raw_data)
        x_data_arrays.append(x)
        y_data_arrays.append(y)
        z_data_arrays.append(z)
    return (x_data_arrays, y_data_arrays, z_data_arrays)

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
            x_data.append((int(raw_row_array[0] - x_min)) * 120000/160)
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
            x_data.append((int(raw_row_array[0] - x_min)) * 120000/160)
            y_data.append(raw_row_array[2] + raw_row_array[3])
        raw_data_row = file.readline()
    print(len(x_data))
    print(x_data)
    return (x_data, y_data)

def find_times(file, start_time, line_str):
    starting_times = []
    for i in range(6):
        starting_row = find_start_of_dataset(file, line_str)
        starting_array = comma_str(starting_row)
        print(starting_array)
        starting_times.append((starting_array[1], (float(starting_array[2]) - start_time)))
    return starting_times

def find_pause_times(file, start_time, line_str):
    starting_times = []
    starting_row = "a"
    while (True):
        starting_row = find_start_of_dataset(file, line_str)
        if (starting_row == ""):
            break
        starting_array = comma_str(starting_row)
        print(starting_array)
        starting_times.append((starting_array[1], (float(starting_array[2]) - start_time)))
    return starting_times

def find_memcached_times(file, start_time, line_str):
    starting_times = []
    cores = []
    starting_row = "a"
    while (True):
        starting_row = find_start_of_dataset(file, line_str)
        if (starting_row == ""):
            break
        starting_array = comma_str(starting_row)
        print(starting_array)
        starting_times.append(float(starting_array[2]) - start_time)
        cores.append(int(starting_array[1]))
    return (starting_times, cores)


print("start program")
total_start_time = int(comma_str(find_start_of_dataset(raw_data, "Timestamp start"))[-1])
print(total_start_time)

(x1, y1, z1) = create_all_data_arrays(raw_data)
# get timestamps of started/paused/unpaused/exited jobs
starting_times = find_times(raw_data, total_start_time/1000, "STARTED:")
print(starting_times)

raw_data.close()
raw_data = open("raw_data_4_3_1.txt", "r")
paused_times = find_pause_times(raw_data, total_start_time/1000, "PAUSED:")
print(paused_times)
raw_data.close()
raw_data = open("raw_data_4_3_1.txt", "r")
unpaused_times = find_pause_times(raw_data, total_start_time/1000, "UNPAUSED:")
print(unpaused_times)
#(x1_2, y1_2, z1_2) = create_all_data_arrays(raw_data)

raw_data.close()
raw_data = open("raw_data_4_3_1.txt", "r")
memcached_cores = find_memcached_times(raw_data, total_start_time/1000, "MEMCACHED:")
print(memcached_cores)



# Plot error bar
plt.figure(figsize=(15, 10))
fig, ax = plt.subplots()

plt.plot(x1[0], y1[0], label="latency [ms]", color="blue")

plt.xlabel("Time [s]")
plt.ylabel("95th percentile latency [ms]")
plt.yticks(color="blue")
plt.xlim(0, 1800)
plt.xticks([0, 500, 1000, 1500, 1800], 
            ['0', '500', '1000', '1500', '1800'])
plt.ylim(0, 2.5)
plt.title("1A: Memcached performance over time")
plt.axhline(y=1.5, linestyle='dotted', color="red")
plt.text(1470, 1.52, "Latency SLO")

colors = {
            "parsec-fft": "blue", 
            "parsec-canneal": "orange", 
            "parsec-dedup": "purple", 
            "parsec-ferret": "brown", 
            "parsec-freqmine": "olive", 
            "parsec-blackscholes": "gray"}
for i in range(len(starting_times)):
    plt.axvline(x=starting_times[i][1], color=colors[starting_times[i][0]], label=starting_times[i][0], linestyle="solid")
for i in range(len(paused_times)):
    plt.axvline(x=paused_times[i][1], color=colors[paused_times[i][0]], linestyle=":")
for i in range(len(unpaused_times)):
    plt.axvline(x=unpaused_times[i][1], color=colors[unpaused_times[i][0]], linestyle=":")

#plt.legend(loc="upper left")
plt.grid()
plt.gcf().set_size_inches(15, 10)

ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Queries per second [QPS]')  # we already handled the x-label with ax1
ax2.plot(x1[0], z1[0], color="green", label="QPS")
ax2.tick_params(axis='y', labelcolor="green")
ax2.set_ylim([0, 100000])
ax2.set_yticks([0, 20000, 40000, 60000, 80000, 100000], ['0', '20K', '40K', '60K', '80K', '100K'])

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
#ax.legend(h1+h2, l1+l2, loc="upper right")
ax.legend(h1+h2, l1+l2, loc='lower center', bbox_to_anchor=(0.5, -0.15), fancybox=True, ncol=3)

fig.set_tight_layout(True)

# Display graph

pylab.savefig('plot4_3_A.png')
#plt.show()





plt.figure(figsize=(15, 10))
fig, ax = plt.subplots()

plt.plot(memcached_cores[0], memcached_cores[1], label="CPU cores", color="blue", linestyle="", marker="x")

plt.xlabel("Time[s]")
plt.ylabel("Number of CPU cores assigned to memcached")
plt.yticks(color="blue")
plt.xlim(0, 1800)
plt.xticks([0, 500, 1000, 1500, 1800], 
            ['0', '500', '1000', '1500', '1800'])
plt.ylim(0, 2.5)
plt.title("1B: Memcached performance over time")


colors = {
            "parsec-fft": "blue", 
            "parsec-canneal": "orange", 
            "parsec-dedup": "purple", 
            "parsec-ferret": "brown", 
            "parsec-freqmine": "olive", 
            "parsec-blackscholes": "gray"}
for i in range(len(starting_times)):
    plt.axvline(x=starting_times[i][1], color=colors[starting_times[i][0]], label=starting_times[i][0], linestyle="solid")
for i in range(len(paused_times)):
    plt.axvline(x=paused_times[i][1], color=colors[paused_times[i][0]], linestyle=":")
for i in range(len(unpaused_times)):
    plt.axvline(x=unpaused_times[i][1], color=colors[unpaused_times[i][0]], linestyle=":")
    
#plt.legend(loc="upper left")
plt.grid()
plt.gcf().set_size_inches(15, 10)

ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Queries per second [QPS]')  # we already handled the x-label with ax1
ax2.plot(x1[0], z1[0], color="green", label="QPS")
ax2.tick_params(axis='y', labelcolor="green")
ax2.set_ylim([0, 100000])
ax2.set_yticks([0, 20000, 40000, 60000, 80000, 100000], ['0', '20K', '40K', '60K', '80K', '100K'])

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, loc="upper right")

fig.set_tight_layout(True)

# Display graph

pylab.savefig('plot4_3_B.png')
plt.show()