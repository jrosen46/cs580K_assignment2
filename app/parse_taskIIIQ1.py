#!/usr/bin/env python

import sys
import os
from collections import defaultdict


def main(path):
    """Parses specific format of 'traffic' file.
    """
    counters_added = defaultdict(int)
    counters_in = defaultdict(int)
    counters_not_in= defaultdict(int)
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(">>>> ADDING "):
                temp = line.replace(">>>> ADDING ", "").split("****")
                src_mac, in_port = temp[0].split(',')
                key = (temp[1].strip(), src_mac.strip(), in_port.strip())
                counters_added[key] += 1

            if line.startswith(">>>> DESTINATION ALREADY KNOWN "):
                key = line.replace(">>>> IN ", "").split("****")
                key = (key[0].strip(), key[1].strip())
                counters_in[key] += 1

            if line.startswith(">>>> DESTINATION NOT KNOWN YET "):
                key = line.replace(">>>> NOT IN ", "").split("****")
                key = (key[0].strip(), key[1].strip())
                counters_not_in[key] += 1

    def my_print_adding(d):
        for k in sorted(d):
            print "dpid: " + str(k[0]) + ", src_mac: " + str(k[1]) + ", in_port: " + str(k[2]) + " --> count: " + str(d[k])
        

    def my_print(d):
        for k in sorted(d):
            print "dpid: " + str(k[0]) + ", dst_mac: " + str(k[1]) + " --> count: " + str(d[k])

    print ">>>> Adding to mapping"
    print "========================"
    my_print_adding(counters_added)

    print ">>>> Already in mapping"
    print "========================"
    my_print(counters_in)

    print ">>>> Not already in mapping"
    print "==========================="
    my_print(counters_not_in)
    

if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError(
            "supply one command line argument of " 
            "the name of the file that needs to be parsed.")

    if not os.path.exists(sys.argv[1]):
        raise ValueError(
            "given file does not exists.")

    main(sys.argv[1])
