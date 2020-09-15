#!/usr/bin/env python3
import docker
client = docker.from_env()
container = client.containers.run("buildserver", "bash -c \"emerge ufetch && ufetch\"", detach=True)

log_stream = container.logs(stream=True)

for line in log_stream:
    print(line.decode("utf-8"))

