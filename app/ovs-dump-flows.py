#!/usr/bin/python

"""
Taken from: https://gist.github.com/djoreilly/3bcd6a81d9504bf740c4

Pass in switch as command line argument, i.e.
python ovs-dump-flows.py s1
"""

import sys
import re
import subprocess

if len(sys.argv) != 2:
    print "bridge name needed"
    sys.exit()

br_name = sys.argv[1]

port_map = dict()
def build_port_map():
    """ Parse names and ofport nums from lines like:
        2(vxlan-ac103c36): addr:fe:67:ed:fd:b6:41
        And build dict for name lookup by ofport num
    """
    pat =  re.compile("^ (\d+)\((.+)\)")
    lines = subprocess.check_output(['ovs-ofctl', 'show', br_name])
    for line in lines.splitlines():
        m = re.match(pat, line)
        if not m:
            continue
        ofport, port_name = m.group(1), m.group(2)
        port_map[ofport] = port_name


IN_PORT_PAT = re.compile("^(.*)(in_port=)(\d+)(,*.*)$")
def conv_match_ofport_to_name(s):
    """ Receives a line like 'blab in_port=2 blab'
        Returns line like 'blab in_port=vxlan-ac103c36 blab'
    """
    m = re.match(IN_PORT_PAT, s)
    if not m:
        return
    before = m.group(1)
    ofport = m.group(3)
    after = m.group(4)
    return "%sin_port=%s%s" % (before, port_map[ofport], after)


def conv_action_ofports_to_names(s):
    """
    eg receives : actions=strip_vlan,set_tunnel:0x3ec,output:3,output:2
    returns: actions=strip_vlan,set_tunnel:0x3ec,output:vxlan-ac103c37,output:vxlan-ac103c36
    """
    pat = re.compile("output:\d+")
    for f in pat.findall(s):
        ofport = f.partition(':')[2]
        s = s.replace(f, "output:%s" % port_map[ofport])
    return s


def print_flows():
    lines = subprocess.check_output(['ovs-ofctl', 'dump-flows', br_name])
    pat_with_priority = re.compile("^ cookie.+table=(\d+).+ priority=(\d+),*(.*) actions=(.+)")
    pat_no_priority = re.compile("^ cookie.+table=(\d+).+(n_bytes=\d+,) (.*) actions=(.+)")
    flows = []
    for line in lines.splitlines():
        m = re.match(pat_with_priority, line)
        if m:
            priority = m.group(2)
        else:
            m = re.match(pat_no_priority, line)
            if not m:
                # neither match found
                continue
            # ovs-ofctl man page says default priority is 32768
            priority = 32768

        table = m.group(1)
        match = m.group(3)
        actions = m.group(4)
        if "in_port" in match:
            match = conv_match_ofport_to_name(match)
        if "output" in actions:
            actions = conv_action_ofports_to_names(actions)
        flows.append([int(table), int(priority), match, actions])

    # sort by table name asending and then priority descending 
    flows.sort(key=lambda k: (k[0],-k[1]))
    
    for flow in flows:
            print "table=%d priority=%d %s actions=%s" % (flow[0], flow[1], flow[2], flow[3])

   
build_port_map()
print_flows()
