#!/usr/bin/python
#display sleep test after timeout on battery
import os
import sys
cmd="".join("/usr/share/autotest/power/power3_sleep_display_battery.sh  %s" % (sys.argv[1]))
os.system(cmd)
