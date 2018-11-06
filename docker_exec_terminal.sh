#!/bin/bash

# if user specifies command line argument, then terminal is attached to
# container with that name; if command line argument is not specified, then
# terminal is attached to container that is listed first in the output of the
# `docker container ls -aq` command.

if [ "$#" -eq 1 ]; then
    echo "here"
    docker exec -it "$1" /bin/bash
else
    docker exec -it $(docker container ls -aq | head -n1) /bin/bash
fi
