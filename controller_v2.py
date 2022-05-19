import psutil
import time
import json


print('Starting measurment')
f = open("cpu_usage.txt", "a")

while True:
    current_time = time.time()
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    f.write(str(current_time) + " " + str(cpu_usage[0]) + " " + str(cpu_usage[1]) + " " + str(cpu_usage[2]) + " " + str(cpu_usage[3]) + "\n")
    
    


