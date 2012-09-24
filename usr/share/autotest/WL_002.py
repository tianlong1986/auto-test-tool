#!/usr/bin/python
#display sleep test after timeout on ac
import os
import sys
cmd="".join("/usr/share/autotest/network/wl_002.sh  %s" % (sys.argv[1]))
os.system(cmd)
