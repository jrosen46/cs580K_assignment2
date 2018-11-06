#!/usr/bin/env python

import sys
import os
from collections import defaultdict


def main(path):
    """Parses specific format of 'traffic' file.
    """
    counters_conn = defaultdict(int)
    counters_dpid = defaultdict(int)
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(">>>> switch received packet connection ****"):
                counters_conn[line.split('****')[-1].strip()] += 1
            if line.startswith(">>>> switch received packet dpid ****"):
                counters_dpid[line.split('****')[-1].strip()] += 1

    def my_print(d, key_str):
        for k in sorted(d):
            print key_str + ": " + str(k) + " --> count: " + str(d[k])

    print ">>>> Connection counts"
    print "======================"
    my_print(counters_conn, "connection")

    print ">>>> dpid counts"
    print "================"
    my_print(counters_dpid, "dpid")
    

if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError(
            "supply one command line argument of " 
            "the name of the file that needs to be parsed.")

    if not os.path.exists(sys.argv[1]):
        raise ValueError(
            "given file does not exists.")

    main(sys.argv[1])
