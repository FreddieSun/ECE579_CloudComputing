#!/usr/bin/env python
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

count = 0
currentKey = None

for line in sys.stdin:
    line = line.strip()
    key, pcount = line.split('\t') # read stdin and get (key, pcount)


#### Complete the rest of the code
