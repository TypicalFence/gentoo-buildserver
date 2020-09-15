#!/usr/bin/env python3
import os
import time
import click
import docker

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
docker_client = docker.from_env()


def get_voulmes(profile):
    base = "{0}/.build_data/{1}".format(SCRIPT_DIR, profile)
    return {
        base + "/binpkgs": {"bind": "/var/cache/binpkgs", "mode": "rw"},
        base + "/repos": {"bind": "/var/db/repos", "mode": "rw"},
    }


def run_job(name, profile):
    moment = int(time.time())
    docker_client.containers.run(
        "buildserver",
        "/root/{0} {1}".format(name, profile),
        volumes=get_voulmes(profile),
        name="{0}-{1}-{2}".format(profile, name, moment),
        labels={"domain": "gentoo-build-job",
                "started": moment, "profile": profile, "job": name},
        detached=True
    )


@click.group()
def cli():
    pass


@cli.command()
@click.argument("profile")
def sync(profile):
    run_job("sync", profile)


@cli.command()
@click.argument("profile")
def build(profile):
    run_job("build", profile)
