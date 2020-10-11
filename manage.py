#!/usr/bin/env python3
import os
import time
import click
import docker

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
docker_client = docker.from_env()

capabilities = ["SYS_PTRACE"]

def ensure_profile_paths(profile):
    base = "{0}/.build_data/{1}".format(SCRIPT_DIR, profile)
    if not os.path.exists(base + "/binpkgs"):
        os.makedirs(base + "/binpkgs")

    if not os.path.exists(base + "/repos"):
        os.makedirs(base + "/repos")


def get_voulmes(profile):
    base = "{0}/.build_data/{1}".format(SCRIPT_DIR, profile)
    return {
        SCRIPT_DIR: {"bind": "/root/repo", "mode": "ro"},
        base + "/binpkgs": {"bind": "/var/cache/binpkgs", "mode": "rw"},
        base + "/repos": {"bind": "/var/db/repos", "mode": "rw"},
    }


def is_running(container_id):
    container = docker_client.containers.get(container_id)
    container_state = container.attrs['State']
    container_is_running = container_state['Running']

    return container_is_running


def run_job(name, profile):
    moment = int(time.time())
    container = docker_client.containers.run(
        "buildserver",
        "/root/{0} {1}".format(name, profile),
        volumes=get_voulmes(profile),
        name="{0}-{1}-{2}".format(profile.replace("/", "_"), name, moment),
        cap_add=capabilities,
        # labels={"domain": "gentoo-build",
        #         "started": moment, "profile": profile, "job": name},
        detach=True,
        tty=True
    )
    return container.id


def run_plain_container(profile):
    moment = int(time.time())
    container = docker_client.containers.run(
        "buildserver",
        "/root/shell {0}".format(profile),
        volumes=get_voulmes(profile),
        name="{0}-{1}".format(profile.replace("/", "_"), moment),
        cap_add=capabilities,
        # labels={"domain": "gentoo-build",
        #         "started": moment, "profile": profile, "job": "shell"},
        
        detach=True,
        tty=True,
        stdin_open=True,
    )
    return container.id


@click.group()
def cli():
    pass


@cli.command()
@click.argument("profile")
@click.option('--logs', is_flag=True)
def sync(profile, logs):
    ensure_profile_paths(profile)
    id = run_job("sync", profile)
    
    if logs:
        os.system("docker logs -f " + id)
 
        # stop container if the user CTR-C'd the logs
        if is_running(id):
            print("Stopping the Container!")
            print("might take a moment")
            docker_client.containers.get(id).stop()

    print(id)


@cli.command()
@click.argument("profile")
@click.option('--logs', is_flag=True)
def build(profile, logs):
    ensure_profile_paths(profile)
    id = run_job("build", profile)

    if logs:
        os.system("docker logs -f " + id)
    
        # stop container if the user CTR-C'd the logs
        if is_running(id):
            print("Stopping the Container!")
            print("might take a moment")
            docker_client.containers.get(id).stop()

    print(id)


@cli.command()
@click.argument("profile")
def shell(profile):
    ensure_profile_paths(profile)
    id = run_plain_container(profile)

    os.system("docker attach " + id)
    container = docker_client.containers.get(id)
    container.stop()
    container.remove()

if __name__ == '__main__':
    cli()
