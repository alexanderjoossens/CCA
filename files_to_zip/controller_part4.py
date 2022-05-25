import psutil
import docker
import time
import os

# Functions to start each docker container
def start_fft():
    container_fft = os.popen('docker run --cpuset-cpus="1" -d --name parsec-fft anakli/parsec:splash2x-fft-native-reduced ./bin/parsecmgmt -a run -p splash2x.fft -i native -n 1').read()
    return client.containers.get(str(container_fft)[:12])

def start_freqmine():
    container_freqmine = os.popen('docker run --cpuset-cpus="2-3" -d --name parsec-freqmine anakli/parsec:freqmine-native-reduced ./bin/parsecmgmt -a run -p freqmine -i native -n 3').read()
    return client.containers.get(str(container_freqmine)[:12])

def start_ferret():
    container_ferret = os.popen('docker run --cpuset-cpus="2-3" -d --name parsec-ferret anakli/parsec:ferret-native-reduced ./bin/parsecmgmt -a run -p ferret -i native -n 3').read()
    return client.containers.get(str(container_ferret)[:12])

def start_canneal():
    container_canneal = os.popen('docker run --cpuset-cpus="1" -d --name parsec-canneal anakli/parsec:canneal-native-reduced ./bin/parsecmgmt -a run -p canneal -i native -n 1').read()
    return client.containers.get(str(container_canneal)[:12])

def start_dedup():
    container_dedup = os.popen('docker run --cpuset-cpus="1" -d --name parsec-dedup anakli/parsec:dedup-native-reduced ./bin/parsecmgmt -a run -p dedup -i native -n 1').read()
    return client.containers.get(str(container_dedup)[:12])

def start_blackscholes():
    container_blackscholes = os.popen('docker run --cpuset-cpus="2-3" -d --name parsec-blackscholes anakli/parsec:blackscholes-native-reduced ./bin/parsecmgmt -a run -p blackscholes -i native -n 2').read()
    return client.containers.get(str(container_blackscholes)[:12])

# Controller
def start_controller():
    print('Starting controller')
    start_time = time.time()
    print(start_time)

    # Keep a list of tasks that use more or less resources, respectively
    highprio_task_list = [start_ferret, start_freqmine]
    lowprio_task_list = [start_canneal, start_dedup]

    # start the first task which uses much resources
    highprio_task = start_blackscholes()
    start_highprio_task = time.time()
    print("STARTED: " + highprio_task.name + " " + str(start_highprio_task))

    # start the first task which uses few resources
    lowprio_task = start_fft()
    start_lowprio_task = time.time()
    print("STARTED: " + lowprio_task.name + " " + str(start_lowprio_task))

    # define a counter to print the measurements every 10 seconds
    counter_time = time.time()

    # Get memcached process id to change number of cores afterwards (taskset)
    memcached_name = "memcached"
    memcached_pid = None

    for proc in psutil.process_iter():
        if memcached_name in proc.name():
            memcached_pid = proc.pid

    print(memcached_pid)
    memcached_state = 0

    os.system("docker inspect -f '{{.State.Status}}' " + highprio_task.name)
    print(highprio_task.status)

    # Booleans to check if all high or low priority jobs have finished
    high_list_finished = 0
    low_list_finished = 0

    # Start of control loop
    while True:
        # Measure CPU usage
        (cpu0, cpu1, cpu2, cpu3) = psutil.cpu_percent(interval=0.1, percpu=True)
        # Get the state of the current high priority and low priority containers
        highprio_state = os.popen("docker inspect -f '{{.State.Status}}' " + highprio_task.name).read()
        lowprio_state = os.popen("docker inspect -f '{{.State.Status}}' " + lowprio_task.name).read()
        # Print statistics every 10 seconds
        if (counter_time + 10 < time.time()):
            print("[" + str(cpu0) + " , " + str(cpu1) + " , " + str(cpu2) + " , " + str(cpu3) + "]")
            print("High priority task: " + highprio_task.name + " in state " + highprio_state + " and low proirity task: " + lowprio_task.name + " in state " + lowprio_state)
            print("High priority task list: " + str(len(highprio_task_list)))
            print("Low priority task list: " + str(len(lowprio_task_list)))
            counter_time = time.time()

        # Decide on highpriority task's state
        # If state has changed to exited: start next job if available
        # If all low priority tasks have already finished, use core 1 additionally
        if (highprio_state[:7] == "running"):
            pass

        elif (highprio_state[:6] == "exited" and high_list_finished == 0):
            try:
                high_stop_time = time.time()
                high_duration = high_stop_time - start_highprio_task
                print("EXITED: " + highprio_task.name + " " + str(high_duration) + " " + str(start_highprio_task))
                highprio_task = highprio_task_list.pop(0)()
                if (low_list_finished == 1):
                    os.system("docker update --cpuset-cpus 1-3 " + highprio_task.id)
                start_highprio_task = time.time()
                print("STARTED: " + highprio_task.name + " " + str(start_highprio_task))
            except:
                high_list_finished = 1
                print("High exception at exit")

        elif (highprio_state == "created"):
            pass
            
        elif (highprio_state == "restarting"):
            pass

        elif (highprio_state == "paused"):
            pass

        elif (highprio_state[:4] == "dead"):
            print("Container DEAD: " + highprio_task.name)



        if (lowprio_state[:7] == "running"):
            pass

        # Decide on lowpriority task's state
        # If state has changed to exited: start next job if available
        # If no lowpriority job is available, assign core 1 (which is no longer running lowpriority tasks) to the current highpriority task
        elif (lowprio_state[:6] == "exited" and low_list_finished == 0):
            try:
                low_stop_time = time.time()
                low_duration = low_stop_time - start_lowprio_task
                print("EXITED: " + lowprio_task.name + " " + str(low_duration) + " " + str(start_lowprio_task))
                lowprio_task = lowprio_task_list.pop(0)()
                start_lowprio_task = time.time()
                print("STARTED: " + lowprio_task.name + " " + str(start_lowprio_task))
            except:
                low_list_finished = 1
                print("Low exception at exit")
                os.system("docker update --cpuset-cpus 1-3 " + highprio_task.id)

        elif (lowprio_state[:7] == "created"):
            pass

        elif (lowprio_state == "restarting"):
            pass

        elif (lowprio_state == "paused"):
            pass

        elif (lowprio_state[:4] == "dead"):
            print("Container DEAD: " + lowprio_task.name)

        # If the CPU0 running memcached has a usage of over 90%, pause the lowpriority job on core 1 or move the highpriority task to cores 2 and 3 (if lowpriority tasks have finished)
        if (cpu0 > 90):
            if (low_list_finished == 0):
                os.system("docker pause " + lowprio_task.id + " >/dev/null 2>&1")
                print("PAUSED: " + lowprio_task.name + " " + str(time.time()))
            else:
                os.system("docker update --cpuset-cpus 2-3 " + highprio_task.id)
                print("UPDATE: 2-3cores" + highprio_task.name + " " + str(time.time() - start_time))
        # If the combined CPU usage of CPU0 and CPU1 drops below 75, we unpause the lowpriority task again or assign the additional core 1 to the highpriority task, respectively
        elif (cpu0 + cpu1 < 75):
            if (low_list_finished == 0):
                os.system("docker unpause " + lowprio_task.id + " >/dev/null 2>&1")
                print("UNPAUSED: " + lowprio_task.name + " " + str(time.time()))
            else:
                os.system("docker update --cpuset-cpus 1-3 " + highprio_task.id)
                print("UPDATE: 1-3cores" + highprio_task.name + " " + str(time.time() - start_time))

        # If the CPU usage of core 0 increases to more than 60%, we assign core 1 to memcached as well.
        # Additionally, we assign half of the CPU shares to the parsec job and half to memcached
        if ((cpu0 > 60) and (memcached_state == 0)):
            os.system("taskset -a -cp 0-1 " + str(memcached_pid) + " >/dev/null 2>&1")
            if (low_list_finished == 0):
                os.system("docker update --cpu-shares 512 " + lowprio_task.id)
            else:
                os.system("docker update --cpu-shares 512 " + highprio_task.id)
            print("MEMCACHED: 2 " + str(time.time()))
            memcached_state = 1
        # If the CPU usage for CPU0 drops below 30% again, we move memcached back to core 0 and assign full CPU shares to the parsec job running on core 1
        elif ((cpu0 < 30) and (memcached_state == 1)):
            os.system("taskset -a -cp 0 " + str(memcached_pid) + " >/dev/null 2>&1")
            if (low_list_finished == 0):
                os.system("docker update --cpu-shares 1024 " + lowprio_task.id)
            else:
                os.system("docker update --cpu-shares 1024 " + highprio_task.id)
            print("MEMCACHED: 1 " + str(time.time()))
            memcached_state = 0


if __name__ == '__main__':
    os.system("sudo usermod -a -G docker ubuntu")
    client = docker.from_env()
    start_controller()
