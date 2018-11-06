#!/usr/bin/env python

import sys
import os
import pprint
import re


def main(path):
    """Parse if config to get dict of switch number to ethernet address.
    """
    switch_to_mac = {}
    with open(path, 'r') as f:
        switch = None
        for line in f:
            if switch is not None:
                mac = re.search(r'\s*ether ([^\s]+)', line).group(1)
                switch_to_mac[switch] = mac
                switch = None
                continue

            m = re.match(r'(s\d): flags', line)
            if m is not None:
                switch = m.group(1)

    pprint.pprint(switch_to_mac) 
    

if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError(
            "supply one command line argument of " 
            "the name of the file that needs to be parsed.")

    if not os.path.exists(sys.argv[1]):
        raise ValueError(
            "given file does not exists.")

    main(sys.argv[1])
