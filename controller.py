import psutil
import docker
import json
import time

def start_controller():
    print('Starting controller')

    container_fft = client.containers.create('anakli/parsec:splash2x-fft-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p splash2x.fft -i native -n 2",
                                    cpuset_cpus="2-3",
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
                                    command="./bin/parsecmgmt -a run -p canneal -i native -n 2",
                                    cpuset_cpus="0-1",
                                    detach=True,
                                    name="parsec-canneal",
                                    )

    container_dedup = client.containers.create('anakli/parsec:dedup-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p dedup -i native -n 2",
                                    cpuset_cpus="0-1",
                                    detach=True,
                                    name="parsec-dedup",
                                    )
    container_blackscholes = client.containers.create('anakli/parsec:blackscholes-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p blackscholes -i native -n 2",
                                    cpuset_cpus="2-3",
                                    command="./bin/parsecmgmt -a run -p ferret -i native -n 2",
                                    cpuset_cpus="2-3",
                                    detach=True,
                                    name="parsec-ferret",
                                    )

    container_canneal = client.containers.create('anakli/parsec:canneal-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p canneal -i native -n 2",
                                    cpuset_cpus="0-1",
                                    detach=True,
                                    name="parsec-canneal",
                                    )

    container_dedup = client.containers.create('anakli/parsec:dedup-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p dedup -i native -n 2",
                                    cpuset_cpus="0-1",
                                    detach=True,
                                    name="parsec-dedup",
                                    )
    container_blackscholes = client.containers.create('anakli/parsec:blackscholes-native-reduced', 
                                    command="./bin/parsecmgmt -a run -p blackscholes -i native -n 2",
                                    cpuset_cpus="2-3",
                                    detach=True,
                                    name="parsec-blackscholes",
                                    )



    print("create containers done")
    start_time = time.time()
    highprio_task_list = [container_blackscholes, container_ferret, container_freqmine]
    lowprio_task_list = [container_fft, container_canneal, container_dedup]
    highprio_task = container_blackscholes
    lowprio_task = container_fft
    low_limit = 50
    high_limit = 60
    counter_time = time.time()

    while True:
        (cpu0, cpu1, cpu2, cpu3) = psutil.cpu_percent(interval=0.1, percpu=True)
        if (counter_time + 10 < time.time()):
            print("[" + str(cpu0) + " , " + str(cpu1) + " , " + str(cpu2) + " , " + str(cpu3) + "]")
            counter_time = time.time()

        if (highprio_task.status == "running"):
            continue

        elif (highprio_task.status == "exited"):
            try:
                highprio_task = highprio_task_list.pop()
                highprio_task.start()
                stop_time = time.time()
                duration = stop_time - start_time
                print("EXITED: ", highprio_task.name, " after ", duration, " time")
            except:
                continue

        elif (highprio_task.status == "created"):
            highprio_task.start()

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
                lowprio_task = lowprio_task_list.pop()
                lowprio_task.start()
                stop_time = time.time()
                duration = stop_time - start_time
                print("EXITED: ", lowprio_task, " after ", duration, " time")
            except:
                continue

        elif (lowprio_task.status == "created"):
            lowprio_task.start()

        elif (lowprio_task.status == "restarting"):
            continue

        elif (lowprio_task.status == "paused"):
            continue

        elif (lowprio_task.status == "dead"):
            print("Container DEAD: ", lowprio_task)

        if (cpu0 > high_limit and cpu1 > high_limit):
            lowprio_task.update(cpuset_cpus="1")
        if (cpu0 < low_limit and cpu1 < low_limit):
            lowprio_task.update(cpuset_cpus="0-1")

if __name__ == '__main__':

    client = docker.from_env()
    start_controller()
