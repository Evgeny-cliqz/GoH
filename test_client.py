
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sigmon probe for checking system health of current host.
"""

from arrow import now
from requests import post

from collections import defaultdict
from json import dumps
from platform import node
from optparse import OptionParser
from argparse import ArgumentParser

# please adjust following parameters!!!
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
OWNER= "cluster_test_admin"
HOST_GROUP= "my_cluster"
HOST_SUB_GROUP= "node001"
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#parser = OptionParser()
#parser.add_option("-d", "--dry-run", action="store_true", dest="dry_run", help="Dump signal JSON to console without sending it to Sigmon.")

#(options, args) = parser.parse_args()

p = ArgumentParser()
p.add_argument('-u', '--url', help='server url')
args = p.parse_args()

print args.url
SIGMON_URL = args.url

def get_load_avgs():
    with open("/proc/loadavg") as f:
        return f.read().strip().split()[:3]

def get_hostname():
    return node()

# using a tree builder for sigmon JSON message
Tree = lambda: defaultdict(Tree)
signal = Tree()



#load_avgs= get_load_avgs()

# determine the status of the system
sys_state = "OK"

# defining the signal header
signal['id']['application'] = HOST_GROUP
signal['id']['alias'] = HOST_SUB_GROUP
signal['id']['service'] = 'sys'
signal['id']['owner'] = OWNER
signal['id']['host'] = get_hostname().replace('.', '_')

signal['timestamp'] = str(now())
signal['periodicity'] = str(5 * 60)  # 5 minutes between signals

#signal['result'] = ...

# determine state of the ES swimlane cluster
signal['state'] = sys_state

# metrics
signal['metrics']['load.avg_1min'] = str(1)
signal['metrics']['load.avg_5min'] = str(2)
signal['metrics']['load.avg_15min'] = str(255)


# send signal to monitoring system
#if options.dry_run:
    #dump signal to console
    #print dumps(signal, sort_keys=True, indent=4)
#else:
    #send signal to sigmon
for i in range(300):
    signal['metrics']['load.avg_1min'] = str(i)
        resp = post(SIGMON_URL, data=dumps(signal), headers={'content-type': 'application/json'})

    #print str(resp.text)
    #print signal['state'], resp.status_code, str(resp.json())
