#!/usr/bin/python
#computer sleep test after timeout on ac
import os
import sys
cmd="".join("/usr/share/autotest/power/power2_sleep_inactive_ac.sh %s" % (sys.argv[1]))
os.system(cmd)
