#!/bin/bash

# docker run -it --rm --privileged -e DISPLAY \
#    -v /tmp/.X11-unix:/tmp/.X11-unix \
#    -v /lib/modules:/lib/modules \
#    my_mininet 

# take out the --rm option so that we can log back into container
docker run -it --privileged -e DISPLAY \
   -v /tmp/.X11-unix:/tmp/.X11-unix \
   -v /lib/modules:/lib/modules \
   my_mininet 
