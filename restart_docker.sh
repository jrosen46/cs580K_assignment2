#!/bin/bash

# if user specifies command line argument, then it restarts container with that
# name; if command line argument is not specified, then container that is
# listed first in the output of the `docker container ls -aq` is restarted.

if [ "$#" -eq 1 ]; then
    echo "here"
    docker start -ia "$1"
else
    docker start -ia $(docker container ls -aq | head -n1)
fi
