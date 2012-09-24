#!/usr/bin/python
#computer sleep test after timeout on battery
import os
import sys
cmd="".join("/usr/share/autotest/power/power4_sleep_inactive_battery.sh  %s" % (sys.argv[1]))
os.system(cmd)
