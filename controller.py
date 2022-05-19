import docker
import json

def start_controller():
    print(f'Starting controller\n')

    container_fft = client.containers.run('anakli/parsec:splash2x-fft-native-reduced', 
                                    command=["-c", "./bin/parsecmgmt -a run -p splash2x.fft -i native -n 1"],       # CHANGE n (number of threads) at beginning
                                    cpuset_cpus="0-1",                                                              # CHANGE
                                    detach=True,
                                    name="parsec-fft",
                                    remove=True)

    container_freqmine = client.containers.run('anakli/parsec:freqmine-native-reduced', 
                                    command=["-c", "./bin/parsecmgmt -a run -p freqmine -i native -n 1"],
                                    cpuset_cpus="0-1",                                                              # CHANGE
                                    detach=True,
                                    name="parsec-freqmine",
                                    remove=True)

    container_ferret = client.containers.run('anakli/parsec:ferret-native-reduced', 
                                    command=["-c", "./bin/parsecmgmt -a run -p ferret -i native -n 1"],
                                    cpuset_cpus="0-1",                                                              # CHANGE
                                    detach=True,
                                    name="parsec-ferret",
                                    remove=True)

    container_canneal = client.containers.run('anakli/parsec:canneal-native-reduced', 
                                    command=["-c", "./bin/parsecmgmt -a run -p canneal -i native -n 1"],
                                    cpuset_cpus="0-1",                                                              # CHANGE
                                    detach=True,
                                    name="parsec-canneal",
                                    remove=True)

    container_dedup = client.containers.run('anakli/parsec:dedup-native-reduced', 
                                    command=["-c", "./bin/parsecmgmt -a run -p dedup -i native -n 1"],
                                    cpuset_cpus="0-1",                                                              # CHANGE
                                    detach=True,
                                    name="parsec-dedup",
                                    remove=True)

    container_blackscholes = client.containers.run('anakli/parsec:blackscholes-native-reduced', 
                                    command=["-c", "./bin/parsecmgmt -a run -p blackscholes -i native -n 1"],
                                    cpuset_cpus="0-1",                                                              # CHANGE
                                    detach=True,
                                    name="parsec-blackscholes",
                                    remove=True)


    stats_fft = container_fft.stats(decode=True)
    with open('stats_fft.txt', 'w') as stats_file:
        stats_file.write(json.dumps(stats_fft))

    container_fft.update(cpuset_cpus="0")






    #list and manage containers
    for container in client.containers.list():
        print(container.id)

    #create containers
    client.containers.create()

    # stop all running containers
    for container in client.containers.list():
        container.stop()

    #print the logs of a specific container
    container = client.containers.get('f1064a8a4c82')
    print(container.logs())

    # to see CPU usage use
    # bash command:
    # docker run --cpuset-cpus="0" -d --rm --name parsec \
    # anakli/parsec:blackscholes-native-reduced \
    # ./bin/parsecmgmt -a run -p blackscholes -i native -n 2
    client.containers.run(cpuset_cpus=0, detach=True, remove=Tre, name="Parsec", threads="2")

    while (cpu usage is smaller than a certain value)
        ...


if __name__ == '__main__':

    client = docker.from_env()
    #client.containers.run('alpine', 'echo hello world')
    start_controller()

