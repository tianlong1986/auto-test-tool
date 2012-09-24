#!/usr/bin/python
#display sleep test after timeout on ac
import os
import sys
cmd="".join("/usr/share/autotest/network/ln_008.sh  %s" % (sys.argv[1]))
os.system(cmd)
