import docker

def start_controller():
    print(f'Starting controller\n')

    container = client.containers.run('bfirsh/reticulate-splines',
                                      detach=True)
    container.logs()

    # to see CPU usage use
    client.containers.run(cpuset_cpus)


if __name__ == '__main__':

    client = docker.from_env()
    client.containers.run('alpine', 'echo hello world')
    start_controller()

