#!/usr/bin/python
#display sleep test after timeout on ac
import os
import sys
cmd="".join("/usr/share/autotest/network/bt_012.sh  %s" % (sys.argv[1]))
os.system(cmd)
