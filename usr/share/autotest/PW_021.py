#!/usr/bin/python
#display sleep test after timeout on ac
import os
import sys
cmd="".join("/usr/share/autotest/power/power1_sleep_display_ac.sh  %s" % (sys.argv[1]))
os.system(cmd)
