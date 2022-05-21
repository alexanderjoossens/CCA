import psutil
import docker
import json
import time
import os


def start_controller():
    print('Starting controller')
    os.system("sudo usermod -a -G docker ubuntu")
    container_blackscholes = os.system('docker run --cpuset-cpus="0" -d --rm --name parsec anakli/parsec:blackscholes-native-reduced ./bin/parsecmgmt -a run -p blackscholes -i native -n 2')

    container_fft = client.containers.create('anakli/parsec:splash2x-fft-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p splash2x.fft -i native -n 1",
                                    cpuset_cpus="1",
                                    detach=True,
                                    name="parsec-fft",
                                    )
    
    container_freqmine = client.containers.create('anakli/parsec:freqmine-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p freqmine -i native -n 2",
                                    cpuset_cpus="2-3",
                                    detach=True,
                                    name="parsec-freqmine",
                                    )

    container_ferret = client.containers.create('anakli/parsec:ferret-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p ferret -i native -n 2",
                                    cpuset_cpus="2-3",
                                    detach=True,
                                    name="parsec-ferret",
                                    )

    container_canneal = client.containers.create('anakli/parsec:canneal-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p canneal -i native -n 1",
                                    cpuset_cpus="1",
                                    detach=True,
                                    name="parsec-canneal",
                                    )

    container_dedup = client.containers.create('anakli/parsec:dedup-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p dedup -i native -n 1",
                                    cpuset_cpus="1",
                                    detach=True,
                                    name="parsec-dedup",
                                    )
    #container_blackscholes = client.containers.create('anakli/parsec:blackscholes-native-reduced', 
                                    #command="./bin/parsecmgmt -a run -p blackscholes -i native -n 2",
                                    #cpuset_cpus="2-3",
                                    #detach=True,
                                    #name="parsec-blackscholes",
                                    #)


    print("create containers done")
    start_time = time.time()
    print(start_time)
    highprio_task_list = [container_ferret, container_freqmine]
    lowprio_task_list = [container_fft, container_canneal, container_dedup]
    highprio_task = container_blackscholes
    lowprio_task = lowprio_task_list.pop(0)
    low_limit = 50
    high_limit = 60
    counter_time = time.time()
    memcached_name = "memcached"
    memcached_pid = None

    for proc in psutil.process_iter():
        if memcached_name in proc.name():
            memcached_pid = proc.pid

    print(memcached_pid)
    print(highprio_task.status)
    #highprio_task.start()
    start_highprio_task = time.time()
    print("STARTED: " + highprio_task.name + " at " + str(start_highprio_task) + "["+ highprio_task.status + "]")

    lowprio_task.start()
    start_lowprio_task = time.time()
    print("STARTED: " + lowprio_task.name + " at " + str(start_lowprio_task))

    while True:
        (cpu0, cpu1, cpu2, cpu3) = psutil.cpu_percent(interval=0.1, percpu=True)
        if (counter_time + 10 < time.time()):
            print("[" + str(cpu0) + " , " + str(cpu1) + " , " + str(cpu2) + " , " + str(cpu3) + "]")
            print("High priority task: " + highprio_task.name + " in state " + highprio_task.status + " and low proirity task: " + lowprio_task.name + " in state " + lowprio_task.status)
            print("High priority task list: " + str(highprio_task_list))
            print("Low priority task list: " + str(lowprio_task_list))
            counter_time = time.time()

        if (highprio_task.status == "running"):
            continue

        elif (highprio_task.status == "exited"):
            try:
                high_stop_time = time.time()
                high_duration = high_stop_time - start_highprio_task
                print("EXITED: " + highprio_task.name + " after " + str(high_duration) + " time, started at: " + str(start_highprio_task))
                highprio_task = highprio_task_list.pop(0)
                highprio_task.start()
                start_highprio_task = time.time()
                print("STARTED: " + highprio_task.name + " at " + str(start_highprio_task))
            except:
                continue

        elif (highprio_task.status == "created"):
            #highprio_task.start()
            #start_highprio_task = time.time()
            #print("STARTED: " + highprio_task.name + " at " + str(start_highprio_task))
            continue
            

        elif (highprio_task.status == "restarting"):
            continue

        elif (highprio_task.status == "paused"):
            continue

        elif (highprio_task.status == "dead"):
            print("Container DEAD: ", highprio_task)



        if (lowprio_task.status == "running"):
            continue

        elif (lowprio_task.status == "exited"):
            try:
                low_stop_time = time.time()
                low_duration = low_stop_time - start_lowprio_task
                print("EXITED: " + lowprio_task.name + " after " + str(low_duration) + " time, started at: " + str(start_lowprio_task))
                lowprio_task = lowprio_task_list.pop(0)
                lowprio_task.start()
                start_lowprio_task = time.time()
                print("STARTED: " + lowprio_task.name + " at " + str(start_lowprio_task))
            except:
                continue

        elif (lowprio_task.status == "created"):
            #lowprio_task.start()
            #start_lowprio_task = time.time()
            #print("STARTED: " + lowprio_task.name + " at " + str(start_lowprio_task))
            continue

        elif (lowprio_task.status == "restarting"):
            continue

        elif (lowprio_task.status == "paused"):
            continue

        elif (lowprio_task.status == "dead"):
            print("Container DEAD: ", lowprio_task)

        if (cpu0 > 80):
            os.system("taskset -a -cp 0-1 " + str(memcached_pid) + " >/dev/null 2>&1")
            print("MEMCACHED: number of cores changed to 2 at " + str(time.time()))
        elif (cpu0 < 30):
            os.system("taskset -a -cp 0 " + str(memcached_pid) + " >/dev/null 2>&1")
            print("MEMCACHED: number of cores changed to 1 at " + str(time.time()))


if __name__ == '__main__':

    client = docker.from_env()
    start_controller()
