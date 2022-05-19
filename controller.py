import docker

def start_controller():
    print(f'Starting controller\n')

    container = client.containers.run('bfirsh/reticulate-splines',
                                      detach=True)
    container.logs()

    #create containers
    client.containers.create()

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
    client.containers.run('alpine', 'echo hello world')
    start_controller()

