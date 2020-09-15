#!/usr/bin/env python3
import sys
import configparser

config = configparser.ConfigParser()
config.read(sys.argv[1])

repos = []

for key in config:
    if key not in ["DEFAULT", "gentoo", "gentoo-buildserver"]:
        repos.append(key)

for repo in repos:
    print(repo)
