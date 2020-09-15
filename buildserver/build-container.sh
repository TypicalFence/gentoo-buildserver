#!/bin/bash

# directory containing this script
dir=$(dirname "$0")

# we have to do this mess because 
# docker doesn't allow COPY .. .
# the image will be always built from the repository root
docker build -t buildserver -f $dir/Dockerfile $dir/..
