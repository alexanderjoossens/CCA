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

    


    stats_fft = container_fft.stats(decode=True)
    with open('stats_fft.txt', 'w') as stats_file:
        stats_file.write(json.dumps(stats_fft))

    container_fft.update(cpuset_cpus="0-2")


if __name__ == '__main__':

    client = docker.from_env()
    start_controller()

