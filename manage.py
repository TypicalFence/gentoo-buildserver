#!/usr/bin/env python3
import os
import time
import click
import docker

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
docker_client = docker.from_env()


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


def run_job(name, profile):
    moment = int(time.time())
    container = docker_client.containers.run(
        "buildserver",
        "/root/{0} {1}".format(name, profile),
        volumes=get_voulmes(profile),
        name="{0}-{1}-{2}".format(profile, name, moment),
        # labels={"domain": "gentoo-build",
        #         "started": moment, "profile": profile, "job": name},
        detach=True,
        tty=True
    )
    print(container.id)


def run_plain_container(profile):
    moment = int(time.time())
    container = docker_client.containers.run(
        "buildserver",
        "/bin/bash",
        volumes=get_voulmes(profile),
        name="{0}-{1}".format(profile, moment),
        # labels={"domain": "gentoo-build",
        #         "started": moment, "profile": profile, "job": "shell"},

        detach=True,
        tty=True
    )
    print(container.id)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("profile")
def sync(profile):
    ensure_profile_paths(profile)
    run_job("sync", profile)


@cli.command()
@click.argument("profile")
def build(profile):
    ensure_profile_paths(profile)
    run_job("build", profile)


@cli.command()
@click.argument("profile")
def shell(profile):
    ensure_profile_paths(profile)
    run_plain_container(profile)


if __name__ == '__main__':
    cli()
